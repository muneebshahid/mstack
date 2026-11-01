---
name: review
description: "Review code changes, subsystems, or designs against their requirements. Use for code review, adversarial or multi-model review, and focused reviews of simplicity or test usefulness."
---

# Review

Find problems worth fixing within the requested scope. Review read-only and return a verdict. No findings is a valid result.

## Scope

Establish the intended behavior from the request, plan, issue, PR, or project evidence; consult project instructions, Git history, discussions, or Logbook records when they could resolve a claim.

Resolve the exact target: paths or artifact; staged, unstaged, and untracked changes; exact revisions; or base and head for a branch or PR, using the merge base and never guessing `main` or substituting a local range for an inaccessible PR. State access gaps.

## Review

Honor explicit requests for adversarial or multi-model review; invoking this skill alone does not require a panel.

Use [Apply Principles](../apply-principles/SKILL.md) and [Review criteria](references/rubric.md) as needed.

For a panel, use [Delegate](../delegate/SKILL.md) for `review_reviewer_a` and `review_reviewer_b`: give both the same filled [Reviewer prompt](references/reviewer-prompt.md) (scope, requirements, findings, snapshot, project instructions, criteria, reference paths; no secrets or unrelated content), launched concurrently in fresh contexts. Exclude reports from reviewers that edited the repository. Report what ran, any substitutions, and limits; do not present an incomplete requested panel as complete.

## Judge findings

Check findings against requirements, evidence, known constraints, and recorded decisions. Verify claims regardless of how many reviewers raised them.

Before accepting a finding, verify its location, reachable path, preconditions, and consequence. Check callers, types, validation, and tests for evidence that rules it out. For unimplemented designs, distinguish requirement conflicts from assumptions needing runtime evidence.

Group findings by cause without losing distinct defects; keep reviewer attribution and label pre-existing issues.

- **Act on:** verified problems worth fixing under the requirements.
- **Consider:** plausible concerns with an unresolved assumption or tradeoff. State what would settle them.
- **Dismiss:** incorrect, unsupported, or out-of-scope suggestions. Explain why.

A common repository pattern can still contain a defect.

## Response

Use these headings as the default report structure, adapting detail to the task:

### Verdict

State whether justified findings remain. Summarize the intent, scope, and review mode: direct, complete panel, or degraded.

### Findings

Order by impact. Include Act on / Consider, location, evidence, consequence, a suggested correction if known, and tracking IDs when used. Label pre-existing issues and attribute panel findings.

### Rejected suggestions

List rejected findings and reasons, grouping duplicates. Preserve substantive disagreements.

### Verification and limits

Report what you inspected or ran, unresolved risks, access or scope gaps, and panel models.
