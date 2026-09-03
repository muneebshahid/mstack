# Logbook: Evaluate Skills in Disposable Runs

Status: implemented
Kind: testing

## Problem

Reading a skill file cannot establish that it activates correctly, invokes the required agents, preserves identities, respects authority, or produces the promised artifact. Testing proposed changes directly in the installed skill would contaminate both the control and the user's environment.

## Decision

`skill-eval` evaluates existing skills only. New skills remain the responsibility of the bundled `skill-creator`.

Evaluation without a revision runs the current skill against realistic acceptance criteria. Evaluation with a proposed revision creates complete temporary current and proposed snapshots, runs matched scenarios, and compares observed behavior. Candidate work occurs in disposable Git repositories and temporary skill roots; the installed skill remains unchanged.

Use host-native fresh subagents for leaf skills. When the skill under test must itself spawn native agents, use one top-level ephemeral `codex exec --json` candidate process inside the disposable repository. That candidate may use native subagents but must not launch another Codex process.

Execution smoke tests use dedicated cheap roles rather than production assignments. The packaged `multimodel` and `codex` profiles map both candidate and judge to Luna `low` with Fast; the `claude-code` profile maps both to Haiku `low`. Quality evaluation uses the production models and settings. A blinded judge reads one common temporary evidence root; launcher metadata stays outside that root so it cannot reveal candidate identity.

## Alternatives considered

- Compare a task with and without a newly created skill. Rejected; new-skill creation and initial testing already belong to `skill-creator`.
- Inject only proposed prose into an evaluator prompt. Rejected because it does not test a complete loadable skill and can hide dependency effects.
- Modify the installed skill and roll it back. Rejected because failure or concurrency could leave the real installation changed.
- Use `codex exec` for every candidate. Rejected because native subagents provide the correct boundary for leaf behavior; the external process is reserved for testing nested orchestration.

## Evidence

- `skills/skill-eval/SKILL.md`
- `skills/skill-eval/references/scenario-runs.md`
- `skills/skill-eval/references/judge-prompt.md`
- `skills/skill-eval/references/report-template.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Smoke tests can establish workflow mechanics without spending production-model budgets, but they must not claim production output quality. Native lifecycle behavior passes only with trace evidence containing real identifiers and subsequent operations against them. Missing capabilities remain failed or unexercised branches rather than prose simulations.

## Revisit when

- The desktop host exposes nested native subagents directly to an evaluation child.
- Trace formats change and no longer expose identities or lifecycle operations.
- Repeated smoke tests show that temporary model substitution changes the orchestration behavior being measured.
