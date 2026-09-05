# Modeling and Types

## Model the domain

Name the concepts, invariants, valid states, transitions, and mutation owners before substantial logic. Choose a structure that makes common reads and writes direct, including lifecycle and concurrent access. Scattered branches or synchronized booleans can reveal a missing state model; local, clear logic needs no framework.

Keep one authoritative shape. Derive types from schemas where those schemas own the contract, rather than maintaining parallel definitions.

## Encode constraints in types

Use the language's useful type support proactively to prevent invalid states, semantic mixups, and partial operations. Give distinct domain IDs, units, and validated values branded or opaque types. Represent mutually exclusive states as variants and keep matches exhaustive so adding a variant exposes each missing case.

Construct valid values rather than repeatedly checking loose shapes. A function requiring an item can accept a head and rest instead of a possibly empty list. Make constructors establish invariants and propagate precise types through callers instead of widening them back to primitives or optional fields.

At runtime boundaries, narrow unknown input through validation before constructing trusted values. Trust internal values only as far as their construction and provenance justify. Unsafe casts and assertions do not validate data or establish a domain guarantee.
