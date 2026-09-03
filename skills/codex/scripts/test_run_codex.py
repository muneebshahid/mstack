from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

RUNNER = Path(__file__).with_name("run_codex.py")
THREAD_ID = "01a068d6-0000-7000-8000-000000000001"


class RunCodexTest(unittest.TestCase):
    def test_extracts_a_successful_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(root, create_fake_codex(root))
            assert completed.returncode == 0, completed.stderr
            assert "Codex report" in (output_dir / "codex.result.md").read_text()
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "succeeded"
            assert summary["effort"] == "xhigh"
            assert summary["served_effort"] == "xhigh"
            assert summary["requested_model"] == "gpt-5.6-sol"
            assert summary["served_model"] == "gpt-5.6-sol"
            assert summary["thread_id"] == THREAD_ID
            assert summary["fast"] is False
            assert Path(summary["rollout_file"]).is_file()

    def test_requests_the_fast_tier_when_asked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex = create_fake_codex(
                root, expected_model="gpt-5.6-luna", expected_effort="low", expected_tier="fast"
            )
            completed, output_dir = run_launcher(
                root, codex, model="gpt-5.6-luna", effort="low", extra_arguments=("--fast",)
            )
            assert completed.returncode == 0, completed.stderr
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["fast"] is True
            assert summary["served_service_tier"] is None

    def test_surfaces_sanitized_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(root, create_fake_codex(root))
            assert completed.returncode == 0, completed.stderr
            progress = [
                json.loads(line)
                for line in completed.stdout.splitlines()
                if json.loads(line).get("event") == "codex.activity"
            ]
            assert [event["activity"] for event in progress] == [
                "Running a read-only shell command",
                "Using linear get issue",
            ]
            assert [event["tool_calls"] for event in progress] == [1, 2]
            assert "super-secret" not in completed.stdout
            assert "super-secret" in (output_dir / "codex.events.jsonl").read_text()
            progress_output = (output_dir / "codex.progress.log").read_text()
            assert "Codex started" in progress_output
            assert "Completed with exit code 0" in progress_output
            assert "super-secret" not in progress_output

    def test_preserves_a_failed_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(root, create_fake_codex(root, exit_code=7))
            assert completed.returncode == 1
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "failed"
            assert summary["failure_reason"] == "process_error"
            assert summary["error_excerpt"] == "authentication failed"

    def test_rejects_a_served_model_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex = create_fake_codex(root, served_model="gpt-5.5")
            completed, output_dir = run_launcher(root, codex)
            assert completed.returncode == 1
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["failure_reason"] == "unverified_model"
            assert summary["served_model"] == "gpt-5.5"
            assert summary["state"] == "failed"

    def test_rejects_a_missing_rollout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            codex = create_fake_codex(root, write_rollout=False)
            completed, output_dir = run_launcher(root, codex, launcher_timeout_seconds=30)
            assert completed.returncode == 1
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["failure_reason"] == "missing_rollout"
            assert summary["thread_id"] == THREAD_ID

    def test_rejects_artifacts_inside_the_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, _ = run_launcher(
                root, create_fake_codex(root), output_inside_workspace=True
            )
            assert completed.returncode != 0
            assert "outside the working directory" in completed.stderr

    def test_stops_a_timed_out_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                create_fake_codex(root, delay_seconds=5),
                extra_arguments=("--timeout-seconds", "1"),
            )
            assert completed.returncode == 1
            events = [json.loads(line) for line in completed.stdout.splitlines()]
            assert any(event.get("event") == "timed_out" for event in events)
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["failure_reason"] == "timeout"


