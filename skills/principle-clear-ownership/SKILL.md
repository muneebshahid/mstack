---
name: principle-clear-ownership
description: "Apply when invariants, mutations, side effects, failure policy, or implementation placement lack one obvious owner. Group responsibilities that change together and put behavior in its canonical home."
---

# Clear Ownership

Give every invariant, mutation, side effect, lifecycle transition, and failure policy one obvious owner. Code that serves the same responsibility should live together; code with different owners should not be fused merely because it runs in sequence.

## Apply when

- The same decision or invariant appears in several modules.
- It is unclear which component may mutate state or perform a side effect.
- A component mixes responsibilities that change for different reasons.
- Callers coordinate special cases that belong behind one owner.
- Similar behavior has several helpers or no canonical location.
- A source file crosses 1,000 lines or becomes a god module and needs an ownership-based decomposition check.

## Map ownership

For each relevant responsibility, identify:

- The state and invariants it protects.
- The operations allowed to mutate that state.
- The side effects it initiates or coordinates.
- Its lifecycle and failure contract.
- Its public contract and dependent callers.

If two components can independently decide the same policy, ownership is split. Choose one owner and make the others request or consume its decision.

## Cohesion and canonical placement

- Keep responsibilities together when they change for the same reason and share the same invariants.
- Separate responsibilities when they have different policies, lifecycles, dependencies, or failure modes.
- Put implementation beside the concept that owns it. Reuse the canonical helper rather than creating a second local version.
- Gather scattered feature checks and duplicated policy behind the owner that can enforce them consistently.
- Organize modules around bodies of knowledge and authority, not chronological execution phases.

## Size is evidence, not ownership

Do not split a component solely because it is large. Crossing 1,000 lines in a non-generated source file is a serious signal to inspect responsibilities, not an automatic demand to create another file. Extract only a cohesive responsibility with a clearer owner. Generated files and mechanical data are excluded.

## Guardrails

- Do not create a god object in the name of centralizing ownership.
- Do not introduce managers, coordinators, or services whose only role is forwarding calls.
- Do not move behavior to a shared utility when a domain or application owner exists.
- Do not confuse execution order with ownership.

Use [Model the Domain](../principle-model-the-domain/SKILL.md) when the missing owner is really a missing domain structure. Use [Dependency Direction](../principle-dependency-direction/SKILL.md) when ownership is clear but dependencies point the wrong way.

## Tests

- "Who is allowed to make this decision or mutation?" There should be one clear answer.
- "Where would a maintainer change this policy?" There should be one canonical location.
- "Do these responsibilities change for the same reason?" If not, separate them.
- "Would this extraction reduce mixed ownership, or only move lines?" Extract only for the former.
