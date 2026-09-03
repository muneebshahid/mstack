---
name: skill-eval
description: "Evaluate an existing Codex skill against realistic scenarios, or compare its current form with a proposed revision. Use for skill evaluation, behavioral regression checks, validating that a skill triggers and executes correctly, or deciding whether a skill change should be promoted."
---

# Skill Eval

Evaluate behavior, not prose in isolation. Run an existing skill in fresh, realistic contexts, inspect what it actually did, and report concrete execution issues. When a revision is proposed, test the complete current and proposed skill under the same conditions and recommend whether to promote the change.

## Boundary

Skill Eval does not create new skills. If the target skill does not exist, resolve and use the bundled `skill-creator` from the advertised skill roots, then stop this workflow.

Evaluation does not authorize installing or modifying the target skill. Keep the installed skill unchanged. Temporary full-skill snapshots, fixtures, prompts, and run artifacts must stay outside the repository and installed skill directories. Remove them after preserving the findings and candidate diff unless the user asks to inspect them.

Run scenarios only in disposable workspaces. Do not mutate a live repository, external system, ticket, pull request, deployment, or user data merely to evaluate a skill.

## 1. Resolve and inspect the target

Resolve a named skill to its installed directory, preferring the current user's Codex skill root and then other advertised skill roots. Read its `SKILL.md` completely. Read supporting resources that define the behavior being exercised, plus `agents/openai.yaml` when present.

Resolve the bundled `skill-creator`, then run its `scripts/quick_validate.py` in an environment with PyYAML. Its scope is limited to `SKILL.md` structure and unfinished markers. Separately inspect `agents/openai.yaml`, linked resources, referenced scripts, and dependency paths; do not imply that the bundled validator checked them. Record structural failures separately from behavioral findings. Structural validity is not evidence that the skill works.

Extract the observable contract:

- The requests that should and should not activate it.
- Its promised outcome and output shape.
- Required skills, references, tools, agents, models, and effort settings.
- Read/write authority and prohibited side effects.
- Required evidence, verification, degradation, and failure behavior.

## 2. Choose the fidelity profile

Classify the evaluation before staging or running it.

- **Execution smoke test:** Use when the question is whether the skill activates or executes its workflow mechanics: reading dependencies, spawning the required agents, retaining identities, invoking tools, producing artifacts, respecting authority, or failing correctly. Read [MStack runtime model resolution](../setup-mstack/references/runtime-resolution.md), resolve `skill_eval_smoke_candidate` and `skill_eval_smoke_judge`, and use those assignments only in complete temporary staged copies and launch arguments. Apply the same substitutions to both arms. Record every substitution and do not claim that production-model output quality was evaluated.
- **Quality evaluation:** Use when judging architecture, review accuracy, synthesis, instruction quality, model choice, model provenance, or any result whose correctness depends materially on reasoning quality. Run the target skill's actual resolved assignments and resolve `skill_eval_quality_judge` for independent judgment. Use this profile whenever the distinction is uncertain.

Never change an installed skill to obtain the smoke-test profile. Apply substitutions only to complete temporary skill and dependency snapshots plus their launch arguments. Cleanup removes those snapshots, leaving the installed production configuration unchanged. Do not substitute the model when model selection, effort, service tier, alias resolution, or verified provenance is itself under evaluation. Do not run a Haiku smoke assignment in Claude plan mode; verify the served model before accepting the run as cheap-profile evidence.

## 3. Materialize a proposed revision when present

When the user proposes a change, create two complete temporary snapshots:

- The installed current skill.
- The current skill with the proposed revision applied.

The proposed snapshot must be a complete runnable skill directory, not a diff or an instruction layered over the current skill. Keep every dependency and fixture identical between the two arms. If the requested revision requires authoring judgment, use the unchanged bundled `skill-creator` against the temporary proposed snapshot. If the user supplied an exact edit, apply that edit to the snapshot directly.

Validate both snapshots before behavioral runs. If the proposed snapshot is structurally invalid, report the defect; do not weaken the validator or evaluate a shape that cannot load.

## 4. Frame realistic scenarios

Read [references/scenario-runs.md](references/scenario-runs.md) completely.

Choose the smallest set of scenarios that can test the claim, normally one to three:

- At least one organic positive request exercising the skill's main outcome.
- One adjacent negative request when activation or over-triggering is material.
- A focused pressure, missing-capability, failure, or authority scenario only when the skill claims behavior for it or the proposed change could affect it.

Before running anything, write three to six concrete rubric criteria. Grade observable decisions, traces, artifacts, mutations, and results. Do not ask candidates to name the skills, principles, or files they used, and do not score expected phrases in their final prose.

For a proposed revision, run the exact same scenarios, fidelity profile, model, effort, tools, fixture, and repository instructions against both complete snapshots. Change only the target skill. For evaluation without a revision, run the current skill alone against the same kind of predeclared contract.

