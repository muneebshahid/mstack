# Concurrency and Retries

## Separate independent writes

First determine whether concurrent actors publish independent results or must change the same state. Independent agents can write separate result files that the parent collects. Separate their write targets instead of locking an unnecessary shared file.

When state must be shared, enforce coordination through exclusive ownership, a single writer, locks, or atomic updates suited to its invariant. Instructions to take turns do not prevent races. Check what happens when another actor writes at the same time.

## Make retries safe

Choose what should happen when an operation repeats, including after partial failure. Setting a completed status again can be idempotent; incrementing a counter again changes the result. Prefer convergence to the intended state when practical.

A transaction or compensation step alone does not make external effects safe to repeat. Use deduplication supported by the external system, such as idempotency keys, or reconcile against its observed state. Choose repeat and recovery behavior consistent with required semantics, including uncertain outcomes after partial failure or restart. Check repetition at meaningful crash points. Safe concurrent access and safe repetition require separate reasoning when both risks exist.
