from __future__ import annotations

import argparse
import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO, TypedDict

SUPPORTED_EFFORTS = ("low", "medium", "high", "xhigh", "max")
MODEL_ALIASES = ("fable", "haiku", "opus", "sonnet")
OUTPUT_DRAIN_SECONDS = 2.0
CONSULTANT_BOUNDARY = """\
## Operating Boundary

Act only as an independent consultant. Investigate freely using the available
filesystem, shell, plugins, skills, MCP servers, and other tools, but do not change state.
Do not edit or create project files, run mutating commands,
modify external systems, create or update tickets, commit, push, or delegate
implementation. Treat write-capable tools as available only for read-only
inspection. If the task would require a mutation, explain what would need to
change and leave the action to the parent agent.

If an expected tool, MCP server, plugin, skill, file, permission, authentication,
or other capability is missing, inaccessible, or fails, do not hide the problem
or silently treat that source as searched. Continue with the available evidence
when possible and do not repeatedly retry the same failure. In the final report,
include a "Capability and Tool Issues" section that records each problem, the
operation attempted, a concise observed error, the evidence or work affected,
its impact on completeness or confidence, and a useful next diagnostic or setup
step. Redact credentials and other secrets. Distinguish a failed or unavailable
source from one that was searched successfully and returned no relevant result.
Omit the section when no capability or tool issue occurred.

"""
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


@dataclass(frozen=True)
class Artifacts:
    raw: Path
    progress: Path
    error: Path
    result: Path
    summary: Path


@dataclass(frozen=True)
class ProcessOutcome:
    exit_code: int
    failure_reason: str | None


@dataclass(frozen=True)
class ExtractionOutcome:
    served_model: str | None
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


class ClaudeSummary(TypedDict):
    requested_model: str
    served_model: str | None
    effort: str
    state: str
    exit_code: int
    failure_reason: str | None
    error_excerpt: str | None
    result_file: str
    raw_file: str
    progress_file: str
    error_file: str


def main() -> int:
    args = parse_args()
    cwd = Path(args.cwd).resolve()
    prompt_path = Path(args.prompt_file).resolve()
    output_dir = Path(args.output_dir).resolve()
    validate_inputs(cwd, prompt_path, output_dir, args.timeout_seconds)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = build_artifacts(output_dir)
    prompt = build_prompt(prompt_path.read_text(encoding="utf-8"))
    command = build_command(
        resolve_claude(), args.model, args.effort, resolve_skill_dirs()
    )
    process = run_process(command, cwd, prompt, artifacts, args.timeout_seconds)
    extraction = extract_result(artifacts, args.model) if process.exit_code == 0 else None
    served_model = extraction.served_model if extraction else None
    failure_reason = process.failure_reason or (
        extraction.failure_reason if extraction else None
    )
    write_summary(
        artifacts,
        args.model,
        args.effort,
        process.exit_code,
        served_model=served_model,
        failure_reason=failure_reason,
    )
    return 0 if served_model is not None else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a selected Claude Code model as a read-only consultant."
    )
    parser.add_argument("--cwd", required=True, help="Trusted directory Claude may read")
    parser.add_argument(
        "--prompt-file", required=True, help="Self-contained task prompt"
    )
    parser.add_argument("--output-dir", required=True, help="Artifact directory")
    parser.add_argument(
        "--model",
        required=True,
        help="Claude model alias or exact model identifier",
    )
    parser.add_argument("--effort", choices=SUPPORTED_EFFORTS, required=True)
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=0,
        help="Optional positive process timeout; 0 keeps the run open-ended",
    )
    return parser.parse_args()


def validate_inputs(
    cwd: Path, prompt_path: Path, output_dir: Path, timeout_seconds: int
) -> None:
    if not cwd.is_dir():
        raise SystemExit(f"Working directory does not exist: {cwd}")
    if not prompt_path.is_file():
        raise SystemExit(f"Prompt file does not exist: {prompt_path}")
    if prompt_path.stat().st_size == 0:
        raise SystemExit(f"Prompt file is empty: {prompt_path}")
    if output_dir == cwd or cwd in output_dir.parents:
        raise SystemExit("Output directory must be outside the working directory")
    if timeout_seconds < 0:
        raise SystemExit("Timeout cannot be negative")


