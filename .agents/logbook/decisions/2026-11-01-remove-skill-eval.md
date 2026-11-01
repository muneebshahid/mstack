# Logbook: Remove Skill Eval

## Context

Skill Eval compared skill variants in fresh external scenarios. It owned three model roles, and repository instructions routed execution checks through its smoke roles.

## Decision

Owner's call: remove the skill, the `skill_eval_quality_judge`, `skill_eval_smoke_candidate`, and `skill_eval_smoke_judge` roles, and the repository's smoke-role instruction. Setup still advises a cheap model for launch checks and warns that plan mode can route Haiku to a larger model. The last version of the skill is at `git show cb0ab6f:skills/skill-eval/SKILL.md`.

## Rejected

None considered.

## Verification and gaps

- `scripts/validate.py` passed, including links and resolver tests.
- Saved profiles with a partial override of a removed role now fail resolution until that table is removed.
- MStack no longer has a packaged way to test skill changes behaviorally.
