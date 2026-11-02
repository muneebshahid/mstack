# Logbook: Remove Review, Implement, and Architect

## Context

These three skills wrapped core engineering work: designing, changing, and reviewing code. Each had been shortened repeatedly, and Review and Architect owned the only remaining role-based panels.

## Decision

Owner's call: remove all three skills and the `architect_candidate_a`, `architect_candidate_b`, `review_reviewer_a`, and `review_reviewer_b` roles. `delegate_default` is the only role left. Apply Principles keeps the engineering standards. The last versions are at `git show 229740b:skills/<name>/SKILL.md`.

## Rejected

None considered.

## Verification and gaps

- `scripts/validate.py` passed, including resolver tests and links.
- Saved profiles with a partial override of a removed role fail resolution until that table is removed.
- MStack no longer tells agents to verify their changes, reports results in a set format, or runs multi-model reviews or design comparisons. Apply Principles and Logbook have no skill routing to them; they load when invoked or named in project instructions.
