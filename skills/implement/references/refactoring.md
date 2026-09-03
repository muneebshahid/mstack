# Refactoring

Use this mode when structure changes and externally observable behavior must remain the same. A refactor that smuggles in a feature or bug fix loses its safety claim; split that work into its own mode.

## 1. Pin the behavior contract

- Read [How](../../how/SKILL.md) to understand the affected flow, callers, side effects, boundaries, and failure behavior. Read [Why](../../why/SKILL.md) only when historical constraints may explain an apparently odd contract.
- Before moving structure, establish a characterization test, snapshot, replay, or old-versus-new equivalence harness. Type checking and compilation alone are not a behavior pin.
- Read [Prove It Works](../../principle-prove-it-works/SKILL.md) so the chosen pin observes the real artifact rather than a proxy.

## 2. Name the target shape

- Read [Model the Domain](../../principle-model-the-domain/SKILL.md) when scattered branches, booleans, repeated shape assumptions, or ad hoc mutation reveal a missing structure.
- State the intended module layout, types, ownership, and call graph under the pinned contract. If that contract exposes a materially wrong existing shape, read [Redesign From First Principles](../../principle-redesign-from-first-principles/SKILL.md) and derive the target as if the corrected assumptions had existed on day one. An established rename, move, inline, extraction, or mechanical deduplication with a clear target does not load Redesign.
- If several consequential target shapes remain viable, use [Architect](../../architect/SKILL.md) as a read-only design checkpoint and apply [Exhaust the Design Space](../../principle-exhaust-the-design-space/SKILL.md). Architect always stops after synthesis; then resume this Refactoring workflow. Skip design competition when the target is established and mechanical.

Load structural principles where their triggers appear:

- Invariants, mutations, side effects, lifecycle, failure policy, or placement lack one canonical owner: [Clear Ownership](../../principle-clear-ownership/SKILL.md).
- Core policy imports infrastructure, framework, transport, persistence, or vendor mechanisms: [Dependency Direction](../../principle-dependency-direction/SKILL.md).
- Public contracts, external representations, validation, persistence, transport, or error translation cross a boundary: [Boundary Discipline](../../principle-boundary-discipline/SKILL.md).
- Types admit invalid states, confuse primitives, duplicate schemas, or require unsafe coercion: [Type System Discipline](../../principle-type-system-discipline/SKILL.md).
- Concurrent actors mutate shared state: [Separate Before Serializing Shared State](../../principle-separate-before-serializing-shared-state/SKILL.md).
- Retried, restarted, or partially failed operations are being reshaped: [Make Operations Idempotent](../../principle-make-operations-idempotent/SKILL.md).

## 3. Subtract, then move

- Read [Subtract Before You Add](../../principle-subtract-before-you-add/SKILL.md). Delete dead weight, one-caller pass-throughs, redundant validators, stale references, and obsolete branches before introducing the target structure.
- Read [Minimize Reader Load](../../principle-minimize-reader-load/SKILL.md). The refactor must reduce layers to trace, state to remember, duplicated decisions, or needless lines somewhere concrete. If it does not, reconsider it.
- When replacing an internal API, read [Migrate Callers Then Delete Legacy APIs](../../principle-migrate-callers-then-delete-legacy-apis/SKILL.md). Inventory every caller, migrate them, and remove the old path in the same wave unless a real external compatibility contract requires a time-boxed migration.
- For a coordinated rewrite or migration with explicit phase boundaries, read [Outcome-Oriented Execution](../../principle-outcome-oriented-execution/SKILL.md). Optimize for the accepted end state while keeping each declared verification boundary coherent.
- For large mechanical moves, consider [Build the Lever](../../principle-build-the-lever/SKILL.md). Prove the transformation on one representative unit, then rerun it safely.

## 4. Move in verifiable units

- Read [Sequence Verifiable Units](../../principle-sequence-verifiable-units/SKILL.md). Keep the behavior pin green after each coherent slice. When commits are authorized, order them so each can be understood and reverted independently.
- Apply [No Comments](../../principle-no-comments/SKILL.md). Replace rationale and constraints with names, types, structure, tests, or the external decision logbook.
- Re-ground renames and migrations against the actual repository. Check string references, configuration, generated boundaries, documentation, and callers rather than trusting a mechanical summary.
- If a recurring correction is exposed, read [Encode Lessons in Structure](../../principle-encode-lessons-in-structure/SKILL.md) and add only the proportionate durable guardrail.

## 5. Prove equivalence

- Replay the original pin against the new structure and exercise the matching surface.
- Run repository-required checks and inspect the final diff for behavior changes, dual APIs, compatibility residue, comments, accidental abstractions, and missed callers.
- State the reader-load delta: what readers no longer have to trace or remember.
- If behavior changed, stop calling the unit a refactor. Revert or split the change into Feature or Bug Fix.

Reply with the pinned contract, old and target structures, ordered changes, equivalence evidence, reader-load reduction, and any behavior change split out rather than hidden.
