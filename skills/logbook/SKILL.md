---
name: logbook
description: "Record each commit's work, accepted and rejected approaches, reasons, and verification. Also capture meaningful investigation and review outcomes."
---

# Logbook

Keep one entry per commit. Capture meaningful outcomes during work; finalize the entry before committing it with the changes it explains. Small commits get short entries. Investigations without code changes can have entries too.

The parent writes the entry using evidence from its own work, workers, and reviewers. Follow [the template](references/record-format.md). Record consequential attempts and decisions, including rejected review suggestions and why they were rejected. Distinguish approaches tried from options considered; never invent alternatives to fill a section.

Store entries at `.agents/logbook/YYYY-MM-DD-short-description.md`. Git associates each entry with its commit; no commit hash is needed inside the file.

Later work gets a new entry. Link earlier entries when relevant; leave their historical accounts intact. Existing records can retain their original format.

Check filenames and layout with [scripts/validate_logbook.py](scripts/validate_logbook.py), passing the repository's Logbook directory. Review the content for accuracy and completeness.
