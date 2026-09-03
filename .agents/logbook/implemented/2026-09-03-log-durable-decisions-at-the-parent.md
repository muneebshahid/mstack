# Logbook: Log Durable Decisions at the Parent

Status: implemented
Kind: process

## Problem

Code and ordinary documentation show the current state but often lose why a direction won, what was rejected, and what evidence should cause maintainers to revisit it. Allowing every worker to write decision records would create noisy or conflicting history.

## Decision

Keep repository-local records under `.agents/logbook/` with explicit `proposed`, `implemented`, and `rejected` lifecycle states. Record durable architecture, behavior, bug-fix, simplification, process, and testing decisions when future maintainers could otherwise relitigate them.

During `implement`, only the parent decides whether a decision deserves a record and writes or updates it. Luna may include rationale, alternatives, and evidence in its unit report, but it does not edit the Logbook. Failed exploratory units are evidence only; they do not become implemented decisions unless the parent adopts a resulting direction.

## Alternatives considered

- Put rationale in source comments. Rejected because completed owned source follows the no-comments principle and historical context ages poorly beside code.
- Let implementation workers update the Logbook directly. Rejected because the parent owns final judgment and can distinguish a local implementation choice from a durable project decision.
- Record every action. Rejected because a chronological diary would obscure decisions worth preserving.

## Evidence

- `skills/logbook/SKILL.md`
- `skills/logbook/references/record-format.md`
- `skills/implement/SKILL.md`
- `skills/implement/references/implementation-worker.md`
- `skills/principle-no-comments/SKILL.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Why investigations can use decision records as evidence while checking current mechanics against code and history. Repository changes that establish a durable decision should update the record in the same implementation unit when practical. The Logbook remains curated rather than exhaustive.

## Revisit when

- Records become stale more often than they answer recurring questions.
- Multiple agents need concurrent authorship and a structural ownership mechanism exists.
- A project already has an authoritative decision-record system that should replace this layout.
