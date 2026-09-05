# Feature

Use this mode when intended behavior is being added or deliberately changed. Own the outcome and design, not merely the requested files.

## 1. Define the experience and proof

- State the user-visible or caller-visible outcome, non-goals, and acceptance evidence before coding.
- For product, UI, API, maintainer-facing tradeoffs, or an unresolved consequential choice, read [Design Decisions](../../apply-principles/references/design-decisions.md). Prefer a smaller polished core over a wider rough surface without dropping requested behavior.
- If the important uncertainty is experiential or empirical, run [Prototype](prototype.md) first. If it is a consequential architectural shape with several viable answers, use [Architect](../../architect/SKILL.md).
- Satisfy a novel consequential choice through Prototype or Architect rather than inventing options inside implementation.

## 2. Ground the current system

- Inspect the affected source, tests, public contracts, data flow, and repository instructions. Read [How](../../how/SKILL.md) for a non-trivial subsystem.
- Read [Why](../../why/SKILL.md) when history or an earlier decision could reveal a real constraint. Do not infer historical intent from current code alone.
- Identify what can be removed before construction and read [Simplicity](../../apply-principles/references/simplicity.md).

## 3. Choose the target shape

Use [Apply Principles](../../apply-principles/SKILL.md) to select the smallest relevant set from its shared index using the actual task and evidence. Read selected references before applying them; new evidence may add another reference without rereading unchanged guidance.
If the requirement demonstrably fights the current shape, read [Design Decisions](../../apply-principles/references/design-decisions.md) before choosing the target.

Use [Architect](../../architect/SKILL.md) as a read-only design checkpoint before implementation when these concerns create a consequential choice with multiple viable shapes. It always stops after the synthesized design; then resume this Feature workflow for implementation and verification. A local, established extension does not require architecture ceremony.

## 4. Simplify and sequence

- Use [Simplicity](../../apply-principles/references/simplicity.md) to choose the smallest direct design that preserves correctness, makes decisions easy to find, and avoids speculative layers or state.
- If a new internal API replaces an old one and callers can migrate together, read [Delivery and Migration](../../apply-principles/references/delivery-and-migration.md). Do not leave accidental dual paths.
- For a planned rewrite or migration with explicit phase boundaries, use [Delivery and Migration](../../apply-principles/references/delivery-and-migration.md) and declare any intentionally unstable intermediate state.
- For repetitive, large, error-prone, or audit-sensitive work, consider [Automation and Learning](../../apply-principles/references/automation-and-learning.md). Build the smallest rerunnable tool only when it repays its cost.
- Use [Delivery and Migration](../../apply-principles/references/delivery-and-migration.md) to deliver the smallest end-to-end slice first and verify each coherent unit before the next. Create commits only with authority; when authorized, prefer green commits that tell the change's story.

## 5. Implement

- Exercise the end-to-end path early instead of building every layer in isolation.
- Keep the implementation within the accepted target shape and scope. Surface material deviations before they silently become a second design.
- Apply [Source Style](../../apply-principles/references/source-style.md) to all owned source.
- When the work exposes a genuinely recurring correction or failure mode, use [Automation and Learning](../../apply-principles/references/automation-and-learning.md) to choose the lightest durable guardrail. Do not generalize an isolated observation into machinery.

## 6. Prove it

Read [Verification](../../apply-principles/references/verification.md). Run repository checks, exercise the actual feature surface, and trace the full input-to-output path. For browser-visible changes, apply its journey-level Pass, Fail, or Skip-with-reason reporting only to materially affected states. Inspect the diff for unintended scope, stale callers, parallel APIs, comments, and unverified behavior. Report an inconclusive surface honestly.

Reply with what changed, the outcome now observable, key choices and tradeoffs, direct verification, and open risks or decisions.
