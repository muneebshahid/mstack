# Logbook: Remove Diagnosis

## Context

`skills/apply-principles/references/diagnosis.md` held root-cause guidance: reproduce failures, fix at the owner, and inspect persistent state after restarts. Implement and the Apply Principles catalog pointed to it.

## Decision

Owner's call: remove the reference, leaving eight principle references. Implement keeps its reminder to add targeted logs when the failing path is unclear and remove them afterward. No other MStack text now tells agents to find a root cause before fixing.

## Rejected

None considered.

## Verification and gaps

- `scripts/validate.py` passed, including links.
- No trial has measured how debugging changes without this guidance.
