# Logbook: Reject speculative branches and test-only paths

## Context

Simplicity already required a concrete requirement or reachable failure before adding complexity. It did not say that a reviewer's finding has to meet the same bar, so agents could add branches for edge cases a reviewer agent raised even when no realistic input reaches them. Nothing addressed production flags, parameters, or variables that exist only so tests can use them.

## Decision

Owner's call: in [Simplicity](../../../skills/apply-principles/references/simplicity.md), a hypothetical edge case, including one a reviewer raises, counts as a reachable failure only once its triggering input or state can be named. When its likelihood and the cost of the failure are both low, leave the code and say why. Production code carries no flags, parameters, branches, or state that exist only for tests. Tests go through the public interface or a seam production also uses, and a need for a test-only hook signals a design problem. Released as 0.4.6.

## Rejected

None considered; both rules extend the existing "reachable failure" and "Subtract before you add" guidance.

## Verification and gaps

- `scripts/validate.py` passed.
- The rules have not been tried against a real reviewer finding.
