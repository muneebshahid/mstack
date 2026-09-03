---
name: principle-model-the-domain
description: "Apply before choosing core types and data structures, or when stateful code branches heavily or repeats shape assumptions. Derive a domain structure from invariants and access patterns so downstream logic becomes obvious."
---

# Model the Domain

Encode the real domain in a data structure instead of scattering it across conditionals. Structural decisions protect option value; choosing the right shape early is cheap, while changing it after logic spreads can become a rewrite.

**Why:** Scattered booleans, repeated shape assumptions, and branching spread across files are accidental complexity. A structure that matches the domain makes invalid states unrepresentable and deletes branches. Choosing it at write time is cheap; recovering it later reads as a refactor and gets deferred.

## Foundational pass

Before writing substantial logic:

1. Name the domain concepts, invariants, valid states, and forbidden combinations.
2. Trace dominant reads, writes, lookups, transitions, and lifecycle paths.
3. Identify which actor or component owns each mutation and what concurrent access could occur.
4. Choose the simplest data structure and core types that make those paths direct and invalid states difficult or impossible to create.
5. Test the proposed shape against edge cases before spreading it through callers.

Define core types early. Types and data models should converge around one authoritative shape. Do not close options with speculative abstractions; prefer explicit code until a structure demonstrably removes branches, duplicated rules, invalid states, or lifecycle risk.

**Reach for structures like these:**

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed object/model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command/event model instead of ad hoc state mutations.
- A module organized around one body of domain knowledge instead of a sequence such as load, validate, transform, and save. Execution order is not ownership.
- A small module boundary that gathers repeated behavior, ownership, or invariants.
- A queue, cache, index, graph/tree, or normalized collection where the data access pattern calls for it.
- Any other structure that fits. The list above covers the common cases only. When none fits, work out what the code must never allow and how the data gets read, then find the structure that encodes exactly that.

Do not force an abstraction. Prefer boring code if the current shape is already clear, local, and unlikely to grow. Be skeptical of an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

The tell that you skipped this is a new feature that grows an existing if/else chain by one more branch, or a second boolean that must stay in sync with the first. Temporal decomposition is another tell. Phase-named modules repeat the same domain rules across steps.

Use [Clear Ownership](../principle-clear-ownership/SKILL.md) to decide the canonical owner of the resulting structure. Use [Separate Before Serializing Shared State](../principle-separate-before-serializing-shared-state/SKILL.md) when concurrent actors may mutate it. Sequence shared scaffolding and implementation through [Sequence Verifiable Units](../principle-sequence-verifiable-units/SKILL.md).
