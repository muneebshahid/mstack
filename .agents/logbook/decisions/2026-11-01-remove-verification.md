# Logbook: Remove Verification

Partly superseded by [Remove Review, Implement, and Architect](2026-11-01-remove-review-implement-architect.md): Implement and its verify line are removed.

## Context

`skills/apply-principles/references/verification.md` set out how to match evidence to a claim: which checks prove what, exercising the closest surface, and reporting skips. Implement and the Apply Principles catalog pointed to it.

## Decision

Owner's call: remove the reference, leaving seven principle references. Implement instead says to always verify changes are working if possible, and leaves the method to the agent.

## Rejected

None considered.

## Verification and gaps

- `scripts/validate.py` passed, including links.
- With the testing reference also gone, no MStack text says when to add tests while implementing. Review still assesses test usefulness.
