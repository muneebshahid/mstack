from __future__ import annotations

import json
import os
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("models.py")


class ModelsTest(unittest.TestCase):
    def run_models(
        self, *arguments: str, expected_code: int = 0, **environment_overrides: str
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment.pop("MSTACK_CONFIG", None)
        environment.pop("XDG_CONFIG_HOME", None)
        environment.pop("MSTACK_HOST", None)
        environment.pop("CLAUDECODE", None)
        environment.update(environment_overrides)
        result = subprocess.run(
            ["python3", str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        self.assertEqual(expected_code, result.returncode, result.stderr)
        return result

    def test_no_config_requires_setup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_models(
                "resolve",
                "--role",
                "implement_worker",
                expected_code=2,
                XDG_CONFIG_HOME=directory,
            )
            self.assertIn("No active profile; run setup-mstack", result.stderr)

    def test_explicit_presets_resolve_without_user_config(self) -> None:
        expected = {
            "codex-preset": {
                "implement_worker": {"model": "gpt-5.6-luna", "effort": "max", "fast": False},
                "explain_explorer": {"model": "gpt-5.6-luna", "effort": "max", "fast": False},
                "architect_candidate_a": {"model": "claude-fable-5-1", "effort": "xhigh", "fast": False},
                "architect_candidate_b": {"model": "gpt-6-astra", "effort": "xhigh", "fast": False},
                "review_reviewer_a": {"model": "claude-fable-5-1", "effort": "max", "fast": False},
                "review_reviewer_b": {"model": "gpt-6-astra", "effort": "max", "fast": False},
                "skill_eval_quality_judge": {"model": "gpt-6-astra", "effort": "medium", "fast": False},
                "skill_eval_smoke_candidate": {"model": "gpt-5.6-luna", "effort": "low", "fast": True},
                "skill_eval_smoke_judge": {"model": "gpt-5.6-luna", "effort": "low", "fast": True},
                "delegate_default": {"model": "claude-fable-5-1", "effort": "xhigh", "fast": False},
            },
            "claude-preset": {
                "implement_worker": {"model": "sonnet", "effort": "high", "fast": False},
                "explain_explorer": {"model": "sonnet", "effort": "high", "fast": False},
                "architect_candidate_a": {"model": "claude-fable-5-1", "effort": "xhigh", "fast": False},
                "architect_candidate_b": {"model": "gpt-6-astra", "effort": "xhigh", "fast": False},
                "review_reviewer_a": {"model": "claude-fable-5-1", "effort": "max", "fast": False},
                "review_reviewer_b": {"model": "gpt-6-astra", "effort": "max", "fast": False},
                "skill_eval_quality_judge": {"model": "claude-fable-5-1", "effort": "medium", "fast": False},
                "skill_eval_smoke_candidate": {"model": "haiku", "effort": "low", "fast": False},
                "skill_eval_smoke_judge": {"model": "haiku", "effort": "low", "fast": False},
                "delegate_default": {"model": "gpt-6-astra", "effort": "xhigh", "fast": False},
            },
        }
        for preset, assignments in expected.items():
            result = self.run_models("resolve", "--preset", preset, "--no-user-config")
            payload = json.loads(result.stdout)
            self.assertEqual(preset, payload["preset"])
            self.assertNotIn("host", payload)
            self.assertEqual(assignments, payload["roles"])

    def test_environment_does_not_select_preset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text('schema_version = 1\npreset = "codex-preset"\n', encoding="utf-8")
            detected = self.run_models("resolve", "--config", str(config))
            marked = self.run_models(
                "resolve",
                "--config",
                str(config),
                CLAUDECODE="1",
                MSTACK_HOST="claude-code",
            )
            self.assertEqual(json.loads(detected.stdout), json.loads(marked.stdout))

    def test_presets_are_host_independent_suggestions(self) -> None:
        plain = self.run_models("presets")
        marked = self.run_models("presets", CLAUDECODE="1", MSTACK_HOST="codex")
        self.assertEqual(plain.stdout, marked.stdout)
        self.assertIn("codex-preset\t", plain.stdout)
        self.assertIn("claude-preset\t", plain.stdout)
        self.assertNotIn("host:", plain.stdout)
        self.assertNotIn("default for this host", plain.stdout)

    def test_saved_preset_and_partial_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.architect_candidate_b]\n"
                'effort = "low"\n',
                encoding="utf-8",
            )
            result = self.run_models(
                "resolve", "--role", "architect_candidate_b", "--config", str(config)
            )
            payload = json.loads(result.stdout)
            self.assertEqual("codex-preset", payload["preset"])
            self.assertEqual(
                {"model": "gpt-6-astra", "effort": "low", "fast": False},
                payload["assignment"],
            )

    def test_explicit_preset_wins_and_keeps_saved_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.implement_worker]\n"
                'effort = "low"\n',
                encoding="utf-8",
            )
            result = self.run_models(
                "resolve",
                "--role",
                "implement_worker",
                "--preset",
                "claude-preset",
                "--config",
                str(config),
            )
            payload = json.loads(result.stdout)
            self.assertEqual("claude-preset", payload["preset"])
            self.assertEqual(
                {"model": "sonnet", "effort": "low", "fast": False},
                payload["assignment"],
            )

    def test_explicit_missing_config_fails_even_without_user_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.toml"
            result = self.run_models(
                "resolve",
                "--preset",
                "codex-preset",
                "--config",
                str(missing),
                "--no-user-config",
                expected_code=2,
            )
            self.assertIn(f"configuration file does not exist: {missing}", result.stderr)

    def test_legacy_profile_requires_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text('schema_version = 1\nprofile = "codex-multimodel"\n', encoding="utf-8")
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("replace profile with preset", result.stderr)
            self.assertIn("setup-mstack", result.stderr)

    def test_legacy_runner_requires_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.implement_worker]\n"
                'runner = "codex-native"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("runner", result.stderr)
            self.assertIn("setup-mstack", result.stderr)

    def test_legacy_delegate_role_requires_update(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.consultant_default]\n"
                'model = "claude-fable-5-1"\n'
                'effort = "xhigh"\n'
                "fast = false\n",
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("consultant_default", result.stderr)
            self.assertIn("delegate_default", result.stderr)
            self.assertIn("setup-mstack", result.stderr)

    def test_unknown_assignment_field_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.implement_worker]\n"
                'provider = "codex"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("unknown fields", result.stderr)

    def test_new_complete_role_resolves(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.new_skill]\n"
                'model = "gpt-new"\n'
                'effort = "high"\n'
                "fast = true\n",
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--role", "new_skill", "--config", str(config))
            payload = json.loads(result.stdout)
            self.assertEqual(
                {"model": "gpt-new", "effort": "high", "fast": True},
                payload["assignment"],
            )

    def test_new_role_must_be_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            config.write_text(
                'schema_version = 1\npreset = "codex-preset"\n\n'
                "[roles.new_skill]\n"
                'model = "gpt-new"\n',
                encoding="utf-8",
            )
            result = self.run_models("resolve", "--config", str(config), expected_code=2)
            self.assertIn("all assignment fields", result.stderr)
            self.assertIn("effort", result.stderr)
            self.assertIn("fast", result.stderr)

    def test_configure_writes_and_validates_overrides_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "models.toml"
            self.run_models(
                "configure",
                "--preset",
                "claude-preset",
                "--set",
                "delegate_default.effort=medium",
                "--set",
                "delegate_default.fast=true",
                "--output",
                str(config),
            )
            saved = tomllib.loads(config.read_text(encoding="utf-8"))
            self.assertEqual("claude-preset", saved["preset"])
            self.assertEqual("medium", saved["roles"]["delegate_default"]["effort"])
            self.assertTrue(saved["roles"]["delegate_default"]["fast"])
            self.assertNotIn("runner", config.read_text(encoding="utf-8"))
            self.assertEqual([config], list(Path(directory).iterdir()))
            result = self.run_models(
                "resolve", "--role", "delegate_default", "--config", str(config)
            )
            payload = json.loads(result.stdout)
            self.assertEqual(
                {"model": "gpt-6-astra", "effort": "medium", "fast": True},
                payload["assignment"],
            )

    def test_configure_accepts_a_complete_custom_role(self) -> None:
        result = self.run_models(
            "configure",
            "--preset",
            "codex-preset",
            "--set",
            "new_skill.model=gpt-new",
            "--set",
            "new_skill.effort=high",
            "--set",
            "new_skill.fast=true",
            "--dry-run",
        )
        self.assertIn("[roles.new_skill]", result.stdout)
        self.assertIn('model = "gpt-new"', result.stdout)
        self.assertIn('effort = "high"', result.stdout)
        self.assertIn("fast = true", result.stdout)

    def test_fast_is_independent_of_model(self) -> None:
        result = self.run_models(
            "configure",
            "--preset",
            "claude-preset",
            "--set",
            "delegate_default.fast=true",
            "--dry-run",
        )
        self.assertIn("fast = true", result.stdout)
        self.assertNotIn("runner", result.stdout)

    def test_legacy_runner_override_requires_update(self) -> None:
        result = self.run_models(
            "configure",
            "--preset",
            "codex-preset",
            "--set",
            "delegate_default.runner=codex",
            "--dry-run",
            expected_code=2,
        )
        self.assertIn("runner", result.stderr)
        self.assertIn("setup-mstack", result.stderr)


if __name__ == "__main__":
    unittest.main()
