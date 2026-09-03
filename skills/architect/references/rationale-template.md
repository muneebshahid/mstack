# Architecture rationale template

Keep the rationale compact—normally about one page. Use sentence-case headings and replace every instruction below with actual content. When persistence is unauthorized, return it in the response rather than creating a file.

## Problem

One paragraph: the requested outcome and the existing constraints that make the shape non-obvious. Name observed integration constraints, callers that cannot break, invariants crossing boundaries, and material evidence gaps.

## Usage (caller's view)

Design this before Shape and before choosing the final types, although the completed document opens with the short Problem section above. Show the README or quickstart the consumer reads plus two or three realistic call sites: imports, calls, results, errors, and relevant side effects. This is the spec. Derive Shape from it; when usage and types diverge, reconcile the sketch to the usage.

## Shape

Present data structures first, then signatures, module map, and data flow. Name load-bearing decisions, invariant owners, validation boundaries, dependency direction, side effects, and failure policy. State what the system deliberately does not do.

Judge interface depth explicitly: what complexity the public surface hides, what remains exposed, and why the interface is no larger than needed. Cite selected principle IDs behind decisions without restating the principles.

## Diagrams

Include the smallest diagrams that make ownership, dependency direction, module boundaries, or a tricky runtime flow materially easier to inspect. Prefer compact Mermaid. Keep the labels consistent with Usage and Shape.

## Synthesis decision

Record which Arena candidate became the base and why, what was grafted from each other candidate, and what was rejected. State whether the parent and configured cross-judge agreed; when the judge was unavailable, record the concrete blocker and that the parent judged the candidates alone.

## Tradeoffs accepted

One bullet per material tradeoff, in the form “we accept X in exchange for Y.” Include choices a future reader might mistake for an oversight.

## Alternatives considered

Required. Name at least one concrete alternative whole shape and why it lost. Compare the complexity each alternative exposes to callers and the complexity it hides. Do not list flavors of the selected shape merely to populate the section.

## Open questions and risks

State unresolved evidence gaps and risks. Phrase questions only when an answer from the caller genuinely changes the architecture; otherwise record the assumption Architect used.

## Implementation handoff

Name the highest-risk load-bearing assumption. Make the first implementation unit the smallest coherent end-to-end slice that can prove or disprove it when practical. If a prerequisite must land first, explain why and place the risk-testing unit at the earliest viable point. Give every unit an outcome, owned surface, dependencies, and direct verification target. Separate load-bearing decisions from details Implement may adapt and name uncertainties implementation must resolve.

Define concrete invalidation signals: observations that contradict caller usage, invariant ownership, boundaries, dependency direction, shared-state assumptions, or failure policy; and repeated friction such as the same workaround, escape hatch, special case, or unplanned coordination appearing in two independent places or units. State the deviation evidence Implement must return. Explain how the sequence keeps the system checkable. If an executable scaffold would materially expose the shape, identify it as an optional first Implement unit rather than creating it in Architect.
