---
name: review
description: "Review code changes, subsystems, or designs against their requirements. Use for code review, adversarial or multi-model review, and focused reviews of simplicity or test usefulness."
---

# Review

Find problems worth fixing within the requested scope. Review read-only and return a verdict. No findings is a valid result.

## Scope

Establish the intended behavior from the request, plan, issue, PR, or project evidence. Read applicable project instructions; consult Git history, discussions, or Logbook records when they could resolve a claim.

Resolve the target:

- Files, subsystem, or design: identify the paths or artifact and necessary context. Existing designs need no introducing diff.
- Working tree: distinguish staged, unstaged, and relevant untracked changes.
- Commit or range: resolve exact revisions.
- Branch or PR: establish base and head from the request, PR metadata, or repository configuration. Use the merge base for a branch diff. Do not guess `main` or substitute a local range for an inaccessible PR.

Record the target, revisions, inclusions, exclusions, and access gaps. Capture one diff or file snapshot. Report an empty diff as no changes to review. If the target changes, refresh affected evidence or state the resulting limit.

## Review

Explicit skill invocations and requested adversarial or multi-model reviews use two independent reviewers. Handle other reviews directly, including focused tests-only or simplicity-only requests. Keep the requested focus.

The parent uses [Apply Principles](../apply-principles/SKILL.md) to select and read relevant references, then reads [Review criteria](references/rubric.md).

For a panel:

1. Resolve `review_reviewer_a` and `review_reviewer_b` through [model configuration](../setup-mstack/references/runtime-resolution.md). Follow each runner's instructions.
2. Fill [Reviewer prompt](references/reviewer-prompt.md) with the scope, requirements, snapshot, project instructions, criteria, and selected reference paths. Exclude secrets and unrelated content. Launch both reviewers concurrently in fresh contexts with the same prompt.
3. Retain process or agent identifiers and monitor completion. Capture reports and available model provenance before closing reviewers. Keep external artifacts outside the repository.
4. Compare repository status and diffs before and after review. Report unexpected edits and exclude reports from reviewers that violated the read-only assignment. Do not silently keep or revert their edits.

Report launch and access failures. Do not substitute models or repeatedly retry unavailable runners. With one usable report, label the verdict degraded. With none, report the blockers without claiming a completed review.

## Judge findings

Check findings against requirements, evidence, known constraints, and recorded decisions. Verify claims regardless of how many reviewers raised them.

Before accepting a finding, verify its location, reachable path, preconditions, and consequence. Check callers, types, validation, and tests for evidence that rules it out. Investigate critical claims even from one reviewer. For unimplemented designs, distinguish requirement conflicts from assumptions needing runtime evidence.

Merge findings only when they share a cause and affected path. Retain reviewer attribution and local IDs; assign stable `REV-NNN` IDs. Distinguish introduced defects from relevant pre-existing issues.

- **Act on:** verified problems worth fixing under the requirements.
- **Consider:** plausible concerns with an unresolved assumption or tradeoff. State what would settle them.
- **Dismiss:** incorrect, unsupported, or out-of-scope suggestions. Explain why.

Check proposed fixes against the simplicity and test criteria too. Prefer the smallest correction that preserves required behavior. A single implementation does not make a boundary unnecessary; a common repository pattern can still contain a defect.

## Response

Use these headings and keep empty sections brief:

### Verdict

State whether justified findings remain. Summarize the intent, scope, and review mode: direct, complete panel, or degraded.

### Findings

Order by impact. Include ID, Act on / Consider, location, evidence, consequence, and a suggested correction if known. Label pre-existing issues and attribute panel findings. Say "No justified findings" when appropriate.

### Rejected suggestions

List rejected findings and reasons, grouping duplicates. Preserve substantive disagreements.

### Verification and limits

Report what you inspected or ran, unresolved risks, access or scope gaps, and panel models. Distinguish reading tests from running them. Keep process identifiers and detailed provenance in the review record.
