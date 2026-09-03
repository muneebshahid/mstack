# Feature

Use this mode when intended behavior is being added or deliberately changed. Own the outcome and design, not merely the requested files.

## 1. Define the experience and proof

- State the user-visible or caller-visible outcome, non-goals, and acceptance evidence before coding.
- For product, UI, API, or maintainer-facing tradeoffs, read [Experience First](../../principle-experience-first/SKILL.md). Prefer a smaller polished core over a wider rough surface.
- If the important uncertainty is experiential or empirical, run [Prototype](prototype.md) first. If it is a consequential architectural shape with several viable answers, use [Architect](../../architect/SKILL.md).
- When a novel consequential choice lacks decisive precedent, read [Exhaust the Design Space](../../principle-exhaust-the-design-space/SKILL.md); satisfy it through Prototype or Architect rather than inventing options inside implementation.

## 2. Ground the current system

- Inspect the affected source, tests, public contracts, data flow, and repository instructions. Read [How](../../how/SKILL.md) for a non-trivial subsystem.
- Read [Why](../../why/SKILL.md) when history or an earlier decision could reveal a real constraint. Do not infer historical intent from current code alone.
- Identify what can be removed before construction and read [Subtract Before You Add](../../principle-subtract-before-you-add/SKILL.md).

## 3. Choose the target shape

Load only the principles whose trigger is present:

- Core concepts, invariants, state transitions, or repeated branching need a coherent structure: [Model the Domain](../../principle-model-the-domain/SKILL.md).
- The new requirement looks bolted onto a shape that would differ if the requirement had existed on day one: [Redesign From First Principles](../../principle-redesign-from-first-principles/SKILL.md).
- Invariants, mutations, side effects, lifecycle, failure policy, or placement need one canonical owner: [Clear Ownership](../../principle-clear-ownership/SKILL.md).
- Stable policy risks importing framework, persistence, transport, or vendor mechanisms: [Dependency Direction](../../principle-dependency-direction/SKILL.md).
- External data, public APIs, persistence, transport, validation, or error translation cross a boundary: [Boundary Discipline](../../principle-boundary-discipline/SKILL.md).
- Typed code represents invalid states, confuses semantic primitives, duplicates schemas, or needs unsafe coercion: [Type System Discipline](../../principle-type-system-discipline/SKILL.md).
- Concurrent actors may write the same state: [Separate Before Serializing Shared State](../../principle-separate-before-serializing-shared-state/SKILL.md).
- Operations may retry, restart, or partially fail: [Make Operations Idempotent](../../principle-make-operations-idempotent/SKILL.md).

Use [Architect](../../architect/SKILL.md) as a read-only design checkpoint before implementation when these concerns create a consequential choice with multiple viable shapes. It always stops after the synthesized design; then resume this Feature workflow for implementation and verification. A local, established extension does not require architecture ceremony.

## 4. Simplify and sequence

- Read [Minimize Reader Load](../../principle-minimize-reader-load/SKILL.md). Choose the smallest direct design that preserves correctness, makes decisions easy to find, and avoids speculative layers or state.
- If a new internal API replaces an old one and callers can migrate together, read [Migrate Callers Then Delete Legacy APIs](../../principle-migrate-callers-then-delete-legacy-apis/SKILL.md). Do not leave accidental dual paths.
- For a planned rewrite or migration with explicit phase boundaries, read [Outcome-Oriented Execution](../../principle-outcome-oriented-execution/SKILL.md) and declare any intentionally unstable intermediate state.
- For repetitive, large, error-prone, or audit-sensitive work, consider [Build the Lever](../../principle-build-the-lever/SKILL.md). Build the smallest rerunnable tool only when it repays its cost.
- Read [Sequence Verifiable Units](../../principle-sequence-verifiable-units/SKILL.md). Deliver the smallest end-to-end slice first and verify each coherent unit before the next. Create commits only with authority; when authorized, prefer green commits that tell the change's story.

## 5. Implement

- Exercise the end-to-end path early instead of building every layer in isolation.
- Keep the implementation within the accepted target shape and scope. Surface material deviations before they silently become a second design.
- Apply [No Comments](../../principle-no-comments/SKILL.md) to all owned source. Temporary architecture-sketch or scaffold TODOs must be gone when their bodies are implemented.
- When the work exposes a genuinely recurring correction or failure mode, read [Encode Lessons in Structure](../../principle-encode-lessons-in-structure/SKILL.md) and choose the lightest durable guardrail. Do not generalize an isolated observation into machinery.

## 6. Prove it

Read [Prove It Works](../../principle-prove-it-works/SKILL.md). Run repository checks, exercise the actual feature surface, and trace the full input-to-output path. For browser-visible changes, apply its journey-level Pass, Fail, or Skip-with-reason reporting only to materially affected states. Inspect the diff for unintended scope, stale callers, parallel APIs, comments, and unverified behavior. Report an inconclusive surface honestly.

Reply with what changed, the outcome now observable, key choices and tradeoffs, direct verification, and open risks or decisions.
