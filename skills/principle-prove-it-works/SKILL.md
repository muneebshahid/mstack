---
name: principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.'"
---

# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

**Pattern:** After completing any task, ask: "how do I prove this actually works?"

Gather fresh evidence after the relevant change. Match each completion claim to the smallest direct check that can prove it, and report material unexercised surfaces as gaps. One green check is not evidence for unrelated claims.

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

Different checks support different claims:

- Unit tests prove focused behavior within their test boundary.
- Integration tests prove connected components and contracts.
- End-to-end or browser exercises prove the user-visible path that was actually exercised.
- Type checking proves static consistency, not runtime correctness.
- Linting and formatting prove source conformance, not behavior.
- Builds prove compilation or packaging, not deployed behavior.
- Requirements review proves coverage of the requested intent.
- Runtime logs and traces prove only the exercised path and environment.

For code and features, run the closest matching surface. Build when compilation or packaging is relevant, exercise the actual behavior, and trace the full input-to-output chain when the claim crosses components. Do not add a broader test harness when a smaller direct check proves the claim with equal confidence.

Delegation: trust artifacts, not self-reports.
When verifying delegated work, inspect the actual output artifact (git diff, file contents, runtime behavior), not the delegate's summary. Agents report what they intended, not always what happened.

## Preserve repeatable proof when it earns its cost

Use a deterministic script or harness when repeatability, complexity, risk, or future regression value repays its maintenance cost. Keep it as small as the claim permits. A one-time direct observation is enough when it is reliable and the automation would be more machinery than evidence.

Keep the artifact visible for the human. Commit it only for large or complex work where the trail has to be auditable later, like a big port or migration (the **show-me-your-work** skill). Most work just needs it visible, not committed.

## Browser-visible work

For a user-facing browser change, report each materially affected journey as **Pass**, **Fail**, or **Skip** with a reason. Cover only relevant states:

- The primary path.
- Error and empty states.
- Re-entry or refresh.
- Responsive behavior.
- Permission or session states.

Use the host-native browser capability and inspect the visible result. Do not manufacture a full journey matrix for states the change cannot affect.
