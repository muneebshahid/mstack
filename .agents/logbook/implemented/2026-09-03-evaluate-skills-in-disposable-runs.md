# Logbook: Evaluate Skills in Disposable Runs

Status: implemented
Kind: simplification

## Problem

Reading a skill cannot establish that it selects the right workflow, delegates successfully, or produces useful results. The original evaluation workflow protected these distinctions but repeated them across four files and required an independent judge for every run.

## Decision

Keep [Skill Eval](../../../skills/skill-eval/SKILL.md) focused on realistic scenarios, predefined criteria, fresh runs, observed evidence, and a consistent report. Use agent judgment for scenario count, repetition, and independent judging; prefer an independent judge for subjective comparisons of revisions the evaluator authored. Evaluation leaves installed skills and live systems unchanged.

Compare complete skill versions under matching conditions and verify which version each candidate read. Distinguish automatic selection from explicitly loaded execution. Cheap model assignments test mechanics; output-quality judgments use the skill's assigned models. Preserve failures, uncertainty, and meaningful ties.

Keep the evaluator in the parent. The [execution reference](../../../skills/skill-eval/references/scenario-runs.md) selects a native candidate when its available tools and remaining nesting depth support the task. Otherwise, the evaluator launches a fresh top-level harness process. Its agent tree is separate from the desktop task's tree. Do not encode a universal nesting limit or change configuration to make a test pass.

Merge reporting into four sections in the main skill and remove the separate report and judge templates. Keep only the execution reference for discovery, permissions, delegation, and session-lifecycle details.

## Alternatives considered

- Require independent judging for every run: removed because direct evidence can settle simple execution checks; use a judge when requested or useful.
- Move the old instructions into references: rejected because this would preserve the duplication and overhead.
- Test an appended diff or modify the installed skill temporarily: rejected because neither reliably isolates complete versions.
- Always launch candidates in a separate CLI: rejected because native candidates suffice when their tools and delegation depth support the workflow.
- Assume Codex and Claude have identical nesting limits: rejected based on the host probe and current Claude documentation.

## Evidence

The initial record reconstructed the evaluation design from the installed stack. The parent later consolidated the main workflow and references, updated the README description, and retained existing model assignments and invocation policy.

A fresh Codex desktop Luna `low` child inspected its callable and deferred tools and reported no native spawn operation. It did not create a descendant or substitute a desktop task. The parent closed it after completion. The native tool could not request the configured Fast tier, so that setting is unverified. This establishes the observed desktop-child limitation, not a universal Codex CLI limit.

The installed Claude Code version was 2.1.257. [Current Claude documentation](https://code.claude.com/docs/en/sub-agents#let-subagents-spawn-their-own-subagents) describes three nested subagent layers by default and a configurable depth limit. This was a documentation check, not a live Claude nesting trial. No harness configuration was changed.

Fable reviewed the original and shortened instructions through Consult, with `claude-fable-5-1` verified and `max` requested; Claude effort is not independently verified. It approved the simplification with two proposed requirements. The parent accepted reading the execution reference before launching and clarified that tool availability must be checked at the candidate's depth. The parent narrowed mandatory independent judging for every self-authored revision to a preference for subjective comparisons, because deterministic execution evidence need not incur another model call. Duplicate authority, activation, and agent-ID instructions were removed. Existing source and reference links, skill structure, repository hygiene, and Logbook validation passed. This was an authoring review and capability probe, not a comparative behavioral evaluation of the two Skill Eval versions. Temporary consultant prompts, reports, and logs were removed after recording these findings.

## Consequences

The skill remains useful for both execution checks and comparisons while avoiding a mandatory judging pipeline. A capability failure can leave a criterion untested. Explicitly loading a skill does not prove automatic selection, and a separate harness process does not prove desktop-level agent integration.

## Revisit when

- Harness tools or nesting limits change.
- Repeated runs show misleading conclusions from the reduced instructions.
- A recurring evaluation needs stronger sampling or independent judgment.
