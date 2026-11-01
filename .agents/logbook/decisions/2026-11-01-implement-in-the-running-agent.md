# Logbook: Implement in the running agent

Superseded by [Remove Review, Implement, and Architect](2026-11-01-remove-review-implement-architect.md): the skill is removed.

## Context

Implement let the parent spawn a persistent `implement_worker` through Delegate, and carried a separate testing reference. The parent had to inspect and verify every diff either way, and the worker path required a dedicated model role and rules for ownership transfer after failures.

## Decision

Owner's call: the running agent makes the edits itself. Implement no longer delegates, and the `implement_worker` role is gone from the registry and both presets. Delegate stays available for other scoped tasks.

Owner's call: remove `skills/implement/references/testing.md`. Version 0.4.5.

## Rejected

- **Keep the worker as an option:** leaves a role, a reference, and ownership rules that exist only for a path this workflow no longer takes.
- **Keep the role for future use:** an unused required preset entry; adding a role later is cheap.

## Verification and gaps

- `scripts/validate.py` passed, covering links, manifests, Logbook layout, and resolver tests.
- Saved profiles with a partial `[roles.implement_worker]` override now fail resolution until that table is removed; complete overrides resolve as an unused custom role.
- This is an instruction change with no behavioral trial, so the effect on large changes is unmeasured.
