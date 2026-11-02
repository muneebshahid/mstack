# Logbook: Replace Explain with Show Me

## Context

Explain combined source selection, optional delegated exploration through `explain_explorer`, a four-section response template, and visual guidance adapted from HumanLayer's Show Me.

## Decision

Owner's call: keep only the visual guidance, as a user-invoked `show-me` skill, and remove the rest, including `references/evidence.md` and the `explain_explorer` role. Architect now investigates directly, Implement no longer routes to Explain, and Grill Me uses Show Me for diagrams.

Show Me keeps the Mermaid fallback from [Explain draws diagrams where Mermaid does not render](../incidents/2026-10-07-explain-mermaid-fallback.md), because upstream assumes Mermaid renders. It leaves out upstream's closing "don't overwhelm the user" line, because that incident removed visual rationing at the owner's request.

## Rejected

None considered beyond the upstream wording above.

## Verification and gaps

- `scripts/validate.py` passed, including links and resolver tests.
- Saved profiles with a partial `[roles.explain_explorer]` override now fail resolution until that table is removed.
- Show Me has not been run in a fresh session.
