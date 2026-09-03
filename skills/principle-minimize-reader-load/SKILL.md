---
name: principle-minimize-reader-load
description: "Apply when code is hard to trace or a change adds layers, state, abstractions, signal threading, or unnecessary lines. Minimize what readers must traverse and remember, using the Laziness Protocol to prefer the smallest direct solution."
---

# Minimize Reader Load

Maintainability is the work a reader must do to understand code. Track two axes:
1. **Layers to trace.** How many indirections sit between the question and the answer.
2. **State to hold.** How much hidden or mutable context the reader must keep in their head.

**Why:** Code is read far more than it is written. LOC, cyclomatic complexity, and "clean architecture" are proxies. Reader load is the thing that matters. The two axes are independent. A flat file with 50 globals can be as hard to reason about as a six-layer adapter stack. Guard both.

## Laziness Protocol

Writing code is cheap, which makes over-engineering easy. Borrow a human maintainer's fatigue. Aim for the most result with the least code and complexity.

- **Prefer deletion.** Look for removals before additions.
- **Maintain a flat call hierarchy.** A rich interface that hides substantial work is not a deep call chain. If answering an ordinary question requires tracing through more than three files or layers, flatten it.
- **Consolidate decisions.** Put each choice behind one source of truth instead of repeating it in several places.
- **Minimize the diff.** Make the smallest change that solves the problem. When correctness and clarity are at least as strong, fewer lines beat elegant boilerplate.
- **Question signal threading.** Before passing a flag or mode through types, schemas, pipelines, or several call layers, look for a more direct ownership path.
- **Remove small leaks early.** Pass-throughs, representation leaks, and duplicated choices compound into permanent coordination costs.

## Complexity Bears the Burden of Proof

Do not accept machinery merely because it is defensible in the abstract. Every abstraction, layer, guard, validator, fallback, retry path, configuration option, extension point, compatibility path, and additional state transition must serve at least one concrete reason:

- An explicit current requirement.
- A reachable failure mode or observed operational constraint.
- A material risk involving security, data integrity, destructive behavior, concurrency, or an unreliable external boundary.

Name the requirement, execution path, or risk. If no concrete reason survives inspection, challenge the machinery and prefer removing or not adding it. Count the states, branches, tests, failure modes, and maintenance obligations introduced by the proposed protection itself.

Defend real boundaries and reachable failures. Do not revalidate states that constructors or trusted types already make impossible, add fallbacks that conceal contract violations, or introduce recovery, compatibility, configurability, and extensibility for hypothetical futures. Use [Boundary Discipline](../principle-boundary-discipline/SKILL.md) to decide where defensive validation and error handling belong.

**The pattern:**
- **Collapse layers** that do not earn their keep: wrappers with one caller, adapters with no second implementation, indirection introduced for a future that never came. Inline them.
- **Make adjacent layers change the abstraction.** A layer that repeats the same methods and arguments adds reader load without compression. Collapse pass-through layers.
- **Demand interface compression.** A broad interface that hides little complexity makes readers learn both the surface and the implementation. Prefer boundaries that hide meaningful decisions.
- **Shrink state scope:** prefer pure functions (returns over mutations), locals over fields, fields over module state, and module state over globals. Derive instead of sync.
- **Name the invariant at the boundary,** not in every consumer, so the reader learns it once.
- **Read from intent to detail.** Put high-level orchestration before lower-level helpers and keep each function at one conceptual level.
- **Use literal, behavior-revealing names** so readers do not need comments or distant context to decode the flow.
- **Align genuinely equivalent flows** so readers can transfer understanding. Preserve asymmetry when the domain, correctness, or performance requires it.
- **Make abstractions earn their keep.** Keep an abstraction when it expresses domain meaning, isolates real volatility, enforces a boundary, or materially simplifies callers. Reject pass-through wrappers, identity adapters, premature interfaces, and generic mechanisms that obscure a simple shape.
- **DRY structure, not every line.** Types, models, and decisions should converge; three explicit similar statements can still beat a premature abstraction.
- Before adding a layer or a piece of state, ask: does this reduce reader load somewhere else by at least as much?

## Tests

- Can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds?
- Does answering an ordinary question cross more than three files or layers?
- Does an abstraction hide meaningful decisions, or make the reader learn two equivalent surfaces?
- Is hidden or mutable state forcing the reader to simulate distant code?
- Would deletion, inlining, or a smaller diff make the code at least as clear and correct?
- What explicit requirement, reachable execution path, or material risk justifies each added layer, guard, fallback, option, or extension point?
- Does the defensive mechanism prevent more complexity and risk than it creates?

If a human maintainer would find the code exhausting to understand or change, simplify it.
