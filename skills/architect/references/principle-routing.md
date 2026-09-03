# Architect principle routing

Architect owns this selection. Resolve each selected ID to the sibling skill at `../../<id>/SKILL.md`, convert it to an absolute path, read every selected file completely, and pass the same ordered absolute path list to both Arena candidates. Do not invoke `apply-principles` inside the candidate panel.

## Core design principles

Read these for every Architect design:

- `principle-experience-first`
- `principle-exhaust-the-design-space`
- `principle-model-the-domain`
- `principle-clear-ownership`
- `principle-boundary-discipline`
- `principle-dependency-direction`
- `principle-minimize-reader-load`

## Conditional design principles

Add a leaf only when grounding or the requested design concretely matches its trigger:

| Trigger | Principle |
|---|---|
| Typed code risks invalid states, primitive confusion, loose casts, or non-exhaustive variants | `principle-type-system-discipline` |
| Concurrent actors may mutate shared state | `principle-separate-before-serializing-shared-state` |
| Retry, restart, crash, or partial failure affects an operation | `principle-make-operations-idempotent` |
| The requirement appears bolted onto the wrong existing shape | `principle-redesign-from-first-principles` |
| Existing complexity can be removed before extension | `principle-subtract-before-you-add` |
| A migration or rewrite has explicit intermediate states | `principle-outcome-oriented-execution` |
| A new internal API replaces legacy callers | `principle-migrate-callers-then-delete-legacy-apis` |
| The design corrects a recurring failure or workaround | `principle-fix-root-causes` |
| Repeated operational knowledge should become an executable guardrail | `principle-encode-lessons-in-structure` |

Do not load conditionals speculatively. Candidate prompts receive design principles only. If a candidate specifically needs the temporary TODO-sketch exception, also provide `principle-no-comments`; Architect does not implement the resulting design.