def run_launcher(
    root: Path,
    codex: Path,
    *,
    output_inside_workspace: bool = False,
    extra_arguments: tuple[str, ...] = (),
    launcher_timeout_seconds: int = 20,
    model: str = "gpt-5.6-sol",
    effort: str = "xhigh",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    prompt = root / "prompt.md"
    prompt.write_text("analyze this", encoding="utf-8")
    workspace = root / "workspace"
    workspace.mkdir(exist_ok=True)
    output_dir = workspace / "output" if output_inside_workspace else root / "output"
    environment = os.environ.copy()
    environment["CODEX_BIN"] = str(codex)
    environment["CODEX_HOME"] = str(root / "codex-home")
    command = [
        sys.executable,
        str(RUNNER),
        "--cwd",
        str(workspace),
        "--prompt-file",
        str(prompt),
        "--output-dir",
        str(output_dir),
        "--model",
        model,
        "--effort",
        effort,
        *extra_arguments,
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=environment,
        check=False,
        timeout=launcher_timeout_seconds,
    )
    return completed, output_dir


def create_fake_codex(
    root: Path,
    exit_code: int = 0,
    *,
    expected_model: str = "gpt-5.6-sol",
    expected_effort: str = "xhigh",
    expected_tier: str = "default",
    served_model: str | None = None,
    write_rollout: bool = True,
    delay_seconds: int = 0,
) -> Path:
    body = f"""
        #!{sys.executable}
        import json
        import os
        import sys
        import time
        from pathlib import Path
        args = sys.argv[1:]
        assert args[0] == "exec"
        assert "--json" in args
        assert "--skip-git-repo-check" in args
        assert args[args.index("--sandbox") + 1] == "read-only"
        assert args[args.index("--model") + 1] == {expected_model!r}
        assert args[args.index("--cd") + 1] == {str((root / "workspace").resolve())!r}
        configs = [args[index + 1] for index, value in enumerate(args) if value == "--config"]
        assert 'model_reasoning_effort="{expected_effort}"' in configs
        assert 'service_tier="{expected_tier}"' in configs
        assert "--ephemeral" not in args
        assert args[-1] == "-"
        prompt = sys.stdin.read()
        assert "Act only as an independent consultant" in prompt
        assert 'include a "Capability and Tool Issues" section' in prompt
        assert prompt.endswith("analyze this")
        time.sleep({delay_seconds})
        if {exit_code} != 0:
            print("authentication failed", file=sys.stderr)
            raise SystemExit({exit_code})
        print(json.dumps({{"type": "thread.started", "thread_id": {THREAD_ID!r}}}), flush=True)
        print(json.dumps({{"type": "turn.started"}}), flush=True)
        print(json.dumps({{"type": "item.started", "item": {{"id": "item_1", "type": "command_execution", "command": "echo super-secret", "status": "in_progress"}}}}), flush=True)
        print(json.dumps({{"type": "item.completed", "item": {{"id": "item_1", "type": "command_execution", "command": "echo super-secret", "aggregated_output": "super-secret", "exit_code": 0, "status": "completed"}}}}), flush=True)
        print(json.dumps({{"type": "item.started", "item": {{"id": "item_2", "type": "mcp_tool_call", "server": "linear", "tool": "get_issue", "status": "in_progress"}}}}), flush=True)
        print(json.dumps({{"type": "item.completed", "item": {{"id": "item_3", "type": "agent_message", "text": "## Analysis\\n\\nCodex report"}}}}), flush=True)
        print(json.dumps({{"type": "turn.completed", "usage": {{"input_tokens": 1}}}}), flush=True)
        if {write_rollout}:
            sessions = Path(os.environ["CODEX_HOME"]) / "sessions" / "2026" / "09" / "03"
            sessions.mkdir(parents=True, exist_ok=True)
            rollout = sessions / ("rollout-2026-09-03T00-00-00-" + {THREAD_ID!r} + ".jsonl")
            lines = [
                {{"type": "session_meta", "payload": {{"id": {THREAD_ID!r}, "model_provider": "openai"}}}},
                {{"type": "turn_context", "payload": {{"model": {served_model or expected_model!r}, "effort": {expected_effort!r}}}}},
            ]
            rollout.write_text("\\n".join(json.dumps(line) for line in lines) + "\\n")
        raise SystemExit(0)
    """
    path = root / "codex-fake"
    path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")
    path.chmod(0o700)
    return path


if __name__ == "__main__":
    unittest.main()
