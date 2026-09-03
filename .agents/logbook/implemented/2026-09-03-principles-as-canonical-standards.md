# Logbook: Principles Are the Canonical Engineering Standards

Status: implemented
Kind: architecture

## Problem

Large code-quality and architecture-review skills repeated overlapping guidance. Their rules could conflict, drift, or be applied wholesale when only a few standards were relevant.

## Decision

Represent engineering standards as small `principle-*` skills. Each leaf owns one rule and states when it applies. `apply-principles` is a router for broad judgment; workflows that already know their required standards load the relevant leaves directly.

Architecture and review workflows may select principles, but they do not restate or weaken them. The current stack keeps twenty leaves covering structure, simplicity, correctness, execution, product design, and source style.

## Alternatives considered

- Keep one code-quality skill and one architecture-review skill. Rejected because both became broad checklists with recurring overlap.
- Put every principle in repository instructions. Rejected because that would load a large standards loop into every task and make contextual selection unreliable.
- Merge related ideas aggressively. Rejected where related principles answer different questions, such as minimizing reader load versus subtracting before adding, or modeling a domain versus reasoning from foundations.

## Evidence

- `skills/apply-principles/SKILL.md`
- `skills/principle-minimize-reader-load/SKILL.md`
- `skills/principle-model-the-domain/SKILL.md`
- `skills/architect/references/principle-routing.md`
- `skills/interrogate/references/principle-routing.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Principles can be reused during planning, implementation, and review without invoking a heavyweight audit. Routing files must identify concrete triggers and avoid selecting leaves merely because they exist. Changes to a standard happen in one canonical leaf.

## Revisit when

- Two leaves repeatedly produce the same decision under the same trigger.
- A workflow must load so many leaves that routing no longer reduces context.
- A recurring engineering rule has no clear canonical owner.
