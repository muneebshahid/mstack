# Bug Fix

Use this mode when observed behavior contradicts an existing intent or contract. Be scientific: every shipped line must trace to evidence about the failure mechanism. A change that merely might help is a hypothesis, not a fix.

If the user asks only for diagnosis or root cause, complete the investigation and return an evidence-backed causal report without launching the implementation worker or modifying source. Continue into planning and implementation only when the active request authorizes a fix; invoking this workflow does not broaden that authority.

## 1. State the contract and reproduce

- State what should happen, what actually happens, the affected surface, and the smallest observable failure.
- Reproduce on the matching surface when reachable. Capture the failure before changing behavior.
- If reproduction is unclear, intermittent, environment-specific, or hidden behind unknown state, instrument early. Do not spend a long investigation guessing from static code when logs can expose the actual path.

### Diagnostic logging

Treat each diagnostic log as an experiment with a specific question.

- Instrument boundaries, branch decisions, state transitions, retries, concurrent ownership, external calls, and failure translation where the competing hypotheses diverge.
- Include stable operation or correlation identifiers and the minimum useful state, timing, outcome, and error fields needed to reconstruct the path.
- Use an appropriate diagnostic level and avoid secrets, credentials, tokens, personal data, unbounded payloads, and high-volume noise.
- Run or drive the instrumented path and read the resulting evidence. Compare traces across successful and failing runs when possible.
- Account for observer effects in timing- or concurrency-sensitive failures; prefer narrow instrumentation and corroborate with another signal.
- Remove temporary logs as soon as they answer their question. Keep a log only when it is intentional, low-noise observability with a clear operational purpose that would materially shorten future diagnosis.
- If only the user or an inaccessible environment can trigger the failure, first prepare focused instrumentation, then request one precise trigger or capture. Do not hand the investigation itself to the user.

Logging is executable code, not a source comment. It remains subject to scope, privacy, performance, and verification requirements.

## 2. Isolate the mechanism

- Separate direct observations from assumptions before ranking causes. Audit assumptions about inputs, environment, timing, state, deployment, and supposedly impossible paths.
- Read [Fix Root Causes](../../principle-fix-root-causes/SKILL.md). When the cause is not already established by direct evidence, rank plausible hypotheses and retain at least one credible competing explanation. For each serious hypothesis, name the supporting observation, its falsifiable prediction, and the observation that would confirm or refute it. Keep this lightweight for an obvious localized failure.
- Trace from the last known-valid state to the first invalid state. Require an unbroken causal chain from trigger through the violated contract or invariant to the observed symptom.
- Change one experimental variable at a time and explicitly invalidate a failed hypothesis before advancing. If a change appears to work but the result contradicts its prediction, treat the improvement as potentially coincidental and continue investigating.
- Read [How](../../how/SKILL.md) to trace the affected runtime flow and boundaries. Read [Why](../../why/SKILL.md) for regression history, prior incidents, tickets, or design constraints when those sources could discriminate among causes.
- Inspect recent code, configuration, dependency, data, deployment, and environmental differences when they could explain the onset or scope of the failure.
- Binary-search inputs, revisions, components, state, or time windows when that removes large parts of the search space.
- For restart-only failures, inspect persistent state, caches, locks, serialized data, and reconciliation before assuming unchanged code became faulty.
- Replace arbitrary sleeps with condition-based waiting when the investigation or fix depends on asynchronous state. Wait for the required observable condition with an appropriate bound; do not use elapsed time as a proxy for readiness.
- For performance regressions, capture a numerical baseline on a comparable workload and environment before claiming a cause or improvement.

When investigation stops converging, do not accumulate speculative edits. Re-ground by minimizing the reproduction, comparing successful and failing environments, searching relevant history, issues, and pull requests, bisecting where practical, or improving instrumentation. Reconsider the design when evidence repeatedly points to a flawed shape. Non-convergence is a signal to re-ground, not a fixed attempt count.

Load conditional principles when the evidence points there:

- Malformed or stale external data, misplaced validation, leaked mechanism errors, or an ambiguous contract: [Boundary Discipline](../../principle-boundary-discipline/SKILL.md).
- Invalid state combinations, primitive confusion, unsafe casts, or a missing exhaustive case: [Type System Discipline](../../principle-type-system-discipline/SKILL.md).
- Split mutation, side-effect, lifecycle, or failure ownership: [Clear Ownership](../../principle-clear-ownership/SKILL.md).
- Core policy coupled to volatile mechanism or a dependency cycle: [Dependency Direction](../../principle-dependency-direction/SKILL.md).
- Retry, restart, duplicate delivery, or partial-failure defects: [Make Operations Idempotent](../../principle-make-operations-idempotent/SKILL.md).
- A race or concurrent shared write: [Separate Before Serializing Shared State](../../principle-separate-before-serializing-shared-state/SKILL.md).
- Scattered state or branching hides the invariant: [Model the Domain](../../principle-model-the-domain/SKILL.md).

## 3. Plan the smallest causal fix

- Change the confirmed cause at its owner. Do not silence a crash with a guard unless the guard is the correct boundary contract.
- Read [Minimize Reader Load](../../principle-minimize-reader-load/SKILL.md) and [Subtract Before You Add](../../principle-subtract-before-you-add/SKILL.md). Remove invalid paths or redundant machinery before adding another branch.
- If the evidence shows the current shape cannot express the correct invariant cleanly, read [Redesign From First Principles](../../principle-redesign-from-first-principles/SKILL.md). Use [Architect](../../architect/SKILL.md) as a read-only design checkpoint when that redesign is consequential and has multiple viable shapes; it always stops after synthesis, then resume this workflow for the causal fix and same-surface verification.
- For a difficult or repeatedly exercised repro, consider [Build the Lever](../../principle-build-the-lever/SKILL.md): a focused harness, replay, trace parser, or comparison script can make the evidence rerunnable.

## 4. Implement and preserve the failure proof

- When a cheap local regression test can express the bug, read [TDD](../../tdd/SKILL.md) and use its failing-then-passing cadence. Otherwise preserve the smallest realistic repro or trace that directly proves the mechanism.
- Read [Sequence Verifiable Units](../../principle-sequence-verifiable-units/SKILL.md). Capture the failing evidence before the fix, but prefer green commits. A deliberately red commit is exceptional and needs a clear review purpose.
- Apply [No Comments](../../principle-no-comments/SKILL.md). Do not leave workaround prose, suppressions, or commented-out experiments.
- Revert experiments and speculative edits that the evidence disproved. Preserve negative evidence and failed approaches in the final report only when they materially constrain future hypotheses.

## 5. Verify and clean up

- Read [Prove It Works](../../principle-prove-it-works/SKILL.md). Rerun the original reproduction on the same surface, then run the focused regression test and repository-required checks.
- Inspect the final diff. Remove temporary logging and diagnostic scaffolding unless each retained item meets the durable-observability test above.
- Check the surrounding pattern within authorized scope, not only the reported instance. Report material matches outside scope.
- If evidence shows a recurring failure or repeated human correction, read [Encode Lessons in Structure](../../principle-encode-lessons-in-structure/SKILL.md) and add the lightest justified type, test, lint, runtime check, or canonical helper.

Reply with the failure and reproduction, hypotheses ruled out, diagnostic evidence, confirmed root cause, causal fix, logs retained or removed, and same-surface verification. Preserve access or reproduction gaps explicitly.
