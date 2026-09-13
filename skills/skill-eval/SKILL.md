---
name: skill-eval
description: Evaluate existing or proposed skill instructions and compare variants through realistic runs.
---

# Skill Eval

The parent defines success, launches scenarios, and assesses evidence before adoption.

## Prepare

Choose realistic tasks and success criteria. Keep variants and proposed role assignments in context; do not write skill files for evaluation.

Select each scenario's model, effort, and Fast setting. Use `skill_eval_smoke_candidate` for mechanics; explicitly choose models for quality evaluation. Keep production settings unchanged; cheap runs do not establish production-model quality.

Include the active profile and new or overridden roles in the brief. Resolve missing assignments before launch; proposed roles need not be saved.

## Run

Launch each scenario/version through [Delegate](../delegate/SKILL.md) in a fresh external process, even for natively available models. See [Running scenarios](references/scenario-runs.md).

Provide the task, complete variant, sources, dependencies, and model assignments. Omit the grading rubric, preferred answer, and authoring discussion. The process executes the skill directly, without another candidate layer.

Set `allow_subagents=true` when needed; children default to false. Limit authorized writes to disposable workspaces.

Hold tasks, model settings, tools, and fixtures constant across variants; record intentional differences. Collect outputs, tool activity, artifacts, and failures.

## Assess

Assess results against the criteria, including failures and ties. Repeat only when uncertainty could change the conclusion.

Use an independent judge when useful or requested, especially for subjective comparisons of your own revisions. Delegate to `skill_eval_smoke_judge` or `skill_eval_quality_judge`. Provide criteria and evidence under neutral variant labels; omit model identities and the preferred outcome. Check the judge's reasoning.

## Report

- **Scope:** scenario, variant, assignments, requested/served models, and mechanics or quality evaluation.
- **Results:** outcomes, evidence, differences, failures, and untested behavior.
- **Recommendation:** adopt, revise, or inconclusive, with reasons.
- **Reproduction:** exact variant text, inline assignments, prompts, settings, and retained evidence paths.

Save the report; remove temporary artifacts unless the user wants to inspect them. Update skills and configuration only after the user selects a variant.
