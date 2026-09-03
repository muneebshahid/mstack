from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("models.py")


class ModelsTest(unittest.TestCase):
    def run_models(self, *arguments: str, expected_code: int = 0) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.pop("MSTACK_CONFIG", None)
        environment.pop("XDG_CONFIG_HOME", None)
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
        for profile in ("multimodel", "codex", "claude-code"):
            result = self.run_models("resolve", "--profile", profile, "--no-user-config")
            self.assertIn(f'"profile": "{profile}"', result.stdout)

    def test_default_profile_preserves_implementation_worker(self) -> None:
        result = self.run_models("resolve", "--role", "implement_worker", "--no-user-config")
        self.assertIn('"model": "gpt-5.6-luna"', result.stdout)
        self.assertIn('"effort": "high"', result.stdout)
        self.assertIn('"fast": true', result.stdout)

    def test_user_override_changes_only_named_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\nprofile = "multimodel"\n\n[roles.how_simple_explainer]\neffort = "low"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--role", "how_simple_explainer", "--config", str(config))
            self.assertIn('"model": "gpt-5.6-sol"', result.stdout)
            self.assertIn('"effort": "low"', result.stdout)

    def test_unknown_user_role_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\nprofile = "multimodel"\n\n[roles.unknown]\nmodel = "x"\n',
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
                "codex",
                "--set",
                "why_synthesizer.effort=medium",
                "--output",
                str(config),
            )
            result = self.run_models("resolve", "--role", "why_synthesizer", "--config", str(config))
            self.assertIn('"profile": "codex"', result.stdout)
            self.assertIn('"effort": "medium"', result.stdout)

    def test_fast_rejected_for_non_codex_runner(self) -> None:
        result = self.run_models(
            "configure",
            "--profile",
            "claude-code",
            "--set",
            "implement_worker.fast=true",
            "--dry-run",
            expected_code=2,
        )
        self.assertIn("supported only by codex-native", result.stderr)


if __name__ == "__main__":
    unittest.main()

