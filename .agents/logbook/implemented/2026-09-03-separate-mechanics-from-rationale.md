# Logbook: Separate Mechanics From Historical Rationale

Status: implemented
Kind: architecture

## Problem

Code can establish what a system does, but it rarely proves why a design was chosen. Combining those questions encourages plausible historical stories unsupported by evidence.

## Decision

Use `how` for current mechanics, ownership, boundaries, data flow, failure behavior, and placement. Use `why` for design lineage, incidents, rejected alternatives, business constraints, and data-backed thresholds. Use `teach` when both views should become one explanation.

For complex How requests, Luna `xhigh` Fast explorers cover independent system angles and Sol `high` synthesizes them. Narrow requests use Sol `medium` directly.

Why creates one Luna `xhigh` Fast investigator per available evidence category. It searches local Git at minimum and may use GitHub, Linear, and other declared project sources when callable. Fable 5.1 `xhigh` synthesizes all positive, negative, contradictory, and unavailable-source evidence. The parent verifies citations and calibrates confidence.

## Alternatives considered

- Infer intent from code shape. Rejected because implementation is evidence of mechanics, not motivation.
- Give one investigator every source. Rejected because source-specific searches benefit from parallelism and independently reported null results.
- Remove unused source playbooks. Rejected because they remain useful when a future project declares those systems in scope.
- Automatically search every available personal connector. Rejected to avoid unrelated data access; the declared project source profile controls scope.

## Evidence

- `skills/how/SKILL.md`
- `skills/why/SKILL.md`
- `skills/why/references/source-playbook.md`
- `skills/teach/SKILL.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Explanations must distinguish observed behavior from historical inference. Missing tools and failed searches remain evidence gaps rather than being rewritten as empty results. Repository Logbook records become a first-class source for Why while current behavior is still checked against code and tests.

## Revisit when

- The distinction routinely forces duplicate exploration without improving epistemic quality.
- A source connector cannot be used safely under project-scoped access rules.
- A smaller investigator topology produces equally complete evidence at materially lower cost.
