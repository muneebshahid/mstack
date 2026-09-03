---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Spawn Claude Fable 5.1 max and GPT-5.6 Sol max to adversarially review code changes. Each model gets the same prompt and rubric. The adversarial signal comes from model diversity, not assigned personas. Models differ in blind spots, priors, and reasoning patterns. Agreement across models is high-confidence signal; lone-model findings are worth reading but lower confidence.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Resolve one canonical review target from the user's request and repository state:

- Explicit files or supplied diff: review exactly that target plus necessary surrounding context.
- Working tree: distinguish unstaged, staged, and relevant untracked files. Include an untracked file only when it belongs to the intended change.
- Commit or range: resolve the exact revisions before packaging the diff.
- Feature branch: determine the actual base from the user, pull-request metadata, upstream configuration, or repository default branch, then use the merge base. Never silently assume `main`.
- Pull request: resolve its number, base, head, revision, description, and diff through `gh` when available. Preserve and report an access failure rather than substituting a guessed local range.

Create a compact scope manifest naming the target, base and head or working-tree surfaces, included paths, excluded surfaces, and any unresolved gap. Capture one exact diff or file package and give that same package to both reviewers. If it is empty, wrong-base, or changes before synthesis, stop or report the drift rather than silently mixing scopes.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly and gather available requirements. What is this code trying to accomplish? Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- An accepted plan, architecture handoff, issue, or explicit acceptance criteria
- The code itself

Write one clear intent paragraph and a compact requirements context. Reviewers challenge whether the work achieves the intent and explicit requirements well, not whether the intent itself is correct. If intent is materially ambiguous, ask the user before proceeding. A missing plan is not a blocker when the request and code establish the intended outcome.

## Step 3, Spawn Reviewers

Launch both reviewers concurrently.

| Reviewer | Execution |
|----------|-----------|
| Reviewer A | Claude Fable 5.1, max, through the `claude-code` skill |
| Reviewer B | GPT-5.6 Sol, max, through Codex's native subagent tool |

Read [references/principle-routing.md](references/principle-routing.md) in full. Resolve the core and concretely triggered conditional principles to absolute filesystem paths, then read every selected `SKILL.md` completely. Interrogate selects these leaves directly; do not invoke `apply-principles` inside the panel.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The frozen scope manifest
2. The stated intent
3. The requirements context
4. The exact diff or file package
5. The review rubric from `references/rubric.md`
6. The ordered list of absolute selected principle skill paths

Prepend this execution guard:

> You are one reviewer in an already-running two-model panel. Read every explicitly provided principle skill and apply it under this read-only review assignment. Do not invoke orchestration skills, delegate, spawn subagents, or modify files. Inspect the supplied code and return only your independent review.

The same filled template goes to both reviewers, so every model applies the same selected principles. Provide filesystem paths rather than copying the skills into the prompt. Include applicable repository instructions because Fable runs without project customizations. Keep secrets and unrelated content out of the prompt.

Before launching, record the repository's current `git status --short` so unexpected mutations can be detected.

Confirm that both launch mechanisms are callable before describing the panel as started: a managed process launcher for Fable and a native subagent spawn tool for Sol. An absent mechanism means that reviewer failed to launch.

1. Read [the Claude Code skill](../claude-code/SKILL.md) in full. Write the filled prompt to a temporary file outside the repository, create a temporary output directory, and invoke its launcher with `--model claude-fable-5-1 --effort max` in a managed terminal session. Retain the returned process or session identity before claiming Fable is running, then yield so orchestration can continue.
2. Immediately invoke Codex's native subagent spawn tool with `model: gpt-5.6-sol`, `reasoning_effort: max`, and no inherited conversation context. Give it the exact same filled prompt. This is a subagent of the current task, not a new user-owned task. The spawn call itself must appear in the execution trace and return a non-empty native reviewer identifier. Surface that exact identifier in the next progress update and retain it before claiming Sol is running.
3. Let both reviewers run concurrently. Wait on the retained Sol identifier through the native agent wait tool and monitor Fable through its terminal session. Never issue an empty wait, infer an orphaned reviewer, or treat an attempted launch as a running reviewer. Avoid repeated unchanged polls.
4. When Fable exits, read `claude.result.md` and `summary.json` from its output directory. Use the native Sol agent's completed final message as Sol's review.
5. Recheck `git status --short`. If the review changed the repository, do not accept, revert, or hide the changes automatically. Report the unexpected mutation and exclude any result that violated the read-only assignment.

If either launch is not invoked, fails, or returns no usable process or reviewer identifier, record that reviewer as failed immediately and do not wait on it. A never-launched reviewer counts as failed when deciding whether one or both reviewers failed. If one reviewer fails, inspect its failure once. Do not repeatedly retry authentication, quota, model-availability, configuration, or missing-identifier failures. Use the surviving review, label the panel degraded, and report the missing reviewer. If both fail, stop and report the concrete blockers. Close a completed native reviewer after capturing its report.

Each reviewer produces structured findings as described in the prompt template.

## Step 4, Synthesize

As results come back, build a unified picture:

1. **Parse all findings** from the reviewers
2. **Identify consensus**. Findings raised by 2+ models independently are highest signal.
3. **Identify lone-model findings**. Still worth reading, but weight accordingly.
4. **Classify the finding type** as introduced defect, relevant pre-existing defect, test gap, or residual risk.
5. **Deduplicate conservatively**. Merge findings only when they share the same underlying cause and affected execution path; similar symptoms alone are insufficient. Preserve every reviewer-local ID and model attribution.
6. **Assign stable IDs** to synthesized findings in order of severity and source location: `INT-001`, `INT-002`, and so on. Use these IDs throughout the verdict.
7. **Note disagreements**. If one model flags something and another explicitly says the opposite, preserve that disagreement.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework. Reviewers only see a slice of the codebase. You have the full context (the goal, the constraints, the timeline, which tradeoffs were already considered). Use that context aggressively.

Before categorization, independently validate every proposed **Act on** finding against the actual code and reachable execution path. Do the same for every `critical` finding raised by only one reviewer. Verify its source location, preconditions, consequence, and whether existing callers, validation, types, or tests already prevent it. An unverified high-severity claim cannot be **Act on**; preserve it as a lower-confidence risk or dismiss it with the evidence gap.

Categorize every finding using these buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Its stable `INT-NNN` ID and finding type
- Its verified source location
- Which model(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Scope
[The frozen target, included and excluded surfaces, and any access or drift gap.]

### Reviewers
- Reviewer [label]: [model name], [process or native identifier, or failed before identity], [N findings] (one bullet per reviewer)

### Act On
[Findings that should be addressed. For each: stable ID, type, verified location, description, which models raised it, and why it matters.]

### Consider
[Findings worth thinking about. For each: description, which models raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale. This shows the user what was filtered out and why, so they can override your judgment if they disagree.]

### Agreement Map
[Where did models agree, where did they diverge, and what does the pattern of agreement/disagreement tell us?]
