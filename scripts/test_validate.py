from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import validate


class RepositoryFilesTest(unittest.TestCase):
    def test_filters_deleted_tracked_and_ignored_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_git(root, "init")
            (root / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
            (root / "present.txt").write_text("present\n", encoding="utf-8")
            (root / "deleted.txt").write_text("deleted\n", encoding="utf-8")
            self.run_git(root, "add", ".gitignore", "present.txt", "deleted.txt")
            (root / "deleted.txt").unlink()
            (root / "new.txt").write_text("new\n", encoding="utf-8")
            (root / "ignored.txt").write_text("ignored\n", encoding="utf-8")

            original_root = validate.ROOT
            validate.ROOT = root
            try:
                paths = validate.repository_files()
            finally:
                validate.ROOT = original_root

            self.assertEqual(
                {path.relative_to(root) for path in paths},
                {Path(".gitignore"), Path("present.txt"), Path("new.txt")},
            )

    @staticmethod
    def run_git(root: Path, *arguments: str) -> None:
        subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
