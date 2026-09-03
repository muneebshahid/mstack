---
name: principle-dependency-direction
description: "Apply when core policy imports infrastructure or framework details, dependency cycles appear, orchestration crosses layers, or an interface may be needed at a genuine architectural seam."
---

# Dependency Direction

Point dependencies toward stable domain and application policy. Frameworks, transport, persistence, and external services implement or invoke core contracts; the core does not depend on their concrete mechanisms.

## Apply when

- Domain or application logic imports framework, transport, persistence, or vendor types.
- A dependency cycle appears between modules or packages.
- High-level policy calls concrete low-level mechanisms directly.
- Orchestration, business rules, and infrastructure details are mixed.
- A proposed interface, port, or adapter needs to justify its seam.

## Determine direction

1. Identify the policy that should remain stable when mechanisms change.
2. Identify volatile mechanisms such as databases, networks, frameworks, clocks, filesystems, queues, and vendors.
3. Define a narrow core-facing contract only when the mechanism crosses a real seam or has a real variant.
4. Make the mechanism depend on that contract through an adapter, composition root, or injected implementation.
5. Keep wiring at the edge and dependency cycles out of the graph.

Dependencies may flow outward at runtime while source dependencies point inward. A domain operation can call a repository contract without importing the concrete database repository.

## Guardrails

- Do not create an interface for every class or function.
- Do not add ports, adapters, factories, or layers merely to satisfy a pattern.
- Keep direct inline calls when both sides belong to one cohesive owner and no architectural seam exists.
- Do not hide a cycle behind service lookup, global registries, callbacks, or dynamic imports.
- Prefer the smallest structural move that restores the intended direction.

Use [Boundary Discipline](../principle-boundary-discipline/SKILL.md) for parsing, validation, public representations, and error translation at a boundary. Use [Clear Ownership](../principle-clear-ownership/SKILL.md) when the problem is who owns the behavior rather than which way dependencies point.

## Tests

- "Could the core policy be tested without loading the framework or infrastructure mechanism?"
- "If the database, transport, or vendor changed, would domain policy remain untouched?"
- "Does this interface protect stable policy or a real variant, or merely mirror one implementation?"
- "Can the dependency graph be explained without a cycle or cross-layer shortcut?"
