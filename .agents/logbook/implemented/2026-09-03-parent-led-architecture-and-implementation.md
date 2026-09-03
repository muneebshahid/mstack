# Logbook: Parent-Led Architecture and Worker-Owned Implementation

Status: implemented
Kind: architecture

## Problem

Consequential code changes need independent design pressure and cheaper implementation capacity without surrendering scope, architecture, or verification to a chain of autonomous agents.

## Decision

Use `implement` as the single code-changing workflow. The parent agent chooses the mode, grounds the task, selects principles, decides whether `architect` is needed, decomposes work, checks every diff and behavior result, and retains final judgment.

`architect` is read-only. It grounds the current system and invokes `arena` for competing designs. Its handoff names load-bearing constraints, adaptable details, invalidation signals, and a first implementation unit that tests the highest-risk assumption when practical.

One persistent GPT-5.6 Luna worker at `high` effort and Fast service writes project code in small verifiable units. The parent iterates with that same worker. Re-architecture is triggered by concrete invalidation evidence, not by ordinary implementation friction or stylistic preference.

## Alternatives considered

- Let the parent write code directly. Rejected to reserve expensive parent reasoning for judgment and verification.
- Let Architect implement its selected design. Rejected because architecture review and mutation need different authority boundaries.
- Spawn a fresh implementer for every unit. Rejected because continuity matters when later units depend on discoveries from earlier ones.
- Re-run architecture after every implementation issue. Rejected as wasteful; only load-bearing invalidation should reopen the design.

## Evidence

- `skills/implement/SKILL.md`
- `skills/implement/references/implementation-worker.md`
- `skills/architect/SKILL.md`
- `skills/architect/references/rationale-template.md`
- `skills/arena/SKILL.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Owned source changes have one entry point and one accountable lead. Architect can be invoked independently to produce diagrams and a proposed design without changing code. Implementation units should be coherent and directly verifiable; roughly 400–500 changed lines is preferred and about 1,000 is a review signal rather than an automatic failure.

## Revisit when

- The host can no longer retain or message a native implementation worker.
- Measurements show persistent-worker context causes more errors than it prevents.
- A class of safe mechanical edits demonstrably does not benefit from parent-worker separation.
