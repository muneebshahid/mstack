---
name: logbook
description: "Record decisions, incidents, and investigations that future agents would need: what was chosen or found, what was rejected, and why."
---

# Logbook

The Logbook is for agents that later work in the repository. Write an entry only when one would need it:

- **Decision:** a choice between options that an agent might otherwise undo or propose again, including options you rejected.
- **Incident:** a bug or failure whose cause or fix is not obvious from the diff.
- **Investigation:** research, a review, or an evaluation whose findings would otherwise be redone. An investigation that ends in a decision is a decision.

Most commits need only a commit message. The parent decides, writes it from its own and its workers' evidence, and commits it with the changes it explains.

Store entries at `.agents/logbook/<class>/YYYY-MM-DD-short-description.md`, where `<class>` is `decisions`, `incidents`, or `investigations`. Use the [template](references/record-format.md) for the class. Git associates each entry with its commit; find it with `git log -- <entry>`.

Record outcomes, not the session. Keep the evidence that explains a choice, such as what failed without it, and leave out step-by-step narration, session IDs, validator counts, and corrections made during the conversation. Most entries fit in about 250 words. Never invent alternatives to fill a section; say when none were considered.

Do not name people or record who asked or suggested what. Give each decision a reason that stands on its own. When the only reason is the owner's preference, mark it "owner's call" so agents ask before reversing it.

Link where the work came from (an issue, CI run, review, or test), related entries, and commits other than the entry's own. Use repository-relative links.

Entries are not rewritten. When a later entry changes an earlier decision, add one line below the earlier entry's title: "Superseded by" and a link to the later entry, or "Partly superseded by", the link, and what changed. Existing entries keep their original format.

Check layout with [scripts/validate_logbook.py](scripts/validate_logbook.py), passing the repository's Logbook directory.
