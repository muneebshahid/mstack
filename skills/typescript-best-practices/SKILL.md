---
name: typescript-best-practices
description: TypeScript best practices. Use when reading or editing any .ts or .tsx file.
---

# TypeScript best practices

Apply [Modeling and Types](../apply-principles/references/modeling-and-types.md) first; this skill grounds it in TypeScript syntax.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Encode distinct domain IDs, units, and validated values with `& { readonly __brand: "X" }`. Establish the invariant at creation and propagate the type. |
| Constructive modeling | Represent required structure directly: `[T, ...T[]]` for non-empty input, pairs for even-length data, and a validated nonnegative duration for elapsed time. |
| Simplest total type | Choose types from the intended contract: `T[]` when empty is valid, `NonEmpty<T>` when an item is required. Do not wait for an unsafe use to expose the constraint. |
| `unknown` over `any` | External data is `unknown`. `any` disables type checking everywhere it touches. |
| Checked construction | Narrow and construct values instead of asserting them. A local assertion may introduce an erased brand only after its invariant is established. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Checks static conformance while retaining useful inferred detail; it does not validate runtime input. |
| Boundary validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelled) stops at that parse. Propagate precise types inside and trust their established guarantees. See [Ownership and Contracts](../apply-principles/references/ownership-and-contracts.md). |
| Schema-derived types | Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Don't mock what you can run. Prefer the framework's real test primitives with leak/disposable checks, and verify UI in a running build. Mock only what you can't run locally. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples: [TypeScript patterns](references/patterns.md).
