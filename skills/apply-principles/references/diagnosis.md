# Diagnosis

## Fix root causes

Reproduce the failure when possible and use observations to distinguish plausible causes. Trace the symptom to its state, owner, and other callers using the same logic. Fix the defect at that owner and check related paths within scope; report affected paths outside it.

Determine whether a guard or workaround enforces a real boundary or merely hides a contract violation. Preserve necessary validation and integrity checks. When reproduction is unavailable, obtain the actual error, state, or focused instrumentation before guessing at a fix.

For failures after restart, inspect persistent state, caches, locks, and configuration. If clearing state changes the result, investigate its validation, reconciliation, and ownership. Report unresolved causes and verification gaps.
