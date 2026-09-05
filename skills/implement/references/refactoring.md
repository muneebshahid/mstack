# Refactoring

Use this mode when structure changes and externally observable behavior must remain the same. A refactor that smuggles in a feature or bug fix loses its safety claim; split that work into its own mode.

## 1. Pin the behavior contract

- Read [How](../../how/SKILL.md) to understand the affected flow, callers, side effects, boundaries, and failure behavior. Read [Why](../../why/SKILL.md) only when historical constraints may explain an apparently odd contract.
- Before moving structure, establish a characterization test, snapshot, replay, or old-versus-new equivalence harness. Type checking and compilation alone are not a behavior pin.
- Read [Verification](../../apply-principles/references/verification.md) so the chosen pin observes the real artifact rather than a proxy.

## 2. Name the target shape

- Read [Modeling and Types](../../apply-principles/references/modeling-and-types.md) when scattered branches, booleans, repeated shape assumptions, or ad hoc mutation reveal a missing structure.
- State the intended module layout, types, ownership, and call graph under the pinned contract. If that contract exposes a materially wrong existing shape, use [Design Decisions](../../apply-principles/references/design-decisions.md) to derive the target as if the corrected assumptions had existed on day one. An established rename, move, inline, extraction, or mechanical deduplication with a clear target does not load design competition.
- If several consequential target shapes remain viable, use [Architect](../../architect/SKILL.md) as a read-only design checkpoint. Architect always stops after synthesis; then resume this Refactoring workflow. Skip design competition when the target is established and mechanical.

Use [Apply Principles](../../apply-principles/SKILL.md) to select the smallest relevant set from its shared index using the pinned contract and target shape. Read selected references before applying them; new evidence may add another reference without rereading unchanged guidance.

## 3. Subtract, then move

- Read [Simplicity](../../apply-principles/references/simplicity.md). Delete dead weight, redundant validators, stale references, and obsolete branches before introducing the target structure.
- When replacing an internal API or coordinating a rewrite with explicit phases, read [Delivery and Migration](../../apply-principles/references/delivery-and-migration.md). Inventory callers, remove the old path when compatibility is not required, and keep each verification boundary coherent.
- For large mechanical moves, consider [Automation and Learning](../../apply-principles/references/automation-and-learning.md). Prove the transformation on one representative unit, then rerun it safely.

## 4. Move in verifiable units

- Use [Delivery and Migration](../../apply-principles/references/delivery-and-migration.md) to keep the behavior pin green after each coherent slice. When commits are authorized, order them so each can be understood and reverted independently.
- Apply [Source Style](../../apply-principles/references/source-style.md). Enforce constraints through names, types, structure, and checks; put rationale in [Logbook](../../logbook/SKILL.md) or separate prose.
- Re-ground renames and migrations against the actual repository. Check string references, configuration, generated boundaries, documentation, and callers rather than trusting a mechanical summary.
- If a recurring correction is exposed, read [Automation and Learning](../../apply-principles/references/automation-and-learning.md) and add only the proportionate durable guardrail.

## 5. Prove equivalence

- Replay the original pin against the new structure and exercise the matching surface using [Verification](../../apply-principles/references/verification.md).
- Run repository-required checks and inspect the final diff for behavior changes, dual APIs, compatibility residue, comments, accidental abstractions, and missed callers.
- State the reader-load delta: what readers no longer have to trace or remember.
- If behavior changed, stop calling the unit a refactor. Revert or split the change into Feature or Bug Fix.

Reply with the pinned contract, old and target structures, ordered changes, equivalence evidence, reader-load reduction, and any behavior change split out rather than hidden.
