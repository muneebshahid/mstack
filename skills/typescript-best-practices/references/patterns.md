# TypeScript patterns

Code examples for each rule in `SKILL.md`. The underlying principles are language-agnostic; see [Modeling and Types](../../apply-principles/references/modeling-and-types.md) and [Ownership and Contracts](../../apply-principles/references/ownership-and-contracts.md).

## Branded types

Give distinct domain IDs, units, and validated values their own types before mixing them becomes a bug. Validate at construction and preserve the precise type through callers.

```ts
type UserId = string & { readonly __brand: "UserId" };

function parseUserId(input: unknown): UserId {
  if (
    typeof input !== "string" ||
    !/^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/i.test(input)
  ) {
    throw new Error("expected UUID-formatted user id");
  }
  return input as UserId;
}

function userHref(id: UserId): string {
  return `/users/${id}`;
}
```

The parser establishes UUID format, not the existence of a user. Its local assertion introduces an erased brand after validation; the assertion itself checks nothing. Follow the `readonly __brand: "X"` convention.

## Discriminated unions

Model valid combinations proactively. A literal discriminant lets the compiler distinguish states; a boolean with unrelated optional fields cannot enforce their relationship.

```ts
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

Pick one discriminant name (`kind`, `type`, `tag`) and stick to it.

## Constructive modeling

Build required structure into the type. Runtime validation establishes facts that TypeScript cannot infer from raw input.

A non-empty tuple guarantees its head, even with `noUncheckedIndexedAccess`:

```ts
type NonEmpty<T> = readonly [T, ...T[]];

function firstEntry(entries: NonEmpty<string>): string {
  return entries[0];
}
```

Narrow a plain array once at the boundary; callers then receive the stronger type:

```ts
const isNonEmpty = <T>(arr: readonly T[]): arr is NonEmpty<T> => arr.length > 0;
```

Pairs encode an even number of elements when flattened:

```ts
type Pairs<T> = [T, T][];
```

A plain number allows negative durations. Validate before introducing the duration type:

```ts
type NonNegativeDurationMs = number & {
  readonly __brand: "NonNegativeDurationMs";
};

function parseDurationMs(input: unknown): NonNegativeDurationMs {
  if (typeof input !== "number" || !Number.isFinite(input) || input < 0) {
    throw new Error("expected finite nonnegative duration");
  }
  return input as NonNegativeDurationMs;
}

type TimeRange = { start: Date; durationMs: NonNegativeDurationMs };
```

This establishes a finite, nonnegative duration. Date validity and arithmetic bounds need their own validation when the contract requires them.

## Simplest total type

Choose the type from the contract. An empty array is valid for a sum:

```ts
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);
```

When the operation requires a session, express that requirement before writing the body:

```ts
function newestSession(sessions: NonEmpty<Session>): Session {
  return sessions[0];
}
```

If absence is a valid result, `Session | undefined` is another total signature. The caller decides what an empty collection means. Do not wait for `!`, an unsafe cast, or a "should never happen" throw to reveal the missing contract.

## `unknown` over `any`

`any` disables type checking wherever it spreads. Treat external data as `unknown` and narrow it before use:

```ts
function parseLabel(input: unknown): string {
  if (typeof input === "object" && input !== null && "label" in input) {
    const label = input.label;
    if (typeof label === "string") return label;
  }
  throw new Error("expected label");
}
```

External sources include RPC payloads, `JSON.parse`, `postMessage`, IPC, file contents, environment variables, database results.

## Checked construction

Construct a domain value after checking its fields instead of asserting that raw data has the desired shape:

```ts
type User = { id: UserId; name: string };

function parseUser(data: unknown): User {
  if (typeof data !== "object" || data === null || !("id" in data) || !("name" in data)) {
    throw new Error("expected user fields");
  }
  const { id, name } = data;
  if (typeof name !== "string" || name.trim().length === 0) {
    throw new Error("expected nonempty name");
  }
  return { id: parseUserId(id), name };
}
```

The parser constructs every field without asserting `data as User`. An erased brand may need a local assertion after validation, as above; this does not justify asserting an unchecked object.

When removing an assertion, check whether the missing piece is a discriminant, a narrower source type, or a boundary parser. `satisfies` can check static conformance but cannot validate unknown runtime input.

## Narrowing hierarchy

From best to last-resort:

1. **Discriminated union switch / if.** Compiler narrows automatically.
2. **`in` operator.** `"key" in obj` narrows to variants containing that key.
3. **`typeof` / `instanceof`.** For primitives and class instances.
4. **User-defined type guard.** When the above aren't enough.
5. **`as` cast.** Only to express an already established guarantee the compiler cannot represent.

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rect"; width: number; height: number };

function areaByFields(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2;
  return s.width * s.height;
}
```

## Type guards

A guard must actually verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe.

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

Prefer discriminant narrowing when possible. The guard adds a layer the reader has to follow.

## Exhaustiveness

In default arms, assign the remaining variant to a `never`-typed local. The compiler errors if a new variant is added without handling.

Return the local in a value-returning switch:

```ts
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}
```

Use a void expression in a statement switch:

```ts
function recordArea(s: Shape, write: (area: number) => void): void {
  switch (s.kind) {
    case "circle":
      write(Math.PI * s.radius ** 2);
      break;
    case "rect":
      write(s.width * s.height);
      break;
    default: {
      const _exhaustive: never = s;
      void _exhaustive;
    }
  }
}
```

## `satisfies` over `as`

`satisfies` checks static conformance while retaining useful inferred detail. It performs no runtime validation. Here the literal union in `Config` lets `config.theme` remain `"dark"`:

```ts
type Config = { theme: "dark" | "light"; cols: number };
const config = { theme: "dark", cols: 3 } satisfies Config;
const theme: "dark" = config.theme;
```

## Boundary validation

Validate once where data crosses in and propagate the resulting domain types. Trust only guarantees established by construction and provenance. See [Ownership and Contracts](../../apply-principles/references/ownership-and-contracts.md).

- **Wire formats** (proto, JSON-RPC): ignore unknown fields only when the compatibility contract permits it; still validate required fields.
- **Persisted JSON:** use a versioned shape and handle parse failures explicitly rather than substituting a successful default.
- **Don't re-validate** established invariants deep in call chains.

## Schema-derived types

When a `.proto`, OpenAPI spec, GraphQL schema, or database migration already defines a shape, derive from the generated types instead of duplicating them.

Substitute the repository's generated module path:

```ts
import type { ChecksMessage } from "<generated module>";
type CheckSummary = Pick<ChecksMessage, "totalCount" | "checks">;
```

Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof` before writing a new interface.

## Object args

Avoid relying on positional argument order:

```ts
openFile(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});
```

An object names each argument:

```ts
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

Skip on hot paths: per-frame render, tokenizers, parsers, anything in a tight loop where the allocation cost matters.
