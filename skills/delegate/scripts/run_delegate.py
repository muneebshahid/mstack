from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TextIO

SUPPORTED_EFFORTS = ("low", "medium", "high", "xhigh", "max")
CLAUDE_MODEL_ALIASES = ("fable", "haiku", "opus", "sonnet")
ROLLOUT_LOOKUP_SECONDS = 5.0
OUTPUT_DRAIN_SECONDS = 2.0
Provider = Literal["claude", "codex"]
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

NO_SUBAGENTS = "Work directly. Do not launch other agents, even when a skill offers delegation."


@dataclass(frozen=True)
class Arguments:
    provider: Provider
    cwd: Path
    prompt_file: Path | None
    model: str
    effort: str
    fast: bool
    allow_writes: bool
    allow_subagents: bool
    output_dir: Path | None
    resume_session_id: str | None
    timeout_seconds: int


@dataclass(frozen=True)
class Artifacts:
    directory: Path
    prompt: Path
    events: Path
    progress: Path
    error: Path
    result: Path
    summary: Path
    rollout: Path | None


@dataclass(frozen=True)
class ProcessOutcome:
    exit_code: int
    failure_reason: str | None


@dataclass(frozen=True)
class ExtractionOutcome:
    served_model: str | None
    served_effort: str | None
    native_session_id: str | None
    observed_session_id: str | None
    result: str | None
    failure_reason: str | None


@dataclass(frozen=True)
class ToolActivity:
    tool: str
    description: str


@dataclass
class ProgressState:
    tool_calls: int = 0
    last_activity: str | None = None


@dataclass(frozen=True)
class RunningProcess:
    process: subprocess.Popen[str]
    output_queue: queue.Queue[str]
    output_thread: threading.Thread
    input_thread: threading.Thread


def main() -> int:
    try:
        arguments = parse_args()
        normalized = normalize_arguments(arguments)
        task = (
            normalized.prompt_file.read_text(encoding="utf-8")
            if normalized.prompt_file
            else sys.stdin.read()
        )
        if not task.strip():
            raise LauncherError("Task prompt is empty")
        artifacts = prepare_artifacts(normalized)
        artifacts.prompt.write_text(
            build_prompt(task, normalized.allow_writes, normalized.allow_subagents),
            encoding="utf-8",
        )
        return run_turn(normalized, artifacts)
    except LauncherError as error:
        print(str(error), file=sys.stderr)
        return 1


def parse_args() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Delegate a task to Claude Code or Codex."
    )
    parser.add_argument("--provider", choices=("claude", "codex"), required=True)
    parser.add_argument("--cwd", required=True)
    parser.add_argument("--prompt-file", help="Read a task file instead of stdin")
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", choices=SUPPORTED_EFFORTS, required=True)
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--allow-writes", action="store_true")
    parser.add_argument("--allow-subagents", action="store_true")
    parser.add_argument("--output-dir")
    parser.add_argument("--resume", dest="resume_session_id", metavar="CONVERSATION_ID")
    parser.add_argument("--timeout-seconds", type=int, default=0)
    parsed = parser.parse_args()
    return Arguments(
        provider=parsed.provider,
        cwd=Path(parsed.cwd),
        prompt_file=Path(parsed.prompt_file) if parsed.prompt_file else None,
        model=parsed.model,
        effort=parsed.effort,
        fast=parsed.fast,
        allow_writes=parsed.allow_writes,
        allow_subagents=parsed.allow_subagents,
        output_dir=Path(parsed.output_dir) if parsed.output_dir else None,
        resume_session_id=parsed.resume_session_id,
        timeout_seconds=parsed.timeout_seconds,
    )


def normalize_arguments(arguments: Arguments) -> Arguments:
    cwd = arguments.cwd.expanduser().resolve()
    prompt_file = (
        arguments.prompt_file.expanduser().resolve() if arguments.prompt_file else None
    )
    output_dir = (
        arguments.output_dir.expanduser().resolve()
        if arguments.output_dir is not None
        else None
    )
    validate_inputs(cwd, prompt_file, output_dir, arguments.timeout_seconds)
    if arguments.provider == "claude" and arguments.fast:
        raise LauncherError("Fast service tier is only supported for Codex")
    return Arguments(
        provider=arguments.provider,
        cwd=cwd,
        prompt_file=prompt_file,
        model=arguments.model,
        effort=arguments.effort,
        fast=arguments.fast,
        allow_writes=arguments.allow_writes,
        allow_subagents=arguments.allow_subagents,
        output_dir=output_dir,
        resume_session_id=arguments.resume_session_id,
        timeout_seconds=arguments.timeout_seconds,
    )


