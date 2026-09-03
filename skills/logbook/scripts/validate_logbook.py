from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path


LIFECYCLES = ("proposed", "implemented", "rejected")
KINDS = ("architecture", "behavior", "bug-fix", "simplification", "process", "testing")
FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def headings(text: str) -> list[str]:
    result: list[str] = []
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            result.append(line.rstrip())
    return result


def validate_note(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(root)
    parts = relative.parts
    if len(parts) != 2 or parts[0] not in LIFECYCLES:
        return [f"{relative}: expected {{proposed,implemented,rejected}}/YYYY-MM-DD-topic.md"]

    lifecycle = parts[0]
    match = FILENAME.fullmatch(parts[1])
    if match is None:
        errors.append(f"{relative}: filename must be YYYY-MM-DD-lowercase-topic.md")
    else:
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            errors.append(f"{relative}: filename contains an invalid date")

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or re.fullmatch(r"# Logbook: \S.*", lines[0]) is None:
        errors.append(f"{relative}: line 1 must be '# Logbook: <title>'")
    if len(lines) < 2 or lines[1] != "":
        errors.append(f"{relative}: line 2 must be blank")
    expected_status = f"Status: {lifecycle}"
    if len(lines) < 3 or lines[2] != expected_status:
        errors.append(f"{relative}: line 3 must be '{expected_status}'")
    if len(lines) < 4 or not lines[3].startswith("Kind: "):
        errors.append(f"{relative}: line 4 must be 'Kind: <kind>'")
    elif lines[3][6:] not in KINDS:
        errors.append(f"{relative}: unknown kind '{lines[3][6:]}'")
    if len(lines) < 5 or lines[4] != "":
        errors.append(f"{relative}: line 5 must be blank")

    found = headings(path.read_text(encoding="utf-8"))
    primary = "## Decision" if lifecycle == "implemented" else "## Proposal"
    forbidden = "## Proposal" if lifecycle == "implemented" else "## Decision"
    required = [
        "## Problem",
        primary,
        "## Alternatives considered",
        "## Evidence",
        "## Consequences",
        "## Revisit when",
    ]
    if found and found[0] != "## Problem":
        errors.append(f"{relative}: first section must be '## Problem'")
    for section in required:
        if section not in found:
            errors.append(f"{relative}: missing '{section}'")
    if forbidden in found:
        errors.append(f"{relative}: {lifecycle} records must not contain '{forbidden}'")
    if len(found) != len(set(found)):
        errors.append(f"{relative}: duplicate level-two section")
    positions = [found.index(section) for section in required if section in found]
    if positions != sorted(positions):
        errors.append(f"{relative}: required sections are out of order")
    return errors


def validate_tree(root: Path) -> tuple[int, list[str]]:
    if not root.exists():
        return 0, [f"{root}: logbook root does not exist"]
    if not root.is_dir():
        return 0, [f"{root}: logbook root is not a directory"]

    errors: list[str] = []
    notes = sorted(root.rglob("*.md"))
    for child in root.iterdir():
        if child.is_dir() and child.name not in LIFECYCLES:
            errors.append(f"{child.relative_to(root)}/: unknown lifecycle directory")
        elif child.is_file():
            errors.append(f"{child.relative_to(root)}: files must live inside a lifecycle directory")
    for note in notes:
        errors.extend(validate_note(note, root))
    return len(notes), errors


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="logbook-validator-") as temporary:
        root = Path(temporary) / ".agents" / "logbook"
        implemented = root / "implemented"
        implemented.mkdir(parents=True)
        valid = implemented / "2026-09-02-example-decision.md"
        valid.write_text(
            "# Logbook: Example decision\n\n"
            "Status: implemented\n"
            "Kind: architecture\n\n"
            "## Problem\n\nProblem.\n\n"
            "## Decision\n\nDecision.\n\n"
            "## Alternatives considered\n\nAlternative.\n\n"
            "## Evidence\n\nEvidence.\n\n"
            "## Consequences\n\nConsequences.\n\n"
            "## Revisit when\n\nSignal.\n",
            encoding="utf-8",
        )
        count, errors = validate_tree(root)
        if count != 1 or errors:
            print("self-test valid fixture failed", file=sys.stderr)
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        valid.write_text(valid.read_text(encoding="utf-8").replace("Status: implemented", "Status: proposed"), encoding="utf-8")
        _, invalid_errors = validate_tree(root)
        if not invalid_errors:
            print("self-test invalid fixture passed unexpectedly", file=sys.stderr)
            return 1
    print("validate_logbook self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(".agents/logbook"))
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        return self_test()

    count, errors = validate_tree(arguments.root.resolve())
    if errors:
        print("validate_logbook: violations found", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print(f"validate_logbook: {count} record(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
