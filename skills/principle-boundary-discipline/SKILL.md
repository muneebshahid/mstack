---
name: principle-boundary-discipline
description: "Apply when designing public contracts or wiring validation, error handling, persistence, transport, or framework adapters. Keep boundary representations private, contracts explicit, and internal values trustworthy by construction."
---

# Boundary Discipline

Place validation, type narrowing, and error handling at system boundaries. Trust internal values only when their construction enforces the claimed invariants. Keep business logic independent of framework wiring; prefer pure functions where the domain permits them.

**Why:** Scattered validation is noisy, redundant, and gives a false sense of safety. Validate data once at the boundary. Keep logic out of framework wiring so it can be tested without the framework.

**The pattern:**
- **At boundaries** (CLI args, config files, external APIs, network protocols): validate, return errors, handle defensively.
- **Inside the system:** typed data, error propagation, and no redundant re-validation when construction already proved the invariant. Trust the types only as far as their constructors and provenance justify.
- **Across the boundary.** Expose domain concepts, not the boundary's private representation. Keep general-purpose mechanism inside and special-purpose policy at the edge.

## Contract discipline

- Expose the smallest public surface that serves actual callers.
- Make inputs, outputs, side effects, failure behavior, and compatibility explicit wherever ambiguity creates risk.
- Keep transport, storage, framework, vendor, and wire representations private to their adapters.
- Translate external failures into the contract owned by the application or domain instead of leaking mechanism-specific errors inward.
- Treat compatibility as a deliberate contract decision, not an accidental consequence of leaving old paths alive.
- Keep implementation details private so callers depend on behavior rather than representation.

**Applications:**

Validation and error handling:
- Validate config at parse time (the boundary), not inside business logic
- Parse raw data into domain types at the boundary
- Do not re-export transport, storage, framework, or wire types through the public surface
- No redundant nil checks deep in call chains if the boundary already validated
- Treat persistence reads, queues, plugins, caches, legacy data, and deserialization as boundaries when they can supply stale, malformed, or externally produced values

Code organization:
- Business logic without framework dependencies; use pure functions where state and effects do not belong to the domain operation
- Parse functions: pure transforms from raw bytes to typed state
- Prompt construction: structured state in, string out
- Scoring and assessment: pure transforms from state to results

**The tests:**
- "Is this data crossing a boundary, or entering from a source whose invariants are not mechanically guaranteed?" If not, validation is probably redundant.
- "Can this be a pure function that the shell just calls?" If yes, extract it.
- "Can a caller tell what this operation returns, changes, emits, and how it fails?"
- "Does the public surface expose a boundary mechanism that should remain private?"

Use [Dependency Direction](../principle-dependency-direction/SKILL.md) when the contract is sound but source dependencies point from stable policy toward a volatile mechanism.