def validate_inputs(
    cwd: Path,
    prompt_file: Path | None,
    output_dir: Path | None,
    timeout_seconds: int,
) -> None:
    if not cwd.is_dir():
        raise LauncherError(f"Working directory does not exist: {cwd}")
    if prompt_file is not None and not prompt_file.is_file():
        raise LauncherError(f"Prompt file does not exist: {prompt_file}")
    if prompt_file is not None and prompt_file.stat().st_size == 0:
        raise LauncherError(f"Prompt file is empty: {prompt_file}")
    if output_dir is not None and is_within(output_dir, cwd):
        raise LauncherError("Output directory must be outside the working directory")
    if timeout_seconds < 0:
        raise LauncherError("Timeout cannot be negative")


def is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def prepare_artifacts(arguments: Arguments) -> Artifacts:
    directory = allocate_output_directory(arguments)
    if is_within(directory, arguments.cwd):
        raise LauncherError("Output directory must be outside the working directory")
    rollout = directory / "codex.rollout.jsonl" if arguments.provider == "codex" else None
    return Artifacts(
        directory=directory,
        prompt=directory / "prompt.md",
        events=directory / f"{arguments.provider}.events.jsonl",
        progress=directory / f"{arguments.provider}.progress.log",
        error=directory / f"{arguments.provider}.stderr.log",
        result=directory / f"{arguments.provider}.result.md",
        summary=directory / "summary.json",
        rollout=rollout,
    )


def allocate_output_directory(arguments: Arguments) -> Path:
    if arguments.output_dir is None:
        root = Path(tempfile.gettempdir()).resolve()
        if is_within(root, arguments.cwd):
            raise LauncherError("Output directory must be outside the working directory; choose --output-dir")
        return Path(tempfile.mkdtemp(prefix="mstack-delegate-", dir=root))
    requested = arguments.output_dir
    if requested.exists() and not requested.is_dir():
        raise LauncherError(f"Output path is not a directory: {requested}")
    try:
        requested.mkdir(parents=True, exist_ok=False)
    except FileExistsError as error:
        raise LauncherError(f"Output directory already exists: {requested}") from error
    return requested


def run_turn(arguments: Arguments, artifacts: Artifacts) -> int:
    prompt = artifacts.prompt.read_text(encoding="utf-8")
    session_id = arguments.resume_session_id
    requested_tier = "fast" if arguments.fast else "default"
    rollout_start_offset = (
        resume_rollout_offset(session_id)
        if arguments.provider == "codex"
        else None
    )
    try:
        binary = resolve_binary(arguments.provider)
        command = build_command(
            arguments.provider,
            binary,
            arguments.cwd,
            arguments.model,
            arguments.effort,
            arguments.fast,
            session_id,
            arguments.allow_writes,
            arguments.allow_subagents,
        )
        process = run_process(
            arguments.provider,
            command,
            arguments.cwd,
            prompt,
            artifacts,
            arguments.timeout_seconds,
        )
    except LauncherError as error:
        print(str(error), file=sys.stderr)
        write_failure_artifacts(artifacts, arguments.provider, str(error))
        extraction = extract_result(
            arguments.provider,
            artifacts,
            arguments.model,
            arguments.effort,
            session_id,
            rollout_start_offset,
        )
        write_summary(
            arguments,
            artifacts,
            extraction,
            127,
            str(error),
            requested_tier,
            session_id,
        )
        return 1
    extraction = extract_result(
        arguments.provider,
        artifacts,
        arguments.model,
        arguments.effort,
        session_id,
        rollout_start_offset,
    )
    failure_reason = process.failure_reason or extraction.failure_reason
    write_summary(
        arguments,
        artifacts,
        extraction,
        process.exit_code,
        failure_reason,
        requested_tier,
        session_id,
    )
    succeeded = process.exit_code == 0 and failure_reason is None
    return 0 if succeeded else 1


def build_prompt(task_prompt: str, allow_writes: bool, allow_subagents: bool) -> str:
    access = (
        "Edit only within the caller's assigned scope."
        if allow_writes
        else "Investigate read-only. Do not edit project files or mutate external systems."
    )
    delegation = (
        "You may use Delegate to launch agents. Each new child defaults to allow_subagents=false; do not inherit this permission automatically."
        if allow_subagents
        else NO_SUBAGENTS
    )
    return f"## Assignment boundaries\n\n{access}\n{delegation}\nReport tool failures and unverified results.\n\n## Task\n\n{task_prompt}"


