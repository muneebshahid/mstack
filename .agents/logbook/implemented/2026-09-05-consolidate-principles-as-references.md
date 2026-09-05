# Logbook: Consolidate Principles as Selective References

Status: implemented
Kind: simplification

## Problem

Twenty public principle skills and separate workflow routing tables repeat selection rules and overlapping guidance. Reducing discovery noise alone would leave that repetition, along with heuristics that can encourage unnecessary abstractions, deletion, or redesign.

## Decision

`apply-principles` is the single standards entry point, with ten selectively loaded references. Related guidance is merged while different questions remain explicit inside each topic: ownership versus dependency direction, concurrent writes versus repeat execution, and coordinated internal migration versus external compatibility.

Use task evidence to justify complexity and simplification. Keep useful boundaries regardless of implementation count, strengthen types for domain invariants, and compare designs only when a consequential choice remains unresolved. The initial consolidation retained the existing no-comments exceptions; [the subsequent wording and policy review](2026-09-05-tighten-principles-and-record-agent-work.md) records the user's stricter replacement and proactive typing requirements.

Callers select through the shared index and pass the relevant references to workers. They do not maintain independent catalogs or start another orchestration workflow to apply a standard. Paths resolve within the same MStack installation, independently of the consumer project's working directory. Existing Architect/Arena orchestration and model assignments are unchanged.

## Alternatives considered

- Move all twenty leaves unchanged first. This isolates packaging but leaves the requested simplification for another pass; the accepted scope combines the move with content consolidation.
- Put all guidance in one mandatory document. Rejected because unrelated detail would load for every standards question.
- Keep separate public leaves and workflow-specific selection tables. Rejected because the repeated discovery and routing are the problem being removed.

## Evidence

- [The shared index](../../../skills/apply-principles/SKILL.md) links all ten canonical references. The initial consolidation reduced 7,995 words in the old leaf files, including frontmatter, to 2,661 words in the references. The subsequent review records further reductions; these measure document size, not runtime context usage.
- `python3 scripts/validate.py` passes with 21 public skills, repository-relative links, packaged model profiles, launcher tests, and Logbook records. The bundled skill validator passes all 21 skills.
- `scripts/test_validate.py` uses a disposable Git repository to cover present tracked files, unstaged deletions, new files, and ignored files. It fails against the original enumerator and passes after filtering missing working-tree paths, allowing validation before staging a migration.
- A fresh reader answered four narrow scenarios covering redundant versus boundary validation, a useful single-implementation interface, concurrent jobs with retry ambiguity, and source-style exceptions. The decisions preserved those distinctions. No comparative production-model benchmark was run.
- This supersedes the separate-leaf packaging in [Principles Are the Canonical Engineering Standards](2026-09-03-principles-as-canonical-standards.md), while preserving canonical ownership of engineering rules.

## Consequences

The catalog and standards text are smaller. A combined reference can include nearby guidance that a task does not need, so selection remains conditional and distinct mechanisms stay identifiable. External integrations naming the removed public skills must migrate; the repository's active callers are updated. The subsequent policy review removes the temporary-sketch/scaffold comment exceptions; [Source Style](../../../skills/apply-principles/references/source-style.md) owns the current rule.

## Revisit when

- A merged topic repeatedly causes agents to confuse different failure mechanisms.
- Representative tasks load irrelevant references or miss required constraints.
- A removed instruction demonstrably prevented a failure that the concise guidance no longer prevents.
