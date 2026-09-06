# Design template

Use these headings for both direct designs and candidate proposals. Keep sections proportional to the task; omit unnecessary sketches and empty subsections.

## Problem and constraints

State the requested outcome, relevant current behavior, and constraints. Separate verified facts, assumptions, and unresolved questions.

## Proposed design

Show realistic caller usage, including relevant results and failures. Derive the types and operations from it. Show who owns state, invariants, and side effects; identify boundaries and dependency direction.

Use signatures, a module map, pseudocode, or diagrams where they clarify the proposal. Keep names and contracts consistent. Label sketches as proposed; describe unfinished behavior in prose rather than source comments.

## Decisions and alternatives

Explain consequential choices and tradeoffs. Record alternatives actually considered and why they lost. If constraints settle the choice, say why without inventing another design.

For a comparison, name the selected proposal, compatible ideas adopted from others, rejected ideas, and the reasons. Report candidate failures, disagreements, and any consultant's contribution. Include captured model provenance in the Logbook material for the parent.

## Implementation handoff

Give each implementation unit an observable outcome, owned surface, dependencies, and verification target. Identify the riskiest assumption and the earliest practical unit that tests it.

Separate decisions that must hold from adaptable details. Name concrete observations that would invalidate the design, including contradictory runtime or type evidence and repeated workarounds that expose a structural problem. State what implementation should return: affected unit and symbols, expected versus required behavior or shape, and the failed check or observation.

Report open questions, unverified assumptions, and access gaps. For an unresolved empirical choice, specify the bounded experiment and evidence needed before choosing.
