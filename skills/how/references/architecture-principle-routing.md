# Architecture Critique Principle Routing

How owns this selection. Do not invoke `apply-principles` or Interrogate inside the critic panel.

## Core critique principles

Read these for every architecture critique:

- `principle-clear-ownership`
- `principle-dependency-direction`
- `principle-boundary-discipline`
- `principle-model-the-domain`
- `principle-minimize-reader-load`

## Conditional principles

Add a leaf when the completed explanation or inspected code matches its trigger:

| Trigger | Principle |
|---|---|
| A requirement appears bolted onto the wrong shape | `principle-redesign-from-first-principles` |
| Retry, restart, crash, or partial failure affects operations | `principle-make-operations-idempotent` |
| Concurrent actors may mutate shared state | `principle-separate-before-serializing-shared-state` |
| A new internal API coexists with legacy callers | `principle-migrate-callers-then-delete-legacy-apis` |
| A rewrite or migration has explicit intermediate states | `principle-outcome-oriented-execution` |
| A user-facing flow or public API has experience tradeoffs | `principle-experience-first` |
| A novel consequential design has several viable shapes | `principle-exhaust-the-design-space` |
| The data model relies on weak types, casts, or invalid states | `principle-type-system-discipline` |
| Existing architecture can be simplified before extension | `principle-subtract-before-you-add` |

Resolve each selected ID to the sibling skill at `../../<id>/SKILL.md`, then convert it to an absolute path. Read every selected file completely before launching critics, then provide the same absolute path list to both. Do not load conditionals speculatively.
