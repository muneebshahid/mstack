---
name: principle-make-operations-idempotent
description: "Apply when commands, lifecycle steps, or processing loops can be retried, restarted, or partially fail. Choose explicit convergence, deduplication, transactions, compensation, or at-most-once semantics."
---

# Make Operations Idempotent

For operations exposed to retries, restarts, or partial failure, choose and enforce a repeat-execution policy. Prefer convergence to the correct state when practical. Transactions, deduplication, compensation, or explicit at-most-once semantics are valid when unconditional idempotency is not.

**Why:** Commands, lifecycle operations, and processing loops run where crashes, restarts, and retries are normal. If partial state changes the next run's outcome, every restart becomes a debugging session.

**The pattern:**
- Convergent startup: scan for existing state, clean stale artifacts, adopt live sessions
- Content-based cleanup: compare by content equivalence, not creation order
- Self-healing locks: use PID-based stale lock detection
- Idempotent scheduling: failed work respawns cleanly, fresh input regenerated after each cycle

**The test:**
1. What happens if this runs twice in a row?
2. What happens if the previous run crashed at every possible point?
3. Does re-execution converge to the same end state?

If any answer is "it depends on what state was left behind," the operation needs reconciliation or another explicit failure and delivery contract.