def build_artifacts(output_dir: Path) -> Artifacts:
    return Artifacts(
        raw=output_dir / "claude.events.jsonl",
        progress=output_dir / "claude.progress.log",
        error=output_dir / "claude.stderr.log",
        result=output_dir / "claude.result.md",
        summary=output_dir / "summary.json",
    )


def resolve_claude() -> str:
    requested = os.environ.get("CLAUDE_CODE_BIN", "claude")
    resolved = shutil.which(requested)
    if resolved is None:
        raise SystemExit(f"Required executable not found: {requested}")
    return resolved


def build_prompt(task_prompt: str) -> str:
    return CONSULTANT_BOUNDARY + task_prompt


def resolve_skill_dirs() -> tuple[Path, ...]:
    packaged_skills = Path(__file__).resolve().parents[2]
    codex_root = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    user_skills = codex_root / "skills"
    resolved = [packaged_skills]
    if user_skills.is_dir() and user_skills.resolve() != packaged_skills:
        resolved.append(user_skills.resolve())
    return tuple(resolved)


def build_command(
    binary: str, model: str, effort: str, skill_dirs: tuple[Path, ...]
) -> tuple[str, ...]:
    return (
        binary,
        "-p",
        "--model",
        model,
        "--effort",
        effort,
        "--permission-mode",
        "auto",
        "--tools",
        "default",
        "--add-dir",
        *(str(path) for path in skill_dirs),
        "--no-session-persistence",
        "--output-format",
        "stream-json",
        "--verbose",
    )


def run_process(
    command: tuple[str, ...],
    cwd: Path,
    prompt: str,
    artifacts: Artifacts,
    timeout_seconds: int,
) -> ProcessOutcome:
    with (
        artifacts.raw.open("w", encoding="utf-8") as raw_stream,
        artifacts.progress.open("w", encoding="utf-8") as progress_stream,
        artifacts.error.open("w", encoding="utf-8") as error_stream,
    ):
        running = start_process(command, cwd, prompt, error_stream)
        write_progress(progress_stream, "Claude started")
        try:
            return wait_for_process(
                running,
                cwd,
                raw_stream,
                progress_stream,
                timeout_seconds,
            )
        except KeyboardInterrupt:
            stop_process(running.process, "interrupted")
            write_progress(progress_stream, "Claude interrupted")
            raise


def start_process(
    command: tuple[str, ...],
    cwd: Path,
    prompt: str,
    error_stream: TextIO,
) -> RunningProcess:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=error_stream,
        text=True,
    )
    output_queue, output_thread = start_output_reader(process)
    input_thread = start_input_writer(process, prompt)
    emit_status("started", process.pid)
    return RunningProcess(process, output_queue, output_thread, input_thread)


