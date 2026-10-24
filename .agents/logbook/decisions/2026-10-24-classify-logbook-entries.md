# Logbook: Classify Logbook entries and record only what agents need

## Context

The Logbook required one entry per commit. Its "Work and decisions" section asked what was tried and what happened, so entries read as session diaries: 33 records averaged about 590 words, with session IDs, validator counts and step-by-step narration. Entries in another repository named the owner throughout, which recorded questions and passing remarks as if they were requirements. Superseded entries had no pointer to what replaced them, so an agent finding one by search could take it as current.

## Decision

Write an entry only when a future agent would need it, and let the agent decide. Entries live in `decisions/`, `incidents/` or `investigations/` with dated filenames, each class with its own [template](../../../skills/logbook/references/record-format.md). Entries record outcomes, name no people, and mark preference decisions "owner's call". Entries are not rewritten, except that an earlier entry gets a "Superseded by" line below its title when a later one changes it. The 33 existing entries were reviewed against the new bar. Seven whose reasoning was obsolete or recorded elsewhere were deleted; references to them name the commit that still holds them. The other 26 moved into the classes unchanged apart from links, those lines, and one removed machine path. Version 0.4.4.

Owner's call: keep files rather than commit messages, with class folders and dates.

## Rejected

- **Commit messages only:** cannot hold incidents or investigations without a code change, and files are found by a plain search of the tree.
- **One file per topic, kept current:** incidents and investigations are events, not topics.
- **Date folders inside each class:** a listing would show only dates, not topics.
- **Separate bug and incident folders:** both follow the same pattern of symptom, cause, fix and prevention.
- **An `adr/` folder:** `decisions/` makes clear that process and tooling choices belong there too.
- **Workers writing entries:** the parent keeps final judgment and can tell a local implementation choice from a decision worth recording, so workers return evidence and the parent writes.

## Verification and gaps

- The validator self-test covers classified, unclassified, unknown-class, nested, misdated, untitled and undated entries.
- `scripts/validate.py` passed, including all links after the move; the Codex skill validator passed for the four changed skills; `claude plugin validate .` passed.
- No agent has yet written an entry under the new rules, so the threshold and templates are untested in use.
- Other repositories using the skill keep the old flat layout until migrated.
