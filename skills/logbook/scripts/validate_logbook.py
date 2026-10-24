from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path


CLASSES = ("decisions", "incidents", "investigations")
FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def validate_entry(path: Path, name: str) -> list[str]:
    match = FILENAME.fullmatch(path.name)
    if match is None:
        return [f"{name}: expected YYYY-MM-DD-lowercase-description.md"]
    errors: list[str] = []
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        errors.append(f"{name}: filename contains an invalid date")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or re.fullmatch(r"# Logbook: \S.*", lines[0]) is None:
        errors.append(f"{name}: first line must be '# Logbook: <title>'")
    return errors


def validate_tree(root: Path) -> tuple[int, list[str]]:
    if not root.is_dir():
        return 0, [f"{root}: logbook directory does not exist"]

    count = 0
    errors: list[str] = []
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or folder.name not in CLASSES:
            errors.append(f"{folder.name}: entries belong in {', '.join(CLASSES)}")
            continue
        for path in sorted(folder.iterdir()):
            name = f"{folder.name}/{path.name}"
            if not path.is_file():
                errors.append(f"{name}: entries must be files directly inside their class folder")
                continue
            count += 1
            errors.extend(validate_entry(path, name))
    return count, errors


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="logbook-validator-") as temporary:
        root = Path(temporary)
        decisions = root / "decisions"
        decisions.mkdir()
        valid = decisions / "2026-09-13-example-change.md"
        valid.write_text("# Logbook: Example change\n", encoding="utf-8")
        if validate_tree(root) != (1, []):
            raise AssertionError("A classified entry was rejected")
        unclassified = root / valid.name
        valid.rename(unclassified)
        if not validate_tree(root)[1]:
            raise AssertionError("An unclassified entry was accepted")
        unknown = root / "notes"
        unknown.mkdir()
        unclassified.rename(unknown / valid.name)
        if not validate_tree(root)[1]:
            raise AssertionError("An unknown class was accepted")
        nested = decisions / "2026"
        nested.mkdir()
        (unknown / valid.name).rename(nested / valid.name)
        unknown.rmdir()
        if not validate_tree(root)[1]:
            raise AssertionError("A nested entry was accepted")
        (nested / valid.name).rename(valid)
        nested.rmdir()
        invalid_date = decisions / "2026-02-30-example-change.md"
        valid.rename(invalid_date)
        if not validate_tree(root)[1]:
            raise AssertionError("An impossible date was accepted")
        invalid_date.rename(valid)
        valid.write_text("", encoding="utf-8")
        if not validate_tree(root)[1]:
            raise AssertionError("An untitled entry was accepted")
        valid.rename(decisions / "undated.md")
        if not validate_tree(root)[1]:
            raise AssertionError("An undated file was accepted")
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