## 5. Run blind

Candidate runs must look like ordinary user work. They must not see evaluation vocabulary, the rubric, other arms, expected findings, or the authoring discussion. Use neutral, project-shaped paths and labels.

Use fresh contexts. Do not fork the current conversation or reuse an authoring agent. Capture the final result and, when exposed by the harness, the actual tool trace, skill and reference reads, model and effort, file changes, capability failures, exit status, and usage. Stream live-only events into a parent-side record outside the candidate-visible workspace when possible; otherwise quote the material event sequence in the report and label the absence of a durable raw trace.

Before launching, search the complete callable tool catalog, including deferred tools, for the capability under evaluation. Choose the candidate boundary from the target skill's execution shape:

- **Leaf candidate:** use the host-native multi-agent tool to start a fresh Codex context.
- **Orchestration candidate:** when the target skill must itself spawn native agents, launch the staged candidate through the top-level process boundary required by its resolved runner in its disposable Git repository. The evaluator owns this process boundary; the candidate must use its native agent tools for delegation and must not launch another copy of its own harness. For Codex this is `codex exec --ephemeral --json`. Pass the fidelity profile's exact candidate model and effort on the command line.

An isolated top-level process evaluates native agent behavior within that candidate session. It does not prove integration with the calling desktop task, whose agent tree cannot address the candidate's children. Do not use it when that app-level relationship is itself under evaluation.

Native identity, persistence, messaging, waiting, resumption, and closing behavior may pass only when the captured JSON trace contains the native operation, a non-empty returned agent identifier, and subsequent operations against that exact identifier. Preserve the candidate thread identifier, exit state, stderr capability warnings, and material lifecycle events. If the selected boundary is unavailable or fails, stop before writes and mark the affected behavior **Unexercised** or failed according to the rubric; do not replace it with prose simulation.

Distinguish activation from execution:

- An organic prompt can test routing only when the trace identifies the loaded skill path or content hash. An isolated catalog additionally tests that the staged copy was selected.
- Explicitly attaching the skill by path tests execution only. Never claim that automatic routing passed after force-loading the skill.

If an identically named installed copy remains visible, record every visible copy and verify which one was read. For a current-skill evaluation, a byte-identical duplicate can support an automatic-routing result but not a project-local-selection result. For a revision comparison, each arm must read its exact staged snapshot; otherwise the comparison is **Inconclusive**.

If the harness cannot test one branch faithfully, mark it **Unexercised**. Do not replace missing runtime evidence with static confidence.

Run one sample per scenario by default. Repeat only when the result is inconsistent, close enough that stochastic variation could change the decision, or the user requests a stronger measurement campaign.

## 6. Judge and verify

Read [references/judge-prompt.md](references/judge-prompt.md) completely.

Use the resolved smoke or quality judge as the independent blinded judge. Give it the rubric, neutral labels, complete outputs, captured traces, and artifact paths, but not model identities or which arm is current. For a revision, both arms must be judged together in one pass on one scale. For a current-skill evaluation, judge the single run against the declared contract and ask for concrete issues. If the assignment uses `claude-code`, read and use [Claude Code](../claude-code/SKILL.md) with the resolved model and effort.

Before launching the judge, create one common temporary evidence root containing the rubric, neutral candidate outputs, traces, and every artifact the judge must inspect. Resolve every referenced path and verify that the configured judge can read it. Copy required evidence into the common root under neutral names when it is elsewhere; fail the judge preflight rather than launching with unreadable evidence. For a `claude-code` judge, every path must be beneath either this evidence root or the Codex skills directory exposed by the Claude launcher; run Claude with the common evidence root as its working directory. Put process output outside the readable root so model provenance, logs, and other parent-only metadata cannot compromise blind judgment. Pass absolute paths and preserve the preflight result in the evaluation evidence.

If the selected judge is unavailable, preserve the capability failure and let the parent perform the rubric-level judgment; label the evaluation degraded. Do not silently substitute another judge.

The parent retains final judgment. Read every output and material artifact, verify trace-based claims, reject judge preferences unsupported by the rubric, and treat a close or mixed result as a tie rather than manufacturing a winner.

## 7. Report and clean up

Use [references/report-template.md](references/report-template.md). Separate:

- Structural findings.
- Observed behavioral findings.
- Activation results versus force-loaded execution results.
- Capability failures and unexercised branches.
- Comparison findings when a revision exists.
- The selected fidelity profile and every temporary model, effort, or service-tier substitution.

For a proposed revision, recommend **Promote**, **Revise**, **Reject**, or **Inconclusive**. This recommendation does not apply the change. Preserve the complete proposed diff, scenario definitions, configuration, material trace excerpts, hashes, and findings in the report, then remove temporary skill snapshots and disposable workspaces unless the user asked to retain them. Report an evidence path only when that path was intentionally retained; otherwise say it was removed.
