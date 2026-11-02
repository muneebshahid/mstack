# Logbook: Add Philosophy of Software Design guidance

## Context

Simplicity and Ownership said little about module depth, generality, or leaked design decisions, which John Ousterhout's *A Philosophy of Software Design* addresses. The wording draws on reviews and summaries of the book, not the book itself.

## Decision

Owner's call: add deep-module and general-purpose guidance to Simplicity, prefer a simpler interface over a simpler implementation, expect each layer to offer a different abstraction, and treat one design decision spread across modules as leakage. Ownership gains when to combine or separate code. A single use is a signal that a module may be too specialized; it still does not prove a boundary unnecessary. Generalizing is rejected when it adds parameters, modes, or speculative features.

## Rejected

- **Masking exceptions or defining errors away:** conflicts with Ownership's rule against turning failed checks into successful defaults.
- **Writing comments first:** would reintroduce a comment policy just after [Remove Source Style](2026-11-01-remove-source-style.md).
- **Calling event-driven code less obvious:** too narrow for a general principle.
- **Tactical versus strategic programming:** a mindset that gives an agent no specific action.
- **A stronger "design it twice" rule:** Design Decisions and Architect already compare alternatives on consequential choices.

## Verification and gaps

- `scripts/validate.py` passed.
- The guidance has not been tried on a real design.
