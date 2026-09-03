from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

RUNNER = Path(__file__).with_name("run_claude.py")


class RunClaudeTest(unittest.TestCase):
    def test_extracts_a_successful_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(root, create_fake_claude(root))
            assert completed.returncode == 0, completed.stderr
            assert "Claude report" in (output_dir / "claude.result.md").read_text()
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "succeeded"
            assert summary["effort"] == "xhigh"
            assert summary["requested_model"] == "claude-fable-5-1"
            assert summary["served_model"] == "claude-fable-5-1"

    def test_prepends_the_consultant_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, _ = run_launcher(root, create_fake_claude(root))
            assert completed.returncode == 0, completed.stderr

    def test_surfaces_sanitized_tool_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(root, create_fake_claude(root))
            assert completed.returncode == 0, completed.stderr
            progress = [
                json.loads(line)
                for line in completed.stdout.splitlines()
                if json.loads(line).get("event") == "claude.activity"
            ]
            assert [event["activity"] for event in progress] == [
                "Reading src/auth.py",
                "Running a read-only shell command",
                "Reading an external file",
            ]
            assert [event["tool_calls"] for event in progress] == [1, 2, 3]
            assert [event["tool"] for event in progress] == ["Read", "Bash", "Read"]
            assert "super-secret" not in completed.stdout
            assert "sensitive-name.txt" not in completed.stdout
            raw_output = (output_dir / "claude.events.jsonl").read_text()
            assert "src/auth.py" in raw_output
            assert "super-secret" in raw_output
            assert "sensitive-name.txt" in raw_output
            progress_output = (output_dir / "claude.progress.log").read_text()
            assert "Claude started" in progress_output
            assert "Reading src/auth.py" in progress_output
            assert "Running a read-only shell command" in progress_output
            assert "Reading an external file" in progress_output
            assert "Completed with exit code 0" in progress_output
            assert "super-secret" not in progress_output
            assert "sensitive-name.txt" not in progress_output
            summary = json.loads((output_dir / "summary.json").read_text())
            assert (
                Path(summary["progress_file"]).resolve()
                == (output_dir / "claude.progress.log").resolve()
            )

    def test_preserves_a_failed_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root, create_fake_claude(root, exit_code=7)
            )
            assert completed.returncode == 1
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "failed"
            assert summary["failure_reason"] == "process_error"
            assert summary["error_excerpt"] == "authentication failed"
            assert (
                "authentication failed" in (output_dir / "claude.stderr.log").read_text()
            )

    def test_rejects_unverified_model_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            claude = create_fake_claude(root, include_model=False)
            completed, output_dir = run_launcher(root, claude)
            assert completed.returncode == 1
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["served_model"] is None
            assert summary["failure_reason"] == "unverified_model"

    def test_accepts_a_matching_model_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            claude = create_fake_claude(
                root,
                expected_model="haiku",
                expected_effort="low",
                served_model="claude-haiku-4-5-20251001",
            )
            completed, output_dir = run_launcher(
                root, claude, model="haiku", effort="low"
            )
            assert completed.returncode == 0, completed.stderr
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["requested_model"] == "haiku"
            assert summary["served_model"] == "claude-haiku-4-5-20251001"
            assert summary["effort"] == "low"

    def test_rejects_artifacts_inside_the_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, _ = run_launcher(
                root, create_fake_claude(root), output_inside_workspace=True
            )
            assert completed.returncode != 0
            assert "outside the working directory" in completed.stderr

    def test_rejects_a_negative_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, _ = run_launcher(
                root,
                create_fake_claude(root),
                extra_arguments=("--timeout-seconds", "-1"),
            )
            assert completed.returncode != 0
            assert "Timeout cannot be negative" in completed.stderr

    def test_stops_a_timed_out_stream_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                create_fake_claude(root, delay_seconds=5),
                extra_arguments=("--timeout-seconds", "1"),
            )
            assert completed.returncode == 1
            events = [json.loads(line) for line in completed.stdout.splitlines()]
            assert any(event.get("event") == "timed_out" for event in events)
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["failure_reason"] == "timeout"

    def test_does_not_wait_for_a_grandchild_holding_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                create_fake_claude(root, child_stdout_seconds=5),
                launcher_timeout_seconds=4,
            )
            assert completed.returncode == 0, completed.stderr
            events = [json.loads(line) for line in completed.stdout.splitlines()]
            assert any(event.get("event") == "output_drain_ended" for event in events)
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "succeeded"

    def test_drains_stdout_while_writing_a_large_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            completed, output_dir = run_launcher(
                root,
                create_fake_claude(root, pre_read_stdout_bytes=200_000),
                prompt_prefix_bytes=200_000,
                launcher_timeout_seconds=5,
            )
            assert completed.returncode == 0, completed.stderr
            raw_output = (output_dir / "claude.events.jsonl").read_text()
            assert '"payload": "' in raw_output
            summary = json.loads((output_dir / "summary.json").read_text())
            assert summary["state"] == "succeeded"


