---
name: implement
description: "Route an authorized code change through Feature, Bug Fix, Refactoring, or Prototype. Use as the single implementation workflow when the task is to add behavior, correct broken behavior, improve structure without changing behavior, or run a disposable experiment."
---

# Implement

Use one entry point for code-changing work. The parent agent remains the lead: it chooses the mode, owns scope and judgment, decomposes the work, inspects the actual diff, verifies each unit, and decides whether the evidence is strong enough to finish. One persistent configured implementation worker writes project code.

## Authority

Inherit authority from the active request. This workflow can edit code only when the user requested a change. It does not by itself authorize commits, branches, pull requests, pushes, deployments, external messages, or expansion into adjacent problems.

Preserve unrelated user changes. Treat repository instructions as binding unless they conflict with a higher-level instruction or the user's explicit request.

## Choose one mode

| Mode | Use when | Read |
|---|---|---|
| **Feature** | Intended behavior is being added or deliberately changed. | [Feature](references/feature.md) |
| **Bug Fix** | Existing intended behavior is broken, regressed, intermittent, or contradicted by observed runtime behavior. | [Bug Fix](references/bug-fix.md) |
| **Refactoring** | Structure changes while externally observable behavior stays fixed. | [Refactoring](references/refactoring.md) |
| **Prototype** | A disposable experiment can cheaply settle a design, interaction, behavior, or performance uncertainty. | [Prototype](references/prototype.md) |

Read only the selected mode. If the work contains multiple modes, split it into ordered units with separate outcomes and verification. Do not hide a feature inside a refactor, turn a speculative change into a bug fix, or promote prototype code into production.

## Shared operating rules

1. Establish the requested outcome, scope, non-goals, and matching verification surface.
2. Ground non-trivial work in the current system. Read [How](../how/SKILL.md) for runtime structure and current mechanics. Read [Why](../why/SKILL.md) only when history, prior decisions, regressions, or external rationale could constrain the change.
3. Read [Architect](../architect/SKILL.md) when a consequential decision changes ownership, boundaries, dependency direction, core state or data shape, public contracts, or cross-system behavior and has more than one viable design. Architect is always read-only: it returns a synthesized design and implementation contract, then stops. The selected Implement mode owns all source changes and verification. Architect already owns competing designs through Arena; do not duplicate that orchestration here.
4. When the work appears decision-bearing, read [Logbook](../logbook/SKILL.md) completely and search `.agents/logbook/` before implementation. Capture only a durable choice maintainers may reasonably revisit: a load-bearing architecture or ownership decision, public or persistent contract, credible tradeoff, recurring non-obvious bug mechanism, meaningful removal, or constraining process or testing strategy. Skip mechanical edits and ordinary local choices. Use Architect's note-ready material when available, but record only what the parent accepts and implementation proves. The parent exclusively creates, updates, moves, and validates Logbook records; the implementation worker supplies factual evidence and clarification but never edits them. Logbook-only parent edits are not project source writing.
5. Read [Apply Principles](../apply-principles/SKILL.md) for its selection and **Resolve tension** rules, but do not invoke it as a second orchestration workflow or request its receipt. Load every principle linked by the selected mode whose stated trigger is actually present. Prefer the smallest triggered set, prefer a specific rule over a broad heuristic, and state a real remaining tradeoff instead of silently averaging principles. Read each selected principle in full. The links route to canonical instructions; the workflow does not restate or weaken them.
6. Before editing owned source, always read and apply [No Comments](../principle-no-comments/SKILL.md). Temporary architecture-sketch or scaffold TODOs do not survive completed implementation.
7. Before code writing, read [references/implementation-worker.md](references/implementation-worker.md) completely, resolve `implement_worker` through MStack configuration, and confirm its configured runner is callable. Its absence is a launch failure. Invoke it to launch the required worker; narration or an intended call is not a launch. A valid spawn response returns a non-empty worker identifier. Surface that exact identifier in the next progress update and retain it before saying the worker is running, writing source, or waiting. If the call is absent, fails, or returns no identifier, stop before editing, preserve the capability failure, and report the blocker. Do not wait on an empty identifier set, infer an orphaned worker, continue from off-trace mutations, or silently replace the worker with the parent.
8. Sequence the work into small coherent units that are easy for the parent to inspect and verify. Each unit must be independently understandable, have bounded authority and explicit exclusions, name its owned or expected files and relevant interfaces, and define observable acceptance and verification evidence. It should be large enough to justify the worker's context load without swallowing a broad plan. Prefer roughly 400–500 changed lines per unit when practical; treat roughly 1,000 changed lines as a decomposition signal, not a hard cap. When an accepted architecture benefits from an executable scaffold, the first Implement unit may establish its types, signatures, and module seams with temporary TODO bodies. Mark it explicitly incomplete, keep the repository's required checks green, verify the structural claim it is meant to expose, and remove every TODO as implementation fills the bodies. If no coherent green scaffold is possible, combine it with the smallest end-to-end implementation slice. Do not treat the scaffold as completed production code. For a decision spanning several authorized commits, the parent creates or updates one `proposed` Logbook record after inspecting the first decision-bearing unit and its evidence, then keeps it current as later evidence arrives; move it to `implemented` only when the decision is realized and freshly verified. A verified single-unit decision may be recorded directly as `implemented` after parent verification.
9. After every unit, inspect the actual diff and run or independently assess the focused verification. Require the worker to report `No deviation`, an `Adaptation` within declared latitude, or a concrete `Deviation` from the accepted architecture, plus factual consequences, constraints, and evidence relevant to any pending Logbook decision. Send concrete implementation feedback to the same worker until the unit passes, architecture-invalidating evidence emerges, or a precise blocker remains. When Logbook capture is active, the parent decides what the result warrants, asks the worker for missing factual clarification when useful, and writes or updates the record itself against the same diff, evidence, accepted rationale, and genuine alternatives. Do not accept the worker's summary as proof.
10. After all units, inspect the final diff, run repository-required checks plus focused checks for the changed behavior, and exercise the matching surface. An inconclusive or wrong-surface result is not a pass. Validate an active Logbook tree with its bundled validator and do not label a record `implemented` while relevant evidence remains inconclusive.
11. Report blockers and evidence gaps precisely. Do not fill them with assumptions or broaden authority to make them disappear.

