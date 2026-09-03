from __future__ import annotations

import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PRIVATE_KEY = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
TOKEN_ASSIGNMENT = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}"
)


class ValidationFailure(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationFailure(message)


def run(command: list[str]) -> None:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        if completed.stdout:
            print(completed.stdout, file=sys.stderr, end="")
        if completed.stderr:
            print(completed.stderr, file=sys.stderr, end="")
        fail(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def repository_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return [ROOT / value.decode() for value in completed.stdout.split(b"\0") if value]


def frontmatter(text: str, path: Path) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 4 or lines[0] != "---":
        fail(f"Missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"Unclosed YAML frontmatter: {path.relative_to(ROOT)}")
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values


def validate_skills() -> None:
    skill_paths = sorted(SKILLS.glob("*/SKILL.md"))
    if not skill_paths:
        fail("No skills found")
    for skill_path in skill_paths:
        values = frontmatter(skill_path.read_text(encoding="utf-8"), skill_path)
        expected = skill_path.parent.name
        name = values.get("name")
        description = values.get("description")
        if name != expected:
            fail(f"Skill name {name!r} does not match directory {expected!r}")
        if not SKILL_NAME.fullmatch(name):
            fail(f"Invalid skill name: {name}")
        if not description:
            fail(f"Missing skill description: {skill_path.relative_to(ROOT)}")
        if len(name) > 64:
            fail(f"Skill name exceeds 64 characters: {name}")
    print(f"Validated {len(skill_paths)} skills")


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"Expected JSON object: {path.relative_to(ROOT)}")
    return value


def validate_manifests() -> None:
    codex = load_json(ROOT / ".codex-plugin/plugin.json")
    codex_marketplace = load_json(ROOT / ".agents/plugins/marketplace.json")
    claude = load_json(ROOT / ".claude-plugin/plugin.json")
    claude_marketplace = load_json(ROOT / ".claude-plugin/marketplace.json")
    if codex.get("name") != "mstack" or claude.get("name") != "mstack":
        fail("Plugin manifests must use the mstack name")
    if codex.get("version") != claude.get("version"):
        fail("Codex and Claude plugin versions differ")
    if codex_marketplace.get("name") != "mstack":
        fail("Codex marketplace must use the mstack name")
    if claude_marketplace.get("name") != "mstack":
        fail("Claude marketplace must use the mstack name")
    codex_plugins = codex_marketplace.get("plugins")
    claude_plugins = claude_marketplace.get("plugins")
    if not isinstance(codex_plugins, list) or len(codex_plugins) != 1:
        fail("Codex marketplace must contain exactly one plugin")
    if not isinstance(claude_plugins, list) or len(claude_plugins) != 1:
        fail("Claude marketplace must contain exactly one plugin")
    codex_entry = codex_plugins[0]
    claude_entry = claude_plugins[0]
    if not isinstance(codex_entry, dict) or codex_entry.get("name") != "mstack":
        fail("Codex marketplace entry is invalid")
    if not isinstance(claude_entry, dict) or claude_entry.get("name") != "mstack":
        fail("Claude marketplace entry is invalid")
    if claude_entry.get("version") != claude.get("version"):
        fail("Claude marketplace and plugin versions differ")
    print(f"Validated plugin manifests at version {codex['version']}")


def validate_toml() -> None:
    paths = [ROOT / "config/models.defaults.toml", *sorted((ROOT / "config/profiles").glob("*.toml"))]
    for path in paths:
        with path.open("rb") as stream:
            tomllib.load(stream)
    for profile in ("multimodel", "codex", "claude-code"):
        run(
            [
                sys.executable,
                "skills/setup-mstack/scripts/models.py",
                "resolve",
                "--profile",
                profile,
                "--no-user-config",
            ]
        )
    print(f"Validated {len(paths)} TOML files and all packaged profiles")


def validate_links(paths: list[Path]) -> None:
    checked = 0
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target == "url":
                continue
            if not target or target.startswith(
                ("#", "http://", "https://", "mailto:", "codex://")
            ):
                continue
            target = target.split("#", 1)[0]
            if not (path.parent / target).resolve().exists():
                fail(f"Broken link in {path.relative_to(ROOT)}: {target}")
            checked += 1
    print(f"Validated {checked} repository-relative Markdown links")


def validate_repository_hygiene(paths: list[Path]) -> None:
    for path in paths:
        relative = path.relative_to(ROOT)
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            fail(f"Generated Python cache is tracked: {relative}")
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PRIVATE_KEY.search(text):
            fail(f"Private key material found: {relative}")
        if TOKEN_ASSIGNMENT.search(text):
            fail(f"Possible credential assignment found: {relative}")
    print(f"Checked {len(paths)} repository files for hygiene")


def validate_tests() -> None:
    run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "skills/setup-mstack/scripts",
            "-p",
            "test_models.py",
        ]
    )
    run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "skills/claude-code/scripts",
            "-p",
            "test_run_claude.py",
        ]
    )
    run(
        [
            sys.executable,
            "skills/logbook/scripts/validate_logbook.py",
            ".agents/logbook",
        ]
    )
    print("Validated unit tests and Logbook records")


def main() -> int:
    try:
        paths = repository_files()
        validate_skills()
        validate_manifests()
        validate_toml()
        validate_links(paths)
        validate_repository_hygiene(paths)
        validate_tests()
    except (OSError, subprocess.CalledProcessError, ValidationFailure, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1
    print("MStack validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