def run_launcher(
    root: Path,
    claude: Path,
    *,
    output_inside_workspace: bool = False,
    extra_arguments: tuple[str, ...] = (),
    prompt_prefix_bytes: int = 0,
    launcher_timeout_seconds: int = 20,
    model: str = "claude-fable-5-1",
    effort: str = "xhigh",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    prompt = root / "prompt.md"
    prompt.write_text("x" * prompt_prefix_bytes + "analyze this", encoding="utf-8")
    workspace = root / "workspace"
    workspace.mkdir()
    output_dir = workspace / "output" if output_inside_workspace else root / "output"
    environment = os.environ.copy()
    environment["CLAUDE_CODE_BIN"] = str(claude)
    codex_root = root / "codex"
    (codex_root / "skills").mkdir(parents=True)
    environment["CODEX_HOME"] = str(codex_root)
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


def create_fake_claude(
    root: Path,
    exit_code: int = 0,
    *,
    include_model: bool = True,
    expected_model: str = "claude-fable-5-1",
    expected_effort: str = "xhigh",
    served_model: str | None = None,
    delay_seconds: int = 0,
    child_stdout_seconds: int = 0,
    pre_read_stdout_bytes: int = 0,
) -> Path:
    body = f"""
        #!{sys.executable}
        import json
        import subprocess
        import sys
        import time
        args = sys.argv[1:]
        assert args[args.index("--model") + 1] == {expected_model!r}
        assert args[args.index("--effort") + 1] == {expected_effort!r}
        assert args[args.index("--permission-mode") + 1] == "auto"
        assert args[args.index("--tools") + 1] == "default"
        assert args[args.index("--add-dir") + 1].endswith("/codex/skills")
        assert args[args.index("--output-format") + 1] == "stream-json"
        assert "--verbose" in args
        assert "--safe-mode" not in args
        assert "--no-session-persistence" in args
        if {child_stdout_seconds}:
            subprocess.Popen([
                sys.executable,
                "-c",
                "import time; time.sleep({child_stdout_seconds})",
            ])
        if {pre_read_stdout_bytes}:
            print(json.dumps({{
                "type": "system",
                "payload": "x" * {pre_read_stdout_bytes},
            }}), flush=True)
        prompt = sys.stdin.read()
        assert "Act only as an independent consultant" in prompt
        assert "do not change state" in prompt
        assert 'include a "Capability and Tool Issues" section' in prompt
        assert "silently treat that source as searched" in prompt
        assert "Redact credentials and other secrets" in prompt
        assert prompt.endswith("analyze this")
        time.sleep({delay_seconds})
        if {exit_code} == 0:
            served_model = {served_model or expected_model!r} if {include_model} else "claude-opus-5"
            print(json.dumps({{
                "type": "assistant",
                "message": {{
                    "model": served_model,
                    "content": [
                        {{
                            "type": "tool_use",
                            "name": "Read",
                            "input": {{"file_path": "src/auth.py"}},
                        }},
                        {{
                            "type": "tool_use",
                            "name": "Bash",
                            "input": {{"command": "echo super-secret"}},
                        }},
                        {{
                            "type": "tool_use",
                            "name": "Read",
                            "input": {{"file_path": "/outside/sensitive-name.txt"}},
                        }},
                    ],
                }},
            }}))
            print(json.dumps({{
                "type": "result",
                "subtype": "success",
                "result": "## Analysis\\n\\nClaude report",
            }}))
        else:
            print("authentication failed", file=sys.stderr)
        raise SystemExit({exit_code})
    """
    return write_executable(root / "claude-fake", body)


def write_executable(path: Path, body: str) -> Path:
    path.write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")
    path.chmod(0o700)
    return path


if __name__ == "__main__":
    unittest.main()
