from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("models.py")


class ModelsTest(unittest.TestCase):
    def run_models(
        self, *arguments: str, expected_code: int = 0, **host_environment: str
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.pop("MSTACK_CONFIG", None)
        environment.pop("XDG_CONFIG_HOME", None)
        environment.pop("MSTACK_HOST", None)
        environment.pop("CLAUDECODE", None)
        environment.update(host_environment)
        result = subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertEqual(expected_code, result.returncode, result.stderr)
        return result

    def test_every_profile_resolves(self) -> None:
        for profile in ("codex-multimodel", "claude-multimodel"):
            result = self.run_models("resolve", "--profile", profile, "--no-user-config")
            self.assertIn(f'"profile": "{profile}"', result.stdout)

    def test_codex_host_defaults_to_codex_multimodel(self) -> None:
        result = self.run_models("resolve", "--role", "implement_worker", "--no-user-config")
        self.assertIn('"host": "codex"', result.stdout)
        self.assertIn('"profile": "codex-multimodel"', result.stdout)
        self.assertIn('"model": "gpt-5.6-luna"', result.stdout)
        self.assertIn('"effort": "high"', result.stdout)
        self.assertIn('"fast": true', result.stdout)

    def test_claude_code_host_defaults_to_claude_multimodel(self) -> None:
        result = self.run_models(
            "resolve", "--role", "interrogate_reviewer_b", "--no-user-config", CLAUDECODE="1"
        )
        self.assertIn('"host": "claude-code"', result.stdout)
        self.assertIn('"profile": "claude-multimodel"', result.stdout)
        self.assertIn('"runner": "codex"', result.stdout)
        self.assertIn('"model": "gpt-5.6-sol"', result.stdout)
        self.assertIn('"effort": "max"', result.stdout)

    def test_explicit_host_overrides_detection(self) -> None:
        result = self.run_models("resolve", "--no-user-config", MSTACK_HOST="codex", CLAUDECODE="1")
        self.assertIn('"profile": "codex-multimodel"', result.stdout)
        result = self.run_models("resolve", "--no-user-config", MSTACK_HOST="other", expected_code=2)
        self.assertIn("MSTACK_HOST", result.stderr)

    def test_user_profile_wins_over_host_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text('schema_version = 1\nprofile = "codex-multimodel"\n', encoding="utf-8")
            result = self.run_models("resolve", "--config", str(config), CLAUDECODE="1")
            self.assertIn('"profile": "codex-multimodel"', result.stdout)

    def test_profiles_marks_the_host_default(self) -> None:
        result = self.run_models("profiles", CLAUDECODE="1")
        self.assertIn("host: claude-code", result.stdout)
        self.assertIn("claude-multimodel\t", result.stdout)
        self.assertIn("(default for this host)", result.stdout)

    def test_user_override_changes_only_named_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\nprofile = "codex-multimodel"\n\n[roles.how_simple_explainer]\neffort = "low"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--role", "how_simple_explainer", "--config", str(config))
            self.assertIn('"model": "gpt-5.6-sol"', result.stdout)
            self.assertIn('"effort": "low"', result.stdout)

    def test_unknown_user_role_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\nprofile = "codex-multimodel"\n\n[roles.unknown]\nmodel = "x"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("unknown roles", result.stderr)

    def test_configure_writes_resolvable_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            self.run_models(
                "configure",
                "--profile",
                "claude-multimodel",
                "--set",
                "why_synthesizer.effort=medium",
                "--output",
                str(config),
            )
            result = self.run_models("resolve", "--role", "why_synthesizer", "--config", str(config))
            self.assertIn('"profile": "claude-multimodel"', result.stdout)
            self.assertIn('"effort": "medium"', result.stdout)

    def test_fast_rejected_for_claude_runners(self) -> None:
        result = self.run_models(
            "configure",
            "--profile",
            "claude-multimodel",
            "--set",
            "implement_worker.fast=true",
            "--dry-run",
            expected_code=2,
        )
        self.assertIn("supported only by codex-native or codex", result.stderr)

    def test_external_runner_rejected_for_implement_worker(self) -> None:
        result = self.run_models(
            "configure",
            "--profile",
            "claude-multimodel",
            "--set",
            "implement_worker.runner=codex",
            "--dry-run",
            expected_code=2,
        )
        self.assertIn("must be a native runner", result.stderr)

    def test_fast_accepted_for_external_codex_runner(self) -> None:
        result = self.run_models(
            "configure",
            "--profile",
            "claude-multimodel",
            "--set",
            "consultant_default.fast=true",
            "--dry-run",
        )
        self.assertIn("fast = true", result.stdout)


if __name__ == "__main__":
    unittest.main()

