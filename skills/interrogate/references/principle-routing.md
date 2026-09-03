# Interrogate Principle Routing

Interrogate owns this selection. Do not invoke `apply-principles` from inside the review panel.

## Core review principles

Read these for every substantive code review:

- `principle-minimize-reader-load`
- `principle-subtract-before-you-add`
- `principle-model-the-domain`
- `principle-boundary-discipline`
- `principle-type-system-discipline`
- `principle-clear-ownership`
- `principle-dependency-direction`
- `principle-no-comments`
- `principle-prove-it-works`

## Conditional principles

Add a leaf when the review evidence matches its trigger:

| Trigger | Principle |
|---|---|
| A requirement is bolted onto the wrong shape | `principle-redesign-from-first-principles` |
| The change fixes a bug, crash, failed test, or workaround | `principle-fix-root-causes` |
| A branch, pull request, sweep, or migration needs coherent checkpoints | `principle-sequence-verifiable-units` |
| A new internal API coexists with an old one | `principle-migrate-callers-then-delete-legacy-apis` |
| A planned rewrite or migration has intermediate states | `principle-outcome-oriented-execution` |
| An operation can retry, restart, or partially fail | `principle-make-operations-idempotent` |
| Concurrent actors can mutate shared state | `principle-separate-before-serializing-shared-state` |
| The change affects a user-facing flow or public consumer API | `principle-experience-first` |
| A novel consequential design had several viable shapes | `principle-exhaust-the-design-space` |
| Large or mechanical work needs a rerunnable artifact | `principle-build-the-lever` |
| The change follows a recurring correction or failure | `principle-encode-lessons-in-structure` |

Resolve each selected ID to the sibling skill at `../../<id>/SKILL.md`, then convert it to an absolute path. Read every selected file completely before launching reviewers, then provide the same absolute path list to both. Do not include a conditional principle merely because it exists.
