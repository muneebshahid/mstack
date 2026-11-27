# Concurrency and Retries

## Separate independent writes

First determine whether concurrent actors publish independent results or must change the same state. Independent agents can write separate result files that the parent collects. Separate their write targets instead of locking an unnecessary shared file.

When state must be shared, enforce coordination through exclusive ownership, a single writer, locks, or atomic updates suited to its invariant. Instructions to take turns do not prevent races. Check what happens when another actor writes at the same time.

## Don't act on an unguarded read

A value read in one statement must not decide a later write unless something stops it changing in between. Assume a second actor every time: a retried job next to the attempt it replaced, a second process, or a command started twice. Use, in this order:
1. One statement that carries its own condition, such as an update whose `where` names the state you expect, an insert with `on conflict`, or a compare-and-set on a version. Read what it returned to learn whether it applied.
2. A constraint that makes the bad state impossible. Every "insert if it isn't there" has a unique key behind it.
3. A lock taken in the same transaction and held until the write commits. A plain read or `exists` is not a lock.

Compute counters and sequence numbers in the write itself, with a unique key behind them. Keep a transaction that holds a lock short and never wait on the network inside it. Say in a comment which of the three makes the code safe.

## Make retries safe

Choose what should happen when an operation repeats, including after partial failure. Setting a completed status again can be idempotent; incrementing a counter again changes the result. Prefer convergence to the intended state when practical.

A transaction or compensation step alone does not make external effects safe to repeat. Use deduplication supported by the external system, such as idempotency keys, or reconcile against its observed state. Choose repeat and recovery behavior consistent with required semantics, including uncertain outcomes after partial failure or restart. Check repetition at meaningful crash points. Safe concurrent access and safe repetition require separate reasoning when both risks exist.
