---
name: architect
description: "Design a consequential change without coding: ground the existing system, use Arena for competing usage/type/module sketches, select a coherent proposed architecture, and return a design package and diagrams for later implementation. Use only when explicitly invoked."
---

# Architect

Design without implementing. Ground the systems the change touches, sketch caller usage, types, signatures, data flow, and module boundaries, then use Arena to synthesize across independent model perspectives. Return a coherent proposed architecture, an implementation contract, and concrete evidence that should invalidate the design during implementation.

## Authority

Architect is explicit-only and always read-only, even when the outer request also authorizes implementation. It must not edit project files, create a worktree, implement a prototype, commit, push, deploy, or mutate external systems.

- Temporary prompts and candidate artifacts stay outside the repository.
- Diagrams, usage sketches, type signatures, module maps, and TODO pseudocode are design artifacts, not source changes.
- Persist a rationale or diagram only when the user separately asks for a file; persistence does not authorize source implementation.
- If executable evidence is needed to choose an architecture, recommend a bounded [Implement Prototype](../implement/references/prototype.md) task and stop. A later Architect run may consume that prototype evidence.

Create a visible working plan for Ground, Sketch, Decide, and Handoff.

## Phase A: Ground the problem

Build a real mental model of every system the new code touches. Naming files is not grounding.

1. Read the [How skill](../how/SKILL.md) completely and run its Explain mode over the relevant subsystems. Use How Critique only when the caller asks for critique or the current structure itself is a contested constraint.
2. Produce the traced model How prescribes: current purpose, runtime flow, ownership, data and invariants, boundaries, side effects, failure behavior, and relevant files.
3. When `.agents/logbook/` exists, search its implemented records for decisions governing the affected subsystem and read relevant proposed or rejected records only when they illuminate active alternatives. Treat current code and tests as authority for mechanics; records preserve stated rationale and tradeoffs. Architect never writes or moves a record.
4. Read and run [Why](../why/SKILL.md) when the design would redefine established ownership, layering, contracts, or a non-obvious constraint whose historical rationale may still matter. Do not run Why merely because old code exists.
5. Skip grounding only for genuinely greenfield work with no surrounding system, contract, or repository convention to integrate.

Turn the grounding into explicit design constraints. Separate observed constraints from assumptions and unresolved questions.

## Select design principles

Read [references/principle-routing.md](references/principle-routing.md). Resolve every selected principle to its absolute `SKILL.md` path and read it completely. Select the core leaves plus only conditionals concretely triggered by the task. Pass the exact same ordered path list to every Arena candidate.

Architect selects leaves directly; do not ask candidates to invoke `apply-principles` or other orchestration skills.

## Phase B: Sketch through Arena

Read the [Arena skill](../arena/SKILL.md) completely and invoke it with the design-sketch task and Phase A grounding.

Architect's explicit invocation makes Arena mandatory even when Arena's generic routing would skip a tightly constrained artifact. If grounding proves that constraints leave only one viable whole shape, the candidates should independently demonstrate that conclusion and the synthesis record should explain why the apparent alternatives fail.

Before launching Arena, read in full:

- [references/runner-prompt.md](references/runner-prompt.md)
- [references/rationale-template.md](references/rationale-template.md)
- [references/design-red-flags.md](references/design-red-flags.md)

Build Arena's common candidate prompt from its own candidate template plus the Architect runner prompt. Every candidate receives:

- The exact requested outcome and read-only design authority.
- The grounding model and unresolved evidence gaps.
- Relevant project paths and repository instructions.
- The ordered selected principle paths.
- The design red flags and rationale template.

Each candidate produces one design package. “Caller usage first” means usage is designed before core data structures, types, and Shape; the final rationale may still open with its short Problem paragraph for readability. Follow usage with function or method signatures, module map, tricky-flow pseudocode, at least one useful dependency or runtime-flow diagram, and rationale.

Use this Arena rubric:

1. The caller experience is small, realistic, and agrees with the proposed types.
2. The domain model and access patterns make invariants and dominant operations direct.
3. Ownership, boundaries, dependency direction, side effects, and failure policy are explicit.
4. The design is proportionate: its public surface hides meaningful complexity without deep call chains or pass-through layers, and every abstraction, guard, fallback, option, compatibility path, or extension point is justified by a current requirement, reachable failure mode, or material risk. Unjustified machinery is grounds to revise or reject a candidate, not merely a tie-breaker.
5. The shape admits a clear implementation, migration, and verification sequence whose earliest practical end-to-end unit tests the highest-risk load-bearing assumption.

