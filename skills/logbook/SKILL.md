---
name: logbook
description: "Capture or refresh repository records of non-trivial changes and meaningful investigation or review outcomes, preserving work, rationale, evidence, and gaps."
---

# Logbook

Every non-trivial change adds or updates a relevant record. This includes changes to behavior, architecture, shared contracts, process, or testing strategy. Mechanical or local edits that change none of these and introduce no new rationale are exempt.

Preserve meaningful investigation and review outcomes too: what agents did, what was accepted or rejected and why, verification, and remaining gaps. A rejected simplification or overengineering suggestion can prevent a later mistake. Record the useful conclusion and supporting work, not every command, candidate, or hypothesis. Related findings can share a record.

## Capture

The parent alone creates, edits, moves, or deletes records. Workers and reviewers supply evidence and clarification. Read [references/record-format.md](references/record-format.md) completely before writing.

Search `.agents/logbook/` and relevant repository history. Update the record that owns the same topic; create a distinct record for a different decision or outcome. Keep files flat within these folders:

- `proposed/`: unfinished changes, pending proposals, or unresolved investigations.
- `implemented/`: realized, freshly verified changes or completed, verified investigation and review conclusions.
- `rejected/`: a considered proposal was declined and its reasoning remains useful.

A completed investigation can recommend future work and still belong in implemented. Distinguish pending recommendations from realized changes without creating a separate record for every follow-up. Meaningful rejected proposals may have their own record or remain with the broader audit that evaluated them.

During implementation, the parent inspects each unit and its evidence, then updates the relevant record. Change lifecycle and wording as the outcome becomes verified or rejected. When commits are authorized, keep the record with the change it explains.

Resolve `scripts/validate_logbook.py` from this skill's directory and run it with the consumer repository's logbook path as its argument. Resolve validation failures and report affected records and material gaps.

## Keep facts and history distinct

Current code, tests, and contracts establish present mechanics. Records preserve stated rationale; proposed and rejected records do not establish shipped behavior. Update moved paths, names, and other factual details with the work they describe. Never rewrite historical reasoning to pretend a later decision was always intended.

For a reversed decision, create a replacement and cross-link both records. A record supports future work; it does not replace executable constraints or user documentation.

## Refresh

When requested, compare the named records with current evidence, correct stale facts, and identify duplication or supersession. Keep partially superseded records linked. Consolidate only when the surviving record preserves unique rationale, alternatives, consequences, evidence gaps, and revisit conditions; repair inbound links.

Retain rejected records while their conclusions prevent plausible mistakes. Delete only within authorized cleanup. Do not add indexes, archives, translations, or sidecar machinery.