def wait_for_process(
    running: RunningProcess,
    cwd: Path,
    raw_stream: TextIO,
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
            running.output_queue,
            raw_stream,
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
        running,
        raw_stream,
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
    failure_reason = None if exit_code == 0 else "process_error"
    return ProcessOutcome(exit_code, failure_reason)


def start_input_writer(process: subprocess.Popen[str], prompt: str) -> threading.Thread:
    if process.stdin is None:
        raise RuntimeError("Could not open stdin for Claude")
    input_thread = threading.Thread(
        target=write_prompt,
        args=(process.stdin, prompt),
        daemon=True,
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
        raise RuntimeError("Could not open stdout for Claude")
    output_queue: queue.Queue[str] = queue.Queue()
    output_thread = threading.Thread(
        target=enqueue_output,
        args=(process.stdout, output_queue),
        daemon=True,
    )
    output_thread.start()
    return output_queue, output_thread


def enqueue_output(stream: TextIO, output_queue: queue.Queue[str]) -> None:
    for line in stream:
        output_queue.put(line)
    stream.close()


def drain_output(
    running: RunningProcess,
    raw_stream: TextIO,
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
            running.output_queue,
            raw_stream,
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
    output_queue: queue.Queue[str],
    raw_stream: TextIO,
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
    raw_stream.write(line)
    raw_stream.flush()
    event = parse_event(line)
    if event is None:
        return
    for activity in activities_from_event(event, cwd):
        progress.tool_calls += 1
        progress.last_activity = activity.description
        emit_activity(
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


def activities_from_event(event: dict[str, JsonValue], cwd: Path) -> list[ToolActivity]:
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
        activities.append(ToolActivity(name, describe_tool_activity(name, inputs, cwd)))
    return activities


def describe_tool_activity(name: str, inputs: dict[str, JsonValue], cwd: Path) -> str:
    normalized = name.lower()
    if normalized in {"read", "notebookread"}:
        return f"Reading {display_path(inputs, cwd)}"
    if normalized in {"grep", "search"}:
        return f"Searching repository contents in {display_path(inputs, cwd)}"
    if normalized in {"glob", "find"}:
        return f"Scanning repository paths in {display_path(inputs, cwd)}"
    if normalized in {"bash", "shell"}:
        return "Running a read-only shell command"
    if "websearch" in normalized or "web_search" in normalized:
        return "Searching the web"
    if "webfetch" in normalized or "web_fetch" in normalized:
        return "Reading a web source"
    if normalized in {"skill", "slashcommand"}:
        return "Loading a skill"
    if normalized in {"todowrite", "taskupdate"}:
        return "Updating its work plan"
    return f"Using {display_tool_name(name)}"


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
    pid: int,
    elapsed_seconds: int,
    tool_calls: int,
    activity: ToolActivity,
    progress_stream: TextIO,
) -> None:
    print(
        json.dumps(
            {
                "event": "claude.activity",
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


def extract_result(artifacts: Artifacts, requested_model: str) -> ExtractionOutcome:
    served_model: str | None = None
    result: str | None = None
    events = read_events(artifacts.raw)
    if not events:
        return ExtractionOutcome(None, "malformed_output")
    for event in events:
        event_type = event.get("type")
        if event_type == "assistant":
            served_model = assistant_model(event) or served_model
        elif event_type == "result" and event.get("subtype") == "success":
            candidate = event.get("result")
            result = candidate if isinstance(candidate, str) else None
    if served_model is None or not model_matches(requested_model, served_model):
        return ExtractionOutcome(None, "unverified_model")
    if not result or not result.strip():
        return ExtractionOutcome(None, "empty_result")
    artifacts.result.write_text(result.strip() + "\n", encoding="utf-8")
    return ExtractionOutcome(served_model, None)


def model_matches(requested_model: str, served_model: str) -> bool:
    requested = requested_model.strip().lower()
    served = served_model.strip().lower()
    if requested in MODEL_ALIASES:
        return f"claude-{requested}-" in served
    return requested == served


def read_events(path: Path) -> list[dict[str, JsonValue]]:
    events: list[dict[str, JsonValue]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
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


def assistant_model(event: dict[str, JsonValue]) -> str | None:
    message = event.get("message")
    if not isinstance(message, dict):
        return None
    model = message.get("model")
    return model if isinstance(model, str) else None


def write_summary(
    artifacts: Artifacts,
    requested_model: str,
    effort: str,
    exit_code: int,
    *,
    served_model: str | None,
    failure_reason: str | None,
) -> None:
    summary: ClaudeSummary = {
        "requested_model": requested_model,
        "served_model": served_model,
        "effort": effort,
        "state": "succeeded" if served_model is not None else "failed",
        "exit_code": exit_code,
        "failure_reason": failure_reason,
        "error_excerpt": read_error_excerpt(artifacts.error),
        "result_file": str(artifacts.result),
        "raw_file": str(artifacts.raw),
        "progress_file": str(artifacts.progress),
        "error_file": str(artifacts.error),
    }
    artifacts.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps({"event": "claude.completed", "summary": str(artifacts.summary)}),
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


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Claude Code invocation interrupted.", file=sys.stderr)
        raise SystemExit(130) from None