Design it independently. Arena's two default candidates satisfy the exploration requirement only when they represent materially independent attempts. If they converge because the constraints force one viable shape, record the consensus. If they converge on an unexamined safe middle or flavors of one shape, reframe and rerun one fresh candidate for a structurally different alternative before synthesis.

Architect requires at least two usable candidate designs before claiming synthesis. If fewer than two candidates succeed, return the surviving design plus the blockers as an incomplete, degraded Architect result. Do not silently substitute a model. A failed configured cross-judge does not block synthesis when at least two candidate designs are usable: the parent performs the criterion-level judgment, records the missing cross-judge, and labels the result degraded.

Screen every candidate against the design red flags before selecting a base. Reject or revise shallow modules, information leakage, temporal decomposition, pass-through methods, and designs that need callers to understand internal rules.

Arena returns one synthesized design package and synthesis record. Populate the rationale's Synthesis decision from Arena's base, graft, and rejection record.

## Phase C: Decide

The parent retains final architectural judgment after Arena.

- Return the synthesized design and stop. Architect never proceeds into source implementation.
- If the caller rejects or materially changes the shape, treat that response as new grounding evidence and return to Phase A.
- If Implement returns evidence that a load-bearing decision is wrong, treat the observed code friction, failed verification, and deviation record as new grounding evidence. Run How over the affected built shape, revise the constraints, and return to Phase B. Do not defend the old sketch or patch it incrementally merely because implementation has started.
- Run [Interrogate](../interrogate/SKILL.md) on the synthesized sketch only when the caller explicitly asks for adversarial pressure. Arena's cross-judge already supplies ordinary independent comparison.

## Phase D: Hand off

Shape the design so [Implement](../implement/SKILL.md) can execute it without silently redesigning it:

1. Identify the highest-risk load-bearing assumption and make the first implementation unit the smallest coherent end-to-end slice that can prove or disprove it when practical. If a prerequisite must land first, explain why and place the risk-testing unit at the earliest viable point. Do not choose an arbitrary small unit that leaves the consequential assumption untested.
2. Give each unit an observable outcome, owned surface, dependencies, and direct verification target.
3. State which decisions are load-bearing, which details the implementer may adapt, and which uncertainties implementation must resolve.
4. Define specific invalidation signals. Include any single observation that contradicts caller usage, an invariant owner, a boundary, dependency direction, shared-state assumptions, or failure policy. Also include repeated friction such as the same workaround, escape hatch, special case, or unplanned coordination appearing in two independent places or units.
5. State the evidence Implement must return when a deviation occurs: affected unit and symbols, expected versus required shape, failed check or runtime observation, and whether the worker believes the issue is local or architectural.
6. Keep the sequence roughly 400–500 changed lines per unit when practical; treat roughly 1,000 changed lines as a decomposition signal, not a hard cap.
7. Return note-ready Logbook material when the selected architecture is decision-bearing: the problem, accepted decision, genuine alternatives considered and why they lost, expected evidence, consequences, and revisit or invalidation signals. This is input to Implement, not a repository write or an instruction to record every design.

The handoff is a decision boundary, not an immutable plan. Implement may adapt explicitly flexible details. It must pause and return to Architect when observed evidence contradicts a load-bearing decision or matches an invalidation signal. A fresh Architect run consumes that evidence and may retain, amend, or replace the design.

Do not invoke Implement automatically. The active parent workflow or user decides whether to proceed from the read-only design into code changes.

## Final verification and output

Before finishing, verify that the usage, types, ownership, boundaries, dependency direction, failure policy, module map, diagrams, implementation sequence, adaptation latitude, and invalidation signals agree with one another. Prefer compact Mermaid diagrams in the response when they make component, dependency, or flow relationships easier to inspect. Report remaining open questions, failed capabilities, and unverified assumptions.

Return:

- The synthesized design package shaped by [references/rationale-template.md](references/rationale-template.md).
- Arena's synthesis record.
- A read-only implementation contract: ordered verifiable units, adaptable details, load-bearing decisions, invalidation signals, deviation-evidence requirements, and remaining risks.
- Note-ready Logbook material when the selected architecture meets the decision-bearing threshold, or a brief statement that no durable record is warranted.
