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
ROLLOUT_LOOKUP_SECONDS = 5.0
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
    rollout: Path


@dataclass(frozen=True)
class ProcessOutcome:
    exit_code: int
    failure_reason: str | None


@dataclass(frozen=True)
class ExtractionOutcome:
    served_model: str | None
    served_effort: str | None
    thread_id: str | None
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


class CodexSummary(TypedDict):
    requested_model: str
    served_model: str | None
    effort: str
    served_effort: str | None
    fast: bool
    served_service_tier: str | None
    thread_id: str | None
    state: str
    exit_code: int
    failure_reason: str | None
    error_excerpt: str | None
    result_file: str
    raw_file: str
    progress_file: str
    error_file: str
    rollout_file: str | None


def main() -> int:
    args = parse_args()
    cwd = Path(args.cwd).resolve()
    prompt_path = Path(args.prompt_file).resolve()
    output_dir = Path(args.output_dir).resolve()
    validate_inputs(cwd, prompt_path, output_dir, args.timeout_seconds)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = build_artifacts(output_dir)
    prompt = build_prompt(prompt_path.read_text(encoding="utf-8"))
    command = build_command(resolve_codex(), cwd, args.model, args.effort, args.fast)
    process = run_process(command, cwd, prompt, artifacts, args.timeout_seconds)
    extraction = (
        extract_result(artifacts, args.model, args.effort)
        if process.exit_code == 0
        else None
    )
    failure_reason = process.failure_reason or (
        extraction.failure_reason if extraction else None
    )
    write_summary(
        artifacts,
        args.model,
        args.effort,
        args.fast,
        process.exit_code,
        extraction=extraction,
        failure_reason=failure_reason,
    )
    return 0 if failure_reason is None and extraction is not None else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a selected Codex model as a read-only consultant."
    )
    parser.add_argument("--cwd", required=True, help="Directory Codex may read")
    parser.add_argument(
        "--prompt-file", required=True, help="Self-contained task prompt"
    )
    parser.add_argument("--output-dir", required=True, help="Artifact directory")
    parser.add_argument(
        "--model",
        required=True,
        help="Exact Codex model slug",
    )
    parser.add_argument("--effort", choices=SUPPORTED_EFFORTS, required=True)
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Request the Fast service tier instead of the default tier",
    )
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
        raw=output_dir / "codex.events.jsonl",
        progress=output_dir / "codex.progress.log",
        error=output_dir / "codex.stderr.log",
        result=output_dir / "codex.result.md",
        summary=output_dir / "summary.json",
        rollout=output_dir / "codex.rollout.jsonl",
    )


def resolve_codex() -> str:
    requested = os.environ.get("CODEX_BIN", "codex")
    resolved = shutil.which(requested)
    if resolved is None:
        raise SystemExit(f"Required executable not found: {requested}")
    return resolved


def build_prompt(task_prompt: str) -> str:
    return CONSULTANT_BOUNDARY + task_prompt


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def build_command(
    binary: str, cwd: Path, model: str, effort: str, fast: bool
) -> tuple[str, ...]:
    return (
        binary,
        "exec",
        "--json",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--cd",
        str(cwd),
        "--model",
        model,
        "--config",
        f"model_reasoning_effort={json.dumps(effort)}",
        "--config",
        f"service_tier={json.dumps('fast' if fast else 'default')}",
        "-",
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
        write_progress(progress_stream, "Codex started")
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
            write_progress(progress_stream, "Codex interrupted")
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
        raise RuntimeError("Could not open stdin for Codex")
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
        raise RuntimeError("Could not open stdout for Codex")
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
    if event.get("type") != "item.started":
        return []
    item = event.get("item")
    if not isinstance(item, dict):
        return []
    kind = item.get("type")
    if not isinstance(kind, str) or kind in {"agent_message", "reasoning", "error"}:
        return []
    return [ToolActivity(kind, describe_item_activity(kind, item, cwd))]


def describe_item_activity(kind: str, item: dict[str, JsonValue], cwd: Path) -> str:
    if kind == "command_execution":
        return "Running a read-only shell command"
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
                "event": "codex.activity",
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
    artifacts: Artifacts, requested_model: str, requested_effort: str
) -> ExtractionOutcome:
    thread_id: str | None = None
    result: str | None = None
    events = read_events(artifacts.raw)
    if not events:
        return ExtractionOutcome(None, None, None, "malformed_output")
    for event in events:
        event_type = event.get("type")
        if event_type == "thread.started":
            candidate_thread = event.get("thread_id")
            thread_id = candidate_thread if isinstance(candidate_thread, str) else None
        elif event_type == "item.completed":
            message = agent_message(event)
            result = message if message is not None else result
    if thread_id is None:
        return ExtractionOutcome(None, None, None, "missing_thread_id")
    rollout = find_rollout(thread_id)
    if rollout is None:
        return ExtractionOutcome(None, None, thread_id, "missing_rollout")
    shutil.copyfile(rollout, artifacts.rollout)
    served_model, served_effort = rollout_provenance(rollout)
    if served_model != requested_model.strip() or served_effort != requested_effort:
        return ExtractionOutcome(served_model, served_effort, thread_id, "unverified_model")
    if not result or not result.strip():
        return ExtractionOutcome(served_model, served_effort, thread_id, "empty_result")
    artifacts.result.write_text(result.strip() + "\n", encoding="utf-8")
    return ExtractionOutcome(served_model, served_effort, thread_id, None)


def agent_message(event: dict[str, JsonValue]) -> str | None:
    item = event.get("item")
    if not isinstance(item, dict) or item.get("type") != "agent_message":
        return None
    text = item.get("text")
    return text if isinstance(text, str) else None


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


def rollout_provenance(rollout: Path) -> tuple[str | None, str | None]:
    served_model: str | None = None
    served_effort: str | None = None
    for event in read_events(rollout):
        if event.get("type") != "turn_context":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        model = payload.get("model")
        effort = payload.get("effort")
        served_model = model if isinstance(model, str) else served_model
        served_effort = effort if isinstance(effort, str) else served_effort
    return served_model, served_effort


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


def write_summary(
    artifacts: Artifacts,
    requested_model: str,
    effort: str,
    fast: bool,
    exit_code: int,
    *,
    extraction: ExtractionOutcome | None,
    failure_reason: str | None,
) -> None:
    succeeded = failure_reason is None and extraction is not None
    summary: CodexSummary = {
        "requested_model": requested_model,
        "served_model": extraction.served_model if extraction else None,
        "effort": effort,
        "served_effort": extraction.served_effort if extraction else None,
        "fast": fast,
        "served_service_tier": None,
        "thread_id": extraction.thread_id if extraction else None,
        "state": "succeeded" if succeeded else "failed",
        "exit_code": exit_code,
        "failure_reason": failure_reason,
        "error_excerpt": read_error_excerpt(artifacts.error),
        "result_file": str(artifacts.result),
        "raw_file": str(artifacts.raw),
        "progress_file": str(artifacts.progress),
        "error_file": str(artifacts.error),
        "rollout_file": str(artifacts.rollout) if artifacts.rollout.exists() else None,
    }
    artifacts.summary.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps({"event": "codex.completed", "summary": str(artifacts.summary)}),
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
        print("Codex invocation interrupted.", file=sys.stderr)
        raise SystemExit(130) from None
