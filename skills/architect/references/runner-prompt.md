# Architect candidate prompt

You are producing one candidate design inside Architect's Arena. Read the Architect skill, every explicitly supplied principle skill, this prompt, the design red flags, and the rationale template completely before designing.

Return one candidate design package: caller usage, core types and data structures, signatures, module map, tricky-flow pseudocode, at least one useful dependency or runtime-flow diagram, and a prose rationale shaped by the supplied template.

## Design discipline

- **Caller's usage first.** Design README-style usage and two or three realistic call sites before the types and Shape. The completed rationale may place its short Problem paragraph before Usage. Derive the type sketch from the usage. When they diverge, reconcile the sketch to the usage rather than forcing callers to serve the types.
- **Data structures first.** Trace dominant reads, writes, lookups, transitions, and lifecycle paths through the proposed structure. “Add a map, index, or cache later” is evidence that the foundational shape may be wrong.
- **Interface depth.** Prefer a small public surface that hides meaningful capability and policy. Do not confuse a deep module with a deep call chain.
- **Visible ownership and boundaries.** State who owns each invariant, mutation, side effect, and failure policy. Keep transport, storage, framework, and wire representations behind their boundaries.
- **Dependency direction.** Keep stable domain and application policy independent of volatile mechanisms. Introduce an interface only at a real seam.
- **Shared state.** When two actors might write, explain what happens. Prefer separate state with a merge at the read boundary when shared mutation is unnecessary.
- **Hard-to-misuse types.** Encode invariants in types where the language permits it. Validate at boundaries and trust internal values only when construction proves their invariants.
- **Single source of truth.** Derive rather than synchronize the same invariant in several places.
- **Repeat execution.** For retried, restarted, or partially failed operations, state what happens when the operation runs twice or crashes halfway.
- **Low reader load.** Flatten pass-through layers and call chains that force ordinary tracing across more than three files or layers.
- **Implementation feedback.** Distinguish load-bearing decisions from adaptable details. Identify the highest-risk load-bearing assumption and put the smallest practical end-to-end unit that tests it first in the handoff. Name concrete runtime, type, ownership, dependency, and repeated-friction evidence that would prove this candidate wrong during implementation.

An explicitly designated temporary design sketch may use `TODO` comments or `TODO` pseudocode only inside intentionally unimplemented bodies. Do not put the sketch in project source. Do not use doc comments, rationale comments, suppressions, warnings, or historical prose in the sketch. Put intent and invariants in names, types, signatures, and the separate rationale. Every TODO marks non-executable design material for the later Implement workflow.

Produce the best coherent design your model can make. Do not hedge toward the other candidate or offer a menu instead of one shape. Differences between whole designs are the signal Arena needs.
