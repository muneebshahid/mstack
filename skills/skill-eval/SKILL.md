---
name: skill-eval
description: Evaluate an existing skill or compare revisions using realistic runs and observed results.
---

# Skill Eval

Check whether a skill works and whether a revision improves it. Use judgment on scenarios, repetition, and independent review.

Evaluation does not authorize changing the installed skill or live systems. Run in disposable workspaces; prepare revisions as temporary copies.

## Frame

Read the target skill and relevant resources. Choose a few realistic scenarios and define success before running them.

Resolve models through [model configuration](../setup-mstack/references/runtime-resolution.md): use `skill_eval_smoke_candidate` for execution checks and the skill's assigned models for output quality. Apply smoke substitutions only to temporary copies and launch arguments. Report them; a cheap run does not establish production-model quality.

## Run

Use fresh candidate contexts with ordinary task prompts, without the rubric or authoring discussion. Read [Running candidates](references/scenario-runs.md) before launching candidates.

For comparisons, stage complete versions with their dependencies and hold the scenario, model settings, tools, and fixture constant. Verify which version each candidate actually read.

Capture outputs and the tool activity, artifacts, and failures needed to assess the criteria. If the chosen environment cannot exercise a behavior, report it as untested.

## Assess

Judge against the original criteria using observed evidence. Keep failures visible and allow ties; repeat when uncertainty could change the conclusion.

Prefer an independent judge for subjective comparisons of revisions you authored; otherwise use one when useful or requested. Resolve `skill_eval_smoke_judge` or `skill_eval_quality_judge` and use [Consult](../consult/SKILL.md) for external assignments. Give the judge the criteria and accessible evidence with neutral version labels. Omit model identities and the preferred outcome. The parent checks its reasoning and decides what to accept.

## Report

Use these sections, keeping each as short as the findings allow:

- **Scope:** skill/version, scenarios, criteria, and requested/served models; execution or quality check.
- **Results:** outcomes, supporting evidence, meaningful differences, failures, and untested behavior.
- **Recommendation:** works, needs changes, or inconclusive; for comparisons, identify improvements, regressions, or ties.
- **Reproduction:** prompts, relevant settings, revision diff or version identifiers, and retained evidence paths.

Preserve the findings, then remove temporary workspaces, prompts, and outputs unless the user wants to inspect them.
