from __future__ import annotations

import json
import os
import signal
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

RUNNER = Path(__file__).with_name("run_consult.py")
CLAUDE_SESSION_ID = "claude-session-0001"
CODEX_THREAD_ID = "01a068d6-0000-7000-8000-000000000001"
CODEX_TURN_ID = "01a068d6-0000-7000-8000-000000000002"
type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


class RunConsultTest(unittest.TestCase):
    def test_claude_success_keeps_persistence_and_disables_memory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root, "claude", create_fake_claude(root)
            )
            assert completed.returncode == 0, completed.stderr
            summary = read_summary(output_dir)
            assert summary["provider"] == "claude"
            assert summary["native_session_id"] == CLAUDE_SESSION_ID
            assert summary["served_model"] == "claude-fable-5-1"
            assert "Claude report" in (output_dir / "claude.result.md").read_text()

    def test_claude_process_failure_stays_failed_with_current_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root, "claude", create_fake_claude(root, exit_code=7)
            )
            assert completed.returncode == 1
            summary = read_summary(output_dir)
            assert summary["state"] == "failed"
            assert summary["failure_reason"] == "process_error"
            assert summary["native_session_id"] == CLAUDE_SESSION_ID
            assert summary["served_model"] == "claude-fable-5-1"
            assert summary["error_excerpt"] == "authentication failed"

    def test_claude_success_requires_a_native_session_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "claude",
                create_fake_claude(root, include_session=False),
            )
            assert completed.returncode == 1
            summary = read_summary(output_dir)
            assert summary["failure_reason"] == "missing_session_id"

    def test_claude_resume_requires_the_same_native_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first, first_output = run_launcher(
                root, "claude", create_fake_claude(root)
            )
            assert first.returncode == 0, first.stderr
            shutil.rmtree(first_output)
            second, second_output = run_launcher(
                root,
                "claude",
                create_fake_claude(root, expected_resume=CLAUDE_SESSION_ID),
                extra_arguments=("--resume", CLAUDE_SESSION_ID),
            )
            assert second.returncode == 0, second.stderr
            summary = read_summary(second_output)
            assert summary["native_session_id"] == CLAUDE_SESSION_ID
            assert summary["resumed_from"] == CLAUDE_SESSION_ID

    def test_codex_success_reports_read_only_flags_and_fast_tier(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "codex",
                create_fake_codex(root),
                model="gpt-5.6-luna",
                effort="low",
                extra_arguments=("--fast",),
            )
            assert completed.returncode == 0, completed.stderr
            summary = read_summary(output_dir)
            assert summary["provider"] == "codex"
            assert summary["native_session_id"] == CODEX_THREAD_ID
            assert summary["served_model"] == "gpt-5.6-luna"
            assert summary["served_effort"] == "low"
            assert summary["fast"] is True
            assert summary["served_service_tier"] is None
            assert "Codex report" in (output_dir / "codex.result.md").read_text()

    def test_codex_resume_uses_requested_properties_and_appended_rollout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first, first_output = run_launcher(
                root,
                "codex",
                create_fake_codex(root),
                model="gpt-5.6-sol",
                effort="xhigh",
            )
            assert first.returncode == 0, first.stderr
            shutil.rmtree(first_output)
            second, second_output = run_launcher(
                root,
                "codex",
                create_fake_codex(root),
                model="gpt-5.6-luna",
                effort="low",
                extra_arguments=("--resume", CODEX_THREAD_ID),
            )
            assert second.returncode == 0, second.stderr
            summary = read_summary(second_output)
            assert summary["native_session_id"] == CODEX_THREAD_ID
            assert summary["resumed_from"] == CODEX_THREAD_ID
            assert summary["requested_model"] == "gpt-5.6-luna"
            assert summary["served_model"] == "gpt-5.6-luna"
            assert summary["effort"] == "low"
            assert summary["served_effort"] == "low"
            rollout = (second_output / "codex.rollout.jsonl").read_text()
            assert "gpt-5.6-sol" in rollout
            assert "gpt-5.6-luna" in rollout

    def test_codex_resume_rejects_a_fresh_native_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first, first_output = run_launcher(
                root, "codex", create_fake_codex(root)
            )
            assert first.returncode == 0, first.stderr
            second, output_dir = run_launcher(
                root,
                "codex",
                create_fake_codex(root, thread_id="different-thread"),
                extra_arguments=("--resume", CODEX_THREAD_ID),
            )
            assert second.returncode == 1
            summary = read_summary(output_dir)
            assert summary["failure_reason"] == "session_id_mismatch"
            assert summary["native_session_id"] == CODEX_THREAD_ID

    def test_codex_resume_rejects_rollout_without_a_new_turn_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first, first_output = run_launcher(
                root, "codex", create_fake_codex(root)
            )
            assert first.returncode == 0, first.stderr
            second, output_dir = run_launcher(
                root,
                "codex",
                create_fake_codex(root, write_current_context=False),
                extra_arguments=("--resume", CODEX_THREAD_ID),
            )
            assert second.returncode == 1
            assert read_summary(output_dir)["failure_reason"] == "unverified_model"

    def test_output_override_rejects_reuse_without_touching_first_turn(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / "output"
            first, _ = run_launcher(
                root, "codex", create_fake_codex(root), output_dir=output
            )
            assert first.returncode == 0, first.stderr
            before = (output / "codex.result.md").read_text()
            second, _ = run_launcher(
                root, "codex", create_fake_codex(root), output_dir=output
            )
            assert second.returncode == 1
            assert "Output directory already exists" in second.stderr
            assert (output / "codex.result.md").read_text() == before

    def test_default_turns_use_separate_temporary_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first, first_output = run_launcher(root, "codex", create_fake_codex(root))
            second, second_output = run_launcher(root, "codex", create_fake_codex(root))
            assert first.returncode == 0, first.stderr
            assert second.returncode == 0, second.stderr
            assert first_output != second_output
            for output in (first_output, second_output):
                assert output.parent == root.resolve()
                assert output.name.startswith("mstack-consult-")
            event = json.loads(second.stdout.splitlines()[-1])
            assert event["native_session_id"] == CODEX_THREAD_ID

    def test_rejects_artifacts_inside_the_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, _ = run_launcher(
                root,
                "codex",
                create_fake_codex(root),
                output_dir=root / "workspace" / "output",
            )
            assert completed.returncode == 1
            assert "outside the working directory" in completed.stderr

    def test_default_artifacts_cannot_fall_inside_the_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            workspace = root / "workspace"
            workspace.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("analyze this", encoding="utf-8")
            environment = os.environ.copy()
            environment["TMPDIR"] = str(workspace)
            completed = invoke(
                root, "codex", create_fake_codex(root), workspace, prompt,
                environment=environment,
            )
            assert completed.returncode == 1
            assert "outside the working directory" in completed.stderr
            assert not list(workspace.iterdir())

    def test_activity_progress_is_redacted_while_raw_events_are_retained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "claude",
                create_fake_claude(root, with_activity=True),
            )
            assert completed.returncode == 0, completed.stderr
            assert "super-secret" not in completed.stdout
            assert "sensitive-name.txt" not in completed.stdout
            raw = (output_dir / "claude.events.jsonl").read_text()
            assert "super-secret" in raw
            assert "sensitive-name.txt" in raw
            progress = (output_dir / "claude.progress.log").read_text()
            assert "Reading src/auth.py" in progress
            assert "Running a read-only shell command" in progress
            assert "Reading an external file" in progress
            assert "super-secret" not in progress
            assert "sensitive-name.txt" not in progress

    def test_large_prompt_and_output_do_not_deadlock(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "claude",
                create_fake_claude(root, pre_read_stdout_bytes=200_000),
                prompt_prefix_bytes=200_000,
            )
            assert completed.returncode == 0, completed.stderr
            assert '"payload": "' in (output_dir / "claude.events.jsonl").read_text()

    def test_descendant_stdout_is_bounded_by_output_drain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "claude",
                create_fake_claude(root, child_stdout_seconds=5),
            )
            assert completed.returncode == 0, completed.stderr
            events = [json.loads(line) for line in completed.stdout.splitlines()]
            assert any(event.get("event") == "output_drain_ended" for event in events)
            assert read_summary(output_dir)["state"] == "succeeded"

    def test_timeout_persists_a_failed_turn(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                "claude",
                create_fake_claude(root, delay_seconds=5),
                extra_arguments=("--timeout-seconds", "1"),
            )
            assert completed.returncode == 1
            events = [json.loads(line) for line in completed.stdout.splitlines()]
            assert any(event.get("event") == "timed_out" for event in events)
            assert read_summary(output_dir)["failure_reason"] == "timeout"

    def test_interrupt_persists_a_resumable_native_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            prompt = root / "interrupt-prompt.md"
            prompt.write_text("analyze this", encoding="utf-8")
            workspace = root / "workspace"
            workspace.mkdir()
            output = root / "interrupt-output"
            binary = create_fake_claude(root, delay_seconds=5)
            environment = os.environ.copy()
            environment["CLAUDE_CODE_BIN"] = str(binary)
            environment["CODEX_HOME"] = str(root / "codex-home")
            process = subprocess.Popen(
                launcher_command(
                    "claude", workspace, prompt, output, "claude-fable-5-1", "low", ()
                ),
                cwd=root,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            time.sleep(0.5)
            process.send_signal(signal.SIGINT)
            stdout, stderr = process.communicate(timeout=8)
            assert process.returncode == 1, (stdout, stderr)
            summary = read_summary(output)
            assert summary["failure_reason"] == "interrupted"
            assert summary["native_session_id"] == CLAUDE_SESSION_ID

    def test_missing_binary_does_not_fallback_and_writes_failure_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            output = root / "output"
            completed, _ = run_launcher(
                root,
                "codex",
                root / "missing-codex",
                output_dir=output,
            )
            assert completed.returncode == 1
            assert "Required executable not found" in completed.stderr
            summary = read_summary(output)
            assert summary["failure_reason"] == (
                "Required executable not found: " + str(root / "missing-codex")
            )


def run_launcher(
    root: Path,
    provider: str,
    binary: Path,
    *,
    output_dir: Path | None = None,
    extra_arguments: tuple[str, ...] = (),
    model: str = "gpt-5.6-luna",
    effort: str = "low",
    prompt_prefix_bytes: int = 0,
) -> tuple[subprocess.CompletedProcess[str], Path]:
    prompt = root / f"{provider}-prompt.md"
    prompt.write_text("x" * prompt_prefix_bytes + "analyze this", encoding="utf-8")
    workspace = root / "workspace"
    workspace.mkdir(exist_ok=True)
    actual_output = output_dir
    environment = os.environ.copy()
    environment["CLAUDE_CODE_BIN"] = str(binary)
    environment["CODEX_BIN"] = str(binary)
    environment["CODEX_HOME"] = str(root / "codex-home")
    environment["TMPDIR"] = str(root)
    completed = invoke(
        root,
        provider,
        binary,
        workspace,
        prompt,
        output_dir=actual_output,
        extra_arguments=extra_arguments,
        model=model if provider == "codex" else "claude-fable-5-1",
        effort=effort,
        environment=environment,
    )
    if actual_output is None:
        summary_event = json.loads(completed.stdout.splitlines()[-1])
        actual_output = Path(summary_event["summary"]).parent
    return completed, actual_output


def invoke(
    root: Path,
    provider: str,
    binary: Path,
    workspace: Path,
    prompt: Path,
    *,
    output_dir: Path | None = None,
    extra_arguments: tuple[str, ...] = (),
    model: str = "gpt-5.6-luna",
    effort: str = "low",
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        launcher_command(provider, workspace, prompt, output_dir, model, effort, extra_arguments),
        capture_output=True,
        text=True,
        env=environment or os.environ.copy(),
        check=False,
        timeout=20,
    )


def launcher_command(
    provider: str,
    workspace: Path,
    prompt: Path,
    output_dir: Path | None,
    model: str,
    effort: str,
    extra_arguments: tuple[str, ...],
) -> list[str]:
    command = [
        sys.executable,
        str(RUNNER),
        "--provider",
        provider,
        "--cwd",
        str(workspace),
        "--prompt-file",
        str(prompt),
        "--model",
        model,
        "--effort",
        effort,
    ]
    if output_dir is not None:
        command.extend(("--output-dir", str(output_dir)))
    command.extend(extra_arguments)
    return command


def read_summary(output_dir: Path) -> dict[str, JsonValue]:
    return json.loads((output_dir / "summary.json").read_text())


def create_fake_claude(
    root: Path,
    exit_code: int = 0,
    expected_resume: str | None = None,
    with_activity: bool = False,
    pre_read_stdout_bytes: int = 0,
    child_stdout_seconds: int = 0,
    delay_seconds: int = 0,
    include_session: bool = True,
) -> Path:
    body = f"""
        #!{sys.executable}
        import json
        import os
        import subprocess
        import sys
        import time
        args = sys.argv[1:]
        assert args[args.index("--model") + 1] == "claude-fable-5-1"
        assert args[args.index("--effort") + 1] == "low"
        assert "--no-session-persistence" not in args
        assert args[args.index("--output-format") + 1] == "stream-json"
        assert os.environ.get("CLAUDE_CODE_DISABLE_AUTO_MEMORY") == "1"
        if {expected_resume!r} is None:
            assert "--resume" not in args
        else:
            assert args[args.index("--resume") + 1] == {expected_resume!r}
        if {child_stdout_seconds}:
            subprocess.Popen([sys.executable, "-c", "import time; time.sleep({child_stdout_seconds})"])
        if {pre_read_stdout_bytes}:
            print(json.dumps({{"type": "system", "payload": "x" * {pre_read_stdout_bytes}}}), flush=True)
        prompt = sys.stdin.read()
        assert "Act only as an independent consultant" in prompt
        assert prompt.endswith("analyze this")
        if {include_session}:
            print(json.dumps({{"type": "system", "session_id": {CLAUDE_SESSION_ID!r}}}), flush=True)
        print(json.dumps({{"type": "assistant", "message": {{"model": "claude-fable-5-1", "content": [
            {{"type": "tool_use", "name": "Read", "input": {{"file_path": "src/auth.py"}}}},
            {{"type": "tool_use", "name": "Bash", "input": {{"command": "echo super-secret"}}}},
            {{"type": "tool_use", "name": "Read", "input": {{"file_path": "/outside/sensitive-name.txt"}}}},
        ] if {with_activity} else []}}}}), flush=True)
        time.sleep({delay_seconds})
        if {exit_code} == 0:
            print(json.dumps({{"type": "result", "subtype": "success", "result": "## Analysis\\n\\nClaude report"}}), flush=True)
        else:
            print("authentication failed", file=sys.stderr)
        raise SystemExit({exit_code})
    """
    return write_executable(root / "claude-fake", body)


def create_fake_codex(
    root: Path,
    *,
    thread_id: str = CODEX_THREAD_ID,
    exit_code: int = 0,
    write_current_context: bool = True,
) -> Path:
    body = f"""
        #!{sys.executable}
        import json
        import os
        import sys
        from pathlib import Path
        args = sys.argv[1:]
        resumed = "resume" in args
        if not resumed:
            assert args[0] == "exec"
        else:
            assert args[0:4] == ["--sandbox", "read-only", "--cd", {str((root / "workspace").resolve())!r}]
            assert args[args.index("exec") + 1] == "resume"
            assert args[args.index("resume") + 1] == "--json"
            assert args[args.index("--sandbox") + 1] == "read-only"
            assert args[args.index("--cd") + 1] == {str((root / "workspace").resolve())!r}
            assert args[args.index("resume") + 3] == {CODEX_THREAD_ID!r}
        assert args[args.index("--model") + 1] in {{"gpt-5.6-sol", "gpt-5.6-luna"}}
        model = args[args.index("--model") + 1]
        configs = [args[index + 1] for index, value in enumerate(args) if value == "--config"]
        effort = next(value.split("=", 1)[1].strip('\\"') for value in configs if value.startswith("model_reasoning_effort="))
        tier = next(value.split("=", 1)[1].strip('\\"') for value in configs if value.startswith("service_tier="))
        assert tier in {{"default", "fast"}}
        assert args[-1] == "-"
        prompt = sys.stdin.read()
        assert "Act only as an independent consultant" in prompt
        print(json.dumps({{"type": "thread.started", "thread_id": {thread_id!r}}}), flush=True)
        print(json.dumps({{"type": "turn.started", "turn_id": {CODEX_TURN_ID!r}}}), flush=True)
        print(json.dumps({{"type": "item.started", "item": {{"type": "command_execution"}}}}), flush=True)
        print(json.dumps({{"type": "item.completed", "turn_id": {CODEX_TURN_ID!r}, "item": {{"type": "agent_message", "text": "## Analysis\\n\\nCodex report"}}}}), flush=True)
        if {exit_code} != 0:
            print("quota exceeded", file=sys.stderr)
            raise SystemExit({exit_code})
        sessions = Path(os.environ["CODEX_HOME"]) / "sessions" / "2026" / "09" / "12"
        sessions.mkdir(parents=True, exist_ok=True)
        rollout = sessions / ("rollout-2026-09-12T00-00-00-" + {CODEX_THREAD_ID!r} + ".jsonl")
        old_context = {{"type": "turn_context", "payload": {{"model": "gpt-5.6-sol", "effort": "xhigh", "turn_id": "old-turn"}}}}
        current_context = {{"type": "turn_context", "payload": {{"model": model, "effort": effort, "turn_id": {CODEX_TURN_ID!r}}}}}
        if resumed:
            with rollout.open("a", encoding="utf-8") as stream:
                stream.write("\\n" + json.dumps(old_context) + ("\\n" + json.dumps(current_context) if {write_current_context} else "") + "\\n")
        else:
            rollout.write_text(json.dumps(current_context) + "\\n")
        raise SystemExit(0)
    """
    return write_executable(root / "codex-fake", body)


def write_executable(path: Path, body: str) -> Path:
    path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")
    path.chmod(0o700)
    return path


if __name__ == "__main__":
    unittest.main()