def resolve_binary(provider: Provider) -> str:
    variable = "CLAUDE_CODE_BIN" if provider == "claude" else "CODEX_BIN"
    default = "claude" if provider == "claude" else "codex"
    requested = os.environ.get(variable, default)
    resolved = shutil.which(requested)
    if resolved is None:
        raise LauncherError(f"Required executable not found: {requested}")
    return resolved


def build_command(
    provider: Provider,
    binary: str,
    cwd: Path,
    model: str,
    effort: str,
    fast: bool,
    resume_session_id: str | None,
    allow_writes: bool,
    allow_subagents: bool,
) -> tuple[str, ...]:
    if provider == "claude":
        return build_claude_command(
            binary, model, effort, resume_session_id, resolve_skill_dirs(), cwd, allow_writes
        )
    return build_codex_command(
        binary, cwd, model, effort, fast, resume_session_id, allow_writes, allow_subagents
    )


def resolve_skill_dirs() -> tuple[Path, ...]:
    packaged_skills = Path(__file__).resolve().parents[2]
    codex_root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    user_skills = codex_root / "skills"
    resolved = [packaged_skills]
    if user_skills.is_dir() and user_skills.resolve() != packaged_skills:
        resolved.append(user_skills.resolve())
    return tuple(resolved)


def build_claude_command(
    binary: str,
    model: str,
    effort: str,
    resume_session_id: str | None,
    skill_dirs: tuple[Path, ...],
    cwd: Path,
    allow_writes: bool,
) -> tuple[str, ...]:
    command: list[str] = [binary, "-p"]
    if resume_session_id is not None:
        command.extend(("--resume", resume_session_id))
    command.extend(
        (
            "--model",
            model,
            "--effort",
            effort,
            "--permission-mode",
            "auto",
            "--tools",
            "default",
            "--add-dir",
        )
    )
    command.extend(str(path) for path in skill_dirs)
    if allow_writes:
        command.extend(("--allowedTools", f"Edit(/{cwd.as_posix()}/**)"))
    command.extend(("--output-format", "stream-json", "--verbose"))
    return tuple(command)


def build_codex_command(
    binary: str,
    cwd: Path,
    model: str,
    effort: str,
    fast: bool,
    resume_session_id: str | None,
    allow_writes: bool,
    allow_subagents: bool,
) -> tuple[str, ...]:
    permissions = codex_permissions(cwd, allow_writes, allow_subagents)
    configs = (
        "--config",
        f"model_reasoning_effort={json.dumps(effort)}",
        "--config",
        f"service_tier={json.dumps('fast' if fast else 'default')}",
    )
    if resume_session_id is None:
        return (
            binary,
            "exec",
            "--json",
            "--skip-git-repo-check",
            *permissions,
            "--cd",
            str(cwd),
            "--model",
            model,
            *configs,
            "-",
        )
    return (
        binary,
        *permissions,
        "--cd",
        str(cwd),
        "--model",
        model,
        *configs,
        "exec",
        "resume",
        "--json",
        "--skip-git-repo-check",
        resume_session_id,
        "-",
    )


def codex_permissions(
    cwd: Path, allow_writes: bool, allow_subagents: bool
) -> tuple[str, ...]:
    if not allow_subagents:
        return ("--sandbox", "workspace-write" if allow_writes else "read-only")
    claude_root = Path(
        os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")
    ).expanduser().resolve()
    paths = {Path(tempfile.gettempdir()).resolve(): "write"}
    paths.update(
        {claude_root / name: "write" for name in ("projects", "session-env", "debug")}
    )
    if not allow_writes:
        paths[cwd] = "read"
    filesystem = ", ".join(
        f"{json.dumps(str(path))}={json.dumps(access)}" for path, access in paths.items()
    )
    base = ":workspace" if allow_writes else ":read-only"
    profile = f'{{extends={json.dumps(base)}, network={{enabled=true}}, filesystem={{{filesystem}}}}}'
    return (
        "--config",
        'default_permissions="mstack_delegate"',
        "--config",
        f"permissions.mstack_delegate={profile}",
    )