## Architecture feedback loop

When Architect supplied the accepted shape, its handoff is the implementation contract:

1. Pass the load-bearing decisions, adaptable details, unresolved uncertainties, and invalidation signals to the implementation worker.
2. After each unit, compare the diff and verification evidence with that contract. A difference within declared adaptation latitude is ordinary implementation judgment. A mismatch with a load-bearing decision or an explicit invalidation signal is not.
3. Treat one direct contradiction of caller usage, invariant ownership, boundaries, dependency direction, shared-state assumptions, or failure policy as sufficient to pause. Also pause when the same workaround, type escape hatch, special case, or unplanned coordination appears in two independent places or units.
4. If the implementation worker already exists, keep it idle and retain its identifier. Preserve the partial diff and deviation evidence, then re-invoke read-only Architect with the original design plus the observed evidence. No project writes occur during this architecture pass. If the contradiction appears before worker launch, run Architect before spawning a worker and do not claim that a worker was resumed.
5. The parent judges the returned design. If a worker already exists, send the revised contract to that same worker and have it remove or reshape superseded partial code before continuing. Otherwise launch the required worker only after the revised contract is accepted. When Logbook capture is active, the parent revises the proposed record to match the replacement decision and preserves only genuine superseded alternatives. Do not layer compatibility patches over a rejected architecture.
6. Reverify the affected unit against the revised contract before advancing.

Do not invoke Architect for an ordinary local coding correction, a detail it explicitly left adaptable, or a single implementation inconvenience that does not contradict the design. Conversely, do not let sunk implementation effort turn an invalid architecture into an immutable plan.

## Completion report

Return:

- begin with the selected mode and requested outcome;
- the implementation worker identifier and any model, effort, or Fast-mode capability gap;
- any Architect design checkpoint and the point where implementation returned to this workflow;
- architecture deviations observed, their classification, and any Architect rerun and resulting replacement contract;
- the important design or diagnostic decisions;
- the implemented change or prototype result;
- the Logbook record created, updated, moved, or deliberately skipped, with the decision-bearing trigger or skip reason;
- the principles loaded and the concrete trigger for each;
- direct verification evidence and any remaining gap;
- any action intentionally not taken because it lacked authority.
