---
name: apply-principles
description: "Select and apply the relevant engineering principle skills to a design, implementation plan, code change, migration, debugging task, or review. Use for broad standards judgment when the exact principles are not already known."
---

# Apply Principles

Route the active task to the smallest relevant set of principle skills. This skill owns selection and conflict resolution, not engineering substance. Read every selected leaf in full and treat it as the canonical rule.

## Authority and mode

Inherit authority from the active request:

- **Guidance:** Before implementation, inspect and recommend. Do not edit.
- **Review:** Assess existing work and report findings. Do not edit.
- **Implementation:** Edit only when the user requested implementation or the calling workflow already authorizes it.

If directly invoked without an edit request, use Review mode. A principle never expands scope, grants mutation authority, or overrides higher-level instructions. For every owned-source edit, always load [No Comments](../principle-no-comments/SKILL.md).

## Select principles

Choose from observable triggers. Do not load the whole catalog by default.

### Product and design

- User, API consumer, or maintainer experience determines the target: [Experience First](../principle-experience-first/SKILL.md).
- A novel or consequential choice has multiple viable shapes and no decisive precedent: [Exhaust the Design Space](../principle-exhaust-the-design-space/SKILL.md).

### Architecture and modeling

- Core data structures, state models, invariants, access patterns, or repeated branches need a coherent shape: [Model the Domain](../principle-model-the-domain/SKILL.md).
- Invariants, mutations, side effects, lifecycle, failure policy, or placement lack one owner: [Clear Ownership](../principle-clear-ownership/SKILL.md).
- Core policy imports infrastructure, dependencies cycle, or orchestration crosses layers: [Dependency Direction](../principle-dependency-direction/SKILL.md).
- Public contracts, external data, persistence, transport, plugins, validation, representations, or error translation cross a boundary: [Boundary Discipline](../principle-boundary-discipline/SKILL.md).
- Typed code permits invalid states, primitive confusion, unchecked casts, loose boundary data, or non-exhaustive variants: [Type System Discipline](../principle-type-system-discipline/SKILL.md).
- A new requirement appears bolted onto a shape that should be reconsidered from day one: [Redesign From First Principles](../principle-redesign-from-first-principles/SKILL.md).
- Retried, restarted, or partially failed operations need an explicit repeat-execution policy: [Make Operations Idempotent](../principle-make-operations-idempotent/SKILL.md).
- Concurrent actors may mutate the same file, branch, key, or state object: [Separate Before Serializing Shared State](../principle-separate-before-serializing-shared-state/SKILL.md).

### Simplicity and source quality

- Code or a proposed change adds traversal, hidden state, layers, abstractions, signal threading, asymmetry, or unnecessary lines: [Minimize Reader Load](../principle-minimize-reader-load/SKILL.md).
- An addition, refactor, or rewrite can delete complexity before construction: [Subtract Before You Add](../principle-subtract-before-you-add/SKILL.md).
- Owned source contains comments, docstrings, suppressions, or prose that should become structure: [No Comments](../principle-no-comments/SKILL.md).

### Change and delivery

- A planned rewrite or migration has explicit intermediate phases and a declared target state: [Outcome-Oriented Execution](../principle-outcome-oriented-execution/SKILL.md).
- A new internal API replaces an old one and callers can migrate together: [Migrate Callers Then Delete Legacy APIs](../principle-migrate-callers-then-delete-legacy-apis/SKILL.md).
- Multi-step work, sweeps, migrations, commits, or pull requests need coherent checkpoints: [Sequence Verifiable Units](../principle-sequence-verifiable-units/SKILL.md).
- Work is about to be declared complete or delegated output needs direct evidence: [Prove It Works](../principle-prove-it-works/SKILL.md).

### Diagnosis, leverage, and learning

- A bug, failed test, crash, or workaround needs root-cause diagnosis: [Fix Root Causes](../principle-fix-root-causes/SKILL.md).
- Repetitive, large, error-prone, or audit-sensitive work may justify a rerunnable artifact: [Build the Lever](../principle-build-the-lever/SKILL.md).
- Evidence shows a correction or instruction is recurring and should become an executable guardrail: [Encode Lessons in Structure](../principle-encode-lessons-in-structure/SKILL.md).

## Apply

1. Establish the requested outcome, scope, mode, repository constraints, and relevant evidence.
2. Select the smallest set whose triggers are concretely present.
3. Read each selected `SKILL.md` completely before using it.
4. Apply the specific leaves to the task. Do not manufacture findings to justify a loaded principle.
5. Trace suspected problems far enough to distinguish concrete cost from preference.
6. In Implementation mode, make only authorized changes and run proportionate direct verification.

## Resolve tension

- Required correctness, safety, boundary validation, and explicit contracts are not removable complexity.
- Redesign determines the right target shape; Minimize Reader Load and Subtract Before You Add seek the smallest clear route to that target.
- Experience First chooses among authorized, correct options; it does not invent product scope.
- Outcome-Oriented Execution may permit a scoped intermediate working state, while Sequence Verifiable Units still expects coherent verification boundaries and normally green commits.
- Build the Lever applies only when its reproducibility or risk reduction repays the extra artifact.
- Prefer the more specific triggered principle over a broad heuristic. When a real conflict remains, state the tradeoff instead of silently averaging the rules.

## Output

Return a compact receipt with:

- **Mode and scope.** What was assessed and whether edits were authorized.
- **Loaded.** Each principle and the concrete trigger that caused selection.
- **Applied.** Findings, decisions, or changes labelled with their principle IDs.
- **Near matches skipped.** Only close candidates whose omission might surprise the user.
- **Verification.** Direct evidence gathered, or material gaps.

For architecture work, classify recommendations as local, structural, or redesign. A structural or redesign recommendation should briefly cover ownership, data and invariants, contracts and dependency direction, control flow and side effects, migration, and verification.
