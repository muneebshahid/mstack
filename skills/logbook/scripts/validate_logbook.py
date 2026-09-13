from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import date
from pathlib import Path


FILENAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def validate_tree(root: Path) -> tuple[int, list[str]]:
    if not root.is_dir():
        return 0, [f"{root}: logbook directory does not exist"]

    count = 0
    errors: list[str] = []
    for path in sorted(root.iterdir()):
        if not path.is_file():
            errors.append(f"{path.name}: entries must be files directly inside the logbook")
            continue
        match = FILENAME.fullmatch(path.name)
        if match is None:
            errors.append(f"{path.name}: expected YYYY-MM-DD-lowercase-description.md")
            continue
        count += 1
        try:
            date.fromisoformat(match.group(1))
        except ValueError:
            errors.append(f"{path.name}: filename contains an invalid date")
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or re.fullmatch(r"# Logbook: \S.*", lines[0]) is None:
            errors.append(f"{path.name}: first line must be '# Logbook: <title>'")
    return count, errors


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="logbook-validator-") as temporary:
        root = Path(temporary)
        valid = root / "2026-09-13-example-change.md"
        valid.write_text("# Logbook: Example change\n", encoding="utf-8")
        if validate_tree(root) != (1, []):
            raise AssertionError("A flat entry was rejected")
        nested = root / "implemented"
        nested.mkdir()
        valid.rename(nested / valid.name)
        if not validate_tree(root)[1]:
            raise AssertionError("A nested entry was accepted")
        (nested / valid.name).rename(valid)
        nested.rmdir()
        invalid_date = root / "2026-02-30-example-change.md"
        valid.rename(invalid_date)
        if not validate_tree(root)[1]:
            raise AssertionError("An impossible date was accepted")
        invalid_date.rename(valid)
        valid.write_text("", encoding="utf-8")
        if not validate_tree(root)[1]:
            raise AssertionError("An untitled entry was accepted")
        valid.rename(root / "undated.md")
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