def run_process(
    provider: Provider,
    command: tuple[str, ...],
    cwd: Path,
    prompt: str,
    artifacts: Artifacts,
    timeout_seconds: int,
) -> ProcessOutcome:
    try:
        with (
            artifacts.events.open("x", encoding="utf-8") as events_stream,
            artifacts.progress.open("x", encoding="utf-8") as progress_stream,
            artifacts.error.open("x", encoding="utf-8") as error_stream,
        ):
            running = start_process(provider, command, cwd, prompt, error_stream)
            label = provider.capitalize()
            write_progress(progress_stream, f"{label} started")
            try:
                return wait_for_process(
                    provider,
                    running,
                    cwd,
                    events_stream,
                    progress_stream,
                    timeout_seconds,
                )
            except KeyboardInterrupt:
                stop_process(running.process, "interrupted")
                write_progress(progress_stream, f"{label} interrupted")
                exit_code = wait_after_stop(running.process)
                drain_output(
                    provider,
                    running,
                    events_stream,
                    progress_stream,
                    cwd,
                    time.monotonic(),
                    ProgressState(),
                )
                emit_status("completed", running.process.pid, exit_code=exit_code)
                write_progress(
                    progress_stream, f"Completed with exit code {exit_code}"
                )
                return ProcessOutcome(exit_code, "interrupted")
    except OSError as error:
        raise LauncherError(f"Could not start {provider} process: {error}") from error


def start_process(
    provider: Provider,
    command: tuple[str, ...],
    cwd: Path,
    prompt: str,
    error_stream: TextIO,
) -> RunningProcess:
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=error_stream,
            env=process_environment(provider),
            text=True,
        )
    except OSError as error:
        raise LauncherError(f"Could not start delegated process: {error}") from error
    output_queue, output_thread = start_output_reader(process)
    input_thread = start_input_writer(process, prompt)
    emit_status("started", process.pid)
    return RunningProcess(process, output_queue, output_thread, input_thread)


