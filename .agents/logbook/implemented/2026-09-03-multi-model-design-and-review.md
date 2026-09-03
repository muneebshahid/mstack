# Logbook: Use Model Diversity for Consequential Design and Review

Status: implemented
Kind: architecture

## Problem

A single frontier model can produce strong work but still has stable blind spots. Assigning several copies of one model different personas does not provide the same independent pressure as genuinely different model families.

## Decision

Use multi-model panels only where a wrong result is consequential enough to repay their cost.

`arena` uses Claude Fable 5.1 `xhigh` and GPT-5.6 Sol `xhigh` for independent candidate artifacts, then a separate Sol `xhigh` cross-judge. The parent reads every candidate, selects the base, grafts only compatible strengths, and produces the final synthesis.

`interrogate` replaces a separate general code-review workflow. Fable 5.1 `max` and Sol `max` receive the same diff, intent, rubric, and selected principles. The parent verifies high-severity claims against reachable code, deduplicates by causal defect, and classifies findings rather than aggregating every suggestion.

How's critique mode uses Fable 5.1 `xhigh` and Sol `xhigh` after first establishing how the subsystem currently works.

## Alternatives considered

- Use only one frontier model. Retained for ordinary work but rejected for explicitly adversarial or consequential design tasks.
- Give reviewers different personas. Rejected because differing prompts confound model diversity and make agreement less meaningful.
- Keep a separate code-review skill beside Interrogate. Rejected because the useful local, staged, and pull-request scoping behavior can live in Interrogate without duplicating review standards.
- Let the model judge choose the final result. Rejected because the parent has the broadest task and repository context.

## Evidence

- `skills/arena/SKILL.md`
- `skills/interrogate/SKILL.md`
- `skills/interrogate/references/lead-judgment.md`
- `skills/how/SKILL.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Panels cost more and should not run automatically for mechanical work. All candidates or reviewers receive the same substantive prompt. Dropouts, capability failures, unexpected mutations, disagreement, and degraded operation remain visible.

## Revisit when

- Evaluation shows one panel member adds little independent signal.
- Model availability or slugs change.
- Native Codex and Claude execution boundaries gain materially different isolation or persistence guarantees.