def process_environment(provider: Provider) -> dict[str, str]:
    environment = os.environ.copy()
    if provider == "claude":
        environment["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    return environment


def start_input_writer(process: subprocess.Popen[str], prompt: str) -> threading.Thread:
    if process.stdin is None:
        raise LauncherError("Could not open delegated stdin")
    input_thread = threading.Thread(
        target=write_prompt, args=(process.stdin, prompt), daemon=True
    )
    input_thread.start()
    return input_thread


def write_prompt(stream: TextIO, prompt: str) -> None:
    try:
        stream.write(prompt)
        stream.close()
    except (BrokenPipeError, OSError):
        return


def start_output_reader(
    process: subprocess.Popen[str],
) -> tuple[queue.Queue[str], threading.Thread]:
    if process.stdout is None:
        raise LauncherError("Could not open delegated stdout")
    output_queue: queue.Queue[str] = queue.Queue()
    output_thread = threading.Thread(
        target=enqueue_output, args=(process.stdout, output_queue), daemon=True
    )
    output_thread.start()
    return output_queue, output_thread


def enqueue_output(stream: TextIO, output_queue: queue.Queue[str]) -> None:
    for line in stream:
        output_queue.put(line)
    stream.close()


def wait_for_process(
    provider: Provider,
    running: RunningProcess,
    cwd: Path,
    events_stream: TextIO,
    progress_stream: TextIO,
    timeout_seconds: int,
) -> ProcessOutcome:
    process = running.process
    started_at = time.monotonic()
    next_heartbeat = started_at + 30
    timed_out = False
    progress = ProgressState()
    while process.poll() is None:
        elapsed = time.monotonic() - started_at
        if timeout_seconds > 0 and elapsed >= timeout_seconds:
            timed_out = stop_process(process, "timed_out")
            break
        consume_output(
            provider,
            running.output_queue,
            events_stream,
            progress_stream,
            cwd,
            process.pid,
            started_at,
            progress,
            wait_seconds=0.25,
        )
        if time.monotonic() >= next_heartbeat:
            emit_status(
                "running",
                process.pid,
                elapsed_seconds=int(elapsed),
                tool_calls=progress.tool_calls,
                last_activity=progress.last_activity,
            )
            latest = progress.last_activity or "waiting for the first tool call"
            write_progress(
                progress_stream,
                f"{format_elapsed(int(elapsed))} | Still running | "
                f"{progress.tool_calls} tool calls | Latest: {latest}",
            )
            next_heartbeat += 30
    exit_code = wait_after_stop(process)
    drain_output(
        provider,
        running,
        events_stream,
        progress_stream,
        cwd,
        started_at,
        progress,
    )
    emit_status("completed", process.pid, exit_code=exit_code)
    write_progress(
        progress_stream,
        f"{format_elapsed(int(time.monotonic() - started_at))} | "
        f"Completed with exit code {exit_code}",
    )
    if timed_out:
        return ProcessOutcome(exit_code, "timeout")
    return ProcessOutcome(exit_code, None if exit_code == 0 else "process_error")


def drain_output(
    provider: Provider,
    running: RunningProcess,
    events_stream: TextIO,
    progress_stream: TextIO,
    cwd: Path,
    started_at: float,
    progress: ProgressState,
) -> None:
    deadline = time.monotonic() + OUTPUT_DRAIN_SECONDS
    while running.output_thread.is_alive() or not running.output_queue.empty():
        if time.monotonic() >= deadline:
            emit_status(
                "output_drain_ended",
                running.process.pid,
                tool_calls=progress.tool_calls,
                last_activity=progress.last_activity,
            )
            return
        consume_output(
            provider,
            running.output_queue,
            events_stream,
            progress_stream,
            cwd,
            running.process.pid,
            started_at,
            progress,
            wait_seconds=0.05,
        )
    running.output_thread.join()
    running.input_thread.join(timeout=0.1)


def consume_output(
    provider: Provider,
    output_queue: queue.Queue[str],
    events_stream: TextIO,
    progress_stream: TextIO,
    cwd: Path,
    pid: int,
    started_at: float,
    progress: ProgressState,
    *,
    wait_seconds: float,
) -> None:
    try:
        line = output_queue.get(timeout=wait_seconds)
    except queue.Empty:
        return
    events_stream.write(line)
    events_stream.flush()
    event = parse_event(line)
    if event is None:
        return
    for activity in activities_from_event(provider, event, cwd):
        progress.tool_calls += 1
        progress.last_activity = activity.description
        emit_activity(
            provider,
            pid,
            int(time.monotonic() - started_at),
            progress.tool_calls,
            activity,
            progress_stream,
        )


def parse_event(line: str) -> dict[str, JsonValue] | None:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        return None
    return event if isinstance(event, dict) else None


def activities_from_event(
    provider: Provider, event: dict[str, JsonValue], cwd: Path
) -> list[ToolActivity]:
    if provider == "claude":
        return claude_activities(event, cwd)
    return codex_activities(event, cwd)


def claude_activities(
    event: dict[str, JsonValue], cwd: Path
) -> list[ToolActivity]:
    if event.get("type") != "assistant":
        return []
    message = event.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if not isinstance(content, list):
        return []
    activities: list[ToolActivity] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        name = block.get("name")
        if not isinstance(name, str):
            continue
        tool_input = block.get("input")
        inputs = tool_input if isinstance(tool_input, dict) else {}
        activities.append(ToolActivity(name, describe_claude_activity(name, inputs, cwd)))
    return activities


def describe_claude_activity(
    name: str, inputs: dict[str, JsonValue], cwd: Path
) -> str:
    normalized = name.lower()
    if normalized in {"read", "notebookread"}:
        return f"Reading {display_path(inputs, cwd)}"
    if normalized in {"grep", "search"}:
        return f"Searching repository contents in {display_path(inputs, cwd)}"
    if normalized in {"glob", "find"}:
        return f"Scanning repository paths in {display_path(inputs, cwd)}"
    if normalized in {"bash", "shell"}:
        return "Running a shell command"
    if "websearch" in normalized or "web_search" in normalized:
        return "Searching the web"
    if "webfetch" in normalized or "web_fetch" in normalized:
        return "Reading a web source"
    if normalized in {"skill", "slashcommand"}:
        return "Loading a skill"
    if normalized in {"todowrite", "taskupdate"}:
        return "Updating its work plan"
    return f"Using {display_tool_name(name)}"


def codex_activities(
    event: dict[str, JsonValue], cwd: Path
) -> list[ToolActivity]:
    if event.get("type") != "item.started":
        return []
    item = event.get("item")
    if not isinstance(item, dict):
        return []
    kind = item.get("type")
    if not isinstance(kind, str) or kind in {"agent_message", "reasoning", "error"}:
        return []
    return [ToolActivity(kind, describe_codex_activity(kind, item, cwd))]


def describe_codex_activity(
    kind: str, item: dict[str, JsonValue], cwd: Path
) -> str:
    if kind == "command_execution":
        return "Running a shell command"
    if kind == "file_change":
        return "Attempting a file change"
    if kind == "mcp_tool_call":
        server = item.get("server")
        tool = item.get("tool")
        if isinstance(server, str) and isinstance(tool, str):
            return f"Using {server} {display_tool_name(tool)}"
        return "Using an MCP tool"
    if kind == "web_search":
        return "Searching the web"
    if kind == "todo_list":
        return "Updating its work plan"
    return f"Using {display_tool_name(kind)}"


def display_path(inputs: dict[str, JsonValue], cwd: Path) -> str:
    value = inputs.get("file_path") or inputs.get("path")
    if not isinstance(value, str) or not value.strip():
        return "the workspace"
    path = Path(value)
    if not path.is_absolute():
        return str(path)
    try:
        return str(path.relative_to(cwd))
    except ValueError:
        return "an external file"


def display_tool_name(name: str) -> str:
    leaf = name.rsplit("__", maxsplit=1)[-1]
    return leaf.replace("_", " ").replace("-", " ")


def emit_activity(
    provider: Provider,
    pid: int,
    elapsed_seconds: int,
    tool_calls: int,
    activity: ToolActivity,
    progress_stream: TextIO,
) -> None:
    print(
        json.dumps(
            {
                "event": f"{provider}.activity",
                "pid": pid,
                "elapsed_seconds": elapsed_seconds,
                "tool_calls": tool_calls,
                "tool": activity.tool,
                "activity": activity.description,
            }
        ),
        flush=True,
    )
    write_progress(
        progress_stream,
        f"{format_elapsed(elapsed_seconds)} | Tool {tool_calls} | "
        f"{activity.description}",
    )


def write_progress(stream: TextIO, message: str) -> None:
    stream.write(message + "\n")
    stream.flush()


def format_elapsed(elapsed_seconds: int) -> str:
    minutes, seconds = divmod(elapsed_seconds, 60)
    return f"{minutes}m {seconds:02d}s" if minutes else f"{seconds}s"


def stop_process(process: subprocess.Popen[str], event: str) -> bool:
    if process.poll() is not None:
        return False
    try:
        process.terminate()
    except ProcessLookupError:
        return False
    emit_status(event, process.pid)
    return True


def wait_after_stop(process: subprocess.Popen[str]) -> int:
    try:
        return process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        return process.wait()


def extract_result(
    provider: Provider,
    artifacts: Artifacts,
    requested_model: str,
    requested_effort: str,
    known_session_id: str | None,
    rollout_start_offset: int | None,
) -> ExtractionOutcome:
    events = read_events(artifacts.events)
    if provider == "claude":
        return extract_claude_result(
            events, artifacts, requested_model, known_session_id
        )
    return extract_codex_result(
        events,
        artifacts,
        requested_model,
        requested_effort,
        known_session_id,
        rollout_start_offset,
    )


def extract_claude_result(
    events: list[dict[str, JsonValue]],
    artifacts: Artifacts,
    requested_model: str,
    known_session_id: str | None,
) -> ExtractionOutcome:
    served_model: str | None = None
    observed_session_id: str | None = None
    result: str | None = None
    for event in events:
        observed_session_id = event_session_id(event) or observed_session_id
        if event.get("type") == "assistant":
            served_model = assistant_model(event) or served_model
        if event.get("type") == "result" and event.get("subtype") == "success":
            candidate = event.get("result")
            result = candidate if isinstance(candidate, str) else result
    failure_reason = None
    native_session_id = observed_session_id or known_session_id
    if not events:
        failure_reason = "malformed_output"
    elif observed_session_id is None:
        failure_reason = "missing_session_id"
    elif (
        known_session_id is not None
        and observed_session_id is not None
        and observed_session_id != known_session_id
    ):
        native_session_id = known_session_id
        failure_reason = "session_id_mismatch"
    elif served_model is None or not model_matches_claude(requested_model, served_model):
        failure_reason = "unverified_model"
    elif not result or not result.strip():
        failure_reason = "empty_result"
    if failure_reason is None and result is not None:
        artifacts.result.write_text(result.strip() + "\n", encoding="utf-8")
    return ExtractionOutcome(
        served_model,
        None,
        native_session_id,
        observed_session_id,
        result,
        failure_reason,
    )


def extract_codex_result(
    events: list[dict[str, JsonValue]],
    artifacts: Artifacts,
    requested_model: str,
    requested_effort: str,
    known_session_id: str | None,
    rollout_start_offset: int | None,
) -> ExtractionOutcome:
    observed_session_id: str | None = None
    result: str | None = None
    current_turn_id = current_codex_turn_id(events)
    for event in events:
        if event.get("type") == "thread.started":
            candidate = event.get("thread_id")
            if isinstance(candidate, str):
                observed_session_id = candidate
        if event.get("type") != "item.completed":
            continue
        event_turn = event_turn_id(event)
        if current_turn_id is not None and event_turn != current_turn_id:
            continue
        candidate_result = codex_agent_message(event)
        if candidate_result is not None:
            result = candidate_result
    if not events:
        return ExtractionOutcome(
            None, None, known_session_id, observed_session_id, result, "malformed_output"
        )
    native_session_id = observed_session_id or known_session_id
    if known_session_id is not None and observed_session_id is None:
        return ExtractionOutcome(
            None,
            None,
            known_session_id,
            observed_session_id,
            result,
            "missing_thread_id",
        )
    if native_session_id is None:
        return ExtractionOutcome(
            None, None, None, observed_session_id, result, "missing_thread_id"
        )
    if known_session_id is not None and native_session_id != known_session_id:
        return ExtractionOutcome(
            None,
            None,
            known_session_id,
            observed_session_id,
            result,
            "session_id_mismatch",
        )
    rollout = find_rollout(native_session_id)
    if rollout is None:
        return ExtractionOutcome(
            None,
            None,
            native_session_id,
            observed_session_id,
            result,
            "missing_rollout",
        )
    if artifacts.rollout is None:
        raise LauncherError("Codex rollout artifact path is unavailable")
    shutil.copyfile(rollout, artifacts.rollout)
    served_model, served_effort = rollout_provenance(
        rollout, current_turn_id, rollout_start_offset
    )
    failure_reason = None
    if served_model != requested_model.strip() or served_effort != requested_effort:
        failure_reason = "unverified_model"
    elif not result or not result.strip():
        failure_reason = "empty_result"
    if failure_reason is None and result is not None:
        artifacts.result.write_text(result.strip() + "\n", encoding="utf-8")
    return ExtractionOutcome(
        served_model,
        served_effort,
        native_session_id,
        observed_session_id,
        result,
        failure_reason,
    )


def event_session_id(event: dict[str, JsonValue]) -> str | None:
    for key in ("session_id", "sessionId"):
        value = event.get(key)
        if isinstance(value, str) and value:
            return value
    for key in ("message", "payload"):
        nested = event.get(key)
        if isinstance(nested, dict):
            value = nested.get("session_id") or nested.get("sessionId")
            if isinstance(value, str) and value:
                return value
    return None


def assistant_model(event: dict[str, JsonValue]) -> str | None:
    message = event.get("message")
    if not isinstance(message, dict):
        return None
    model = message.get("model")
    return model if isinstance(model, str) else None


def model_matches_claude(requested_model: str, served_model: str) -> bool:
    requested = requested_model.strip().lower()
    served = served_model.strip().lower()
    if requested in CLAUDE_MODEL_ALIASES:
        return f"claude-{requested}-" in served
    return requested == served


def current_codex_turn_id(events: list[dict[str, JsonValue]]) -> str | None:
    for event in reversed(events):
        turn_id = event_turn_id(event)
        if turn_id is not None:
            return turn_id
    return None


def event_turn_id(event: dict[str, JsonValue]) -> str | None:
    value = event.get("turn_id")
    if isinstance(value, str) and value:
        return value
    for key in ("payload", "item"):
        nested = event.get(key)
        if isinstance(nested, dict):
            value = nested.get("turn_id")
            if isinstance(value, str) and value:
                return value
    return None


def codex_agent_message(event: dict[str, JsonValue]) -> str | None:
    item = event.get("item")
    if not isinstance(item, dict) or item.get("type") != "agent_message":
        return None
    text = item.get("text")
    return text if isinstance(text, str) else None


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def find_rollout(thread_id: str) -> Path | None:
    sessions = codex_home() / "sessions"
    deadline = time.monotonic() + ROLLOUT_LOOKUP_SECONDS
    while True:
        matches = sorted(sessions.glob(f"**/rollout-*-{thread_id}.jsonl"))
        if matches:
            return matches[-1]
        if time.monotonic() >= deadline:
            return None
        time.sleep(0.25)


def resume_rollout_offset(thread_id: str | None) -> int | None:
    if thread_id is None:
        return None
    rollout = existing_rollout(thread_id)
    if rollout is None:
        return None
    try:
        return rollout.stat().st_size
    except OSError:
        return None


def existing_rollout(thread_id: str) -> Path | None:
    matches = sorted((codex_home() / "sessions").glob(f"**/rollout-*-{thread_id}.jsonl"))
    return matches[-1] if matches else None


def rollout_provenance(
    rollout: Path, current_turn_id: str | None, start_offset: int | None
) -> tuple[str | None, str | None]:
    contexts: list[tuple[str | None, str | None, str | None]] = []
    events = read_events(rollout, start_offset or 0)
    for event in events:
        if event.get("type") != "turn_context":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        model = payload.get("model")
        effort = payload.get("effort")
        context_turn_id = payload.get("turn_id")
        contexts.append(
            (
                model if isinstance(model, str) else None,
                effort if isinstance(effort, str) else None,
                context_turn_id if isinstance(context_turn_id, str) else None,
            )
        )
    if current_turn_id is not None:
        matching = [context for context in contexts if context[2] == current_turn_id]
        if not matching:
            return None, None
        return matching[-1][0], matching[-1][1]
    if not contexts:
        return None, None
    return contexts[-1][0], contexts[-1][1]


def read_events(path: Path, start_offset: int = 0) -> list[dict[str, JsonValue]]:
    events: list[dict[str, JsonValue]] = []
    try:
        with path.open("rb") as stream:
            stream.seek(start_offset)
            lines = stream.read().decode("utf-8").splitlines()
    except OSError:
        return events
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def write_failure_artifacts(artifacts: Artifacts, provider: Provider, message: str) -> None:
    artifacts.events.touch()
    artifacts.progress.write_text(f"{provider.capitalize()} failed before launch\n", encoding="utf-8")
    artifacts.error.write_text(message + "\n", encoding="utf-8")


def write_summary(
    arguments: Arguments,
    artifacts: Artifacts,
    extraction: ExtractionOutcome,
    exit_code: int,
    failure_reason: str | None,
    requested_tier: str,
    resumed_from: str | None,
) -> None:
    native_session_id = extraction.native_session_id or resumed_from
    summary: dict[str, JsonValue] = {
        "provider": arguments.provider,
        "cwd": str(arguments.cwd),
        "native_session_id": native_session_id,
        "thread_id": native_session_id
        if arguments.provider == "codex"
        else None,
        "resumed_from": resumed_from,
        "requested_model": arguments.model,
        "served_model": extraction.served_model,
        "effort": arguments.effort,
        "served_effort": extraction.served_effort,
        "fast": arguments.fast,
        "allow_writes": arguments.allow_writes,
        "allow_subagents": arguments.allow_subagents,
        "requested_service_tier": requested_tier
        if arguments.provider == "codex"
        else None,
        "served_service_tier": None,
        "state": "succeeded" if failure_reason is None and exit_code == 0 else "failed",
        "exit_code": exit_code,
        "failure_reason": failure_reason,
        "error_excerpt": read_error_excerpt(artifacts.error),
        "artifact_dir": str(artifacts.directory),
        "prompt_file": str(artifacts.prompt),
        "result_file": str(artifacts.result),
        "raw_file": str(artifacts.events),
        "progress_file": str(artifacts.progress),
        "error_file": str(artifacts.error),
        "rollout_file": str(artifacts.rollout)
        if artifacts.rollout is not None and artifacts.rollout.exists()
        else None,
    }
    artifacts.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "event": f"{arguments.provider}.completed",
                "native_session_id": native_session_id,
                "summary": str(artifacts.summary),
            }
        ),
        flush=True,
    )


def read_error_excerpt(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return content[:1000] if content else None


def emit_status(
    event: str,
    pid: int,
    elapsed_seconds: int | None = None,
    exit_code: int | None = None,
    tool_calls: int | None = None,
    last_activity: str | None = None,
) -> None:
    payload: dict[str, str | int] = {"event": event, "pid": pid}
    if elapsed_seconds is not None:
        payload["elapsed_seconds"] = elapsed_seconds
    if exit_code is not None:
        payload["exit_code"] = exit_code
    if tool_calls is not None:
        payload["tool_calls"] = tool_calls
    if last_activity is not None:
        payload["last_activity"] = last_activity
    print(json.dumps(payload), flush=True)


class LauncherError(Exception):
    pass


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Delegation interrupted.", file=sys.stderr)
        raise SystemExit(130) from None
