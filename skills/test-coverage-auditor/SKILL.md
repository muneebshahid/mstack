---
name: test-coverage-auditor
description: Audit whether tests are appropriate for code changes, not just whether coverage exists. Use when reviewing a diff, pull request, staged changes, or recent implementation to verify that changed behavior is covered end to end where needed, each added or modified test has a clear purpose, and missing, redundant, brittle, or low-signal tests are called out.
---

# Test Coverage Auditor

## Overview

Assess whether the test suite proves the behavior affected by a change. Prioritize test relevance, failure signal, and end-to-end confidence over raw coverage percentage.

## Workflow

1. Identify the review scope from the user request: unstaged diff, staged diff, branch diff, pull request, or specific files.
2. Read the changed production code and infer the intended behavior from the task, PR description, commit messages, tickets, docs, or nearby tests.
3. Build a behavior map: list each user-visible behavior, contract, edge case, state transition, error path, and compatibility promise affected by the change.
4. Read added and modified tests. For each test, identify the behavior it proves, the failure it would catch, and whether it is at the right level.
5. Compare the behavior map to the tests. Mark each behavior as covered, partially covered, untested, or intentionally out of scope.
6. Run targeted tests when useful to validate that the tests pass and fail for meaningful reasons. Prefer focused commands before full suites.
7. Report only high-value gaps and low-signal tests. Avoid asking for tests that do not materially reduce risk.

## Audit Criteria

A good test is one that would fail for a realistic regression in the changed behavior. Treat these as strong signals:

- It exercises the public API, workflow, or boundary that users or callers depend on.
- It asserts behavior, outputs, side effects, persisted state, emitted events, or error contracts rather than only implementation details.
- It covers the risky edge created by the change, not merely the happy path.
- It uses realistic inputs and keeps mocks at system boundaries.
- It would fail if the new code were removed, bypassed, or wired incorrectly.
- It is located near the relevant test suite and follows existing test style.
- It has a clear name that describes behavior, not implementation mechanics.

Treat these as weak or questionable tests:

- Tests that only assert mocks were called when the observable behavior is unverified.
- Snapshot or broad golden tests that are easy to update without understanding the regression.
- Tests that duplicate existing coverage without covering a new branch, contract, or integration point.
- Tests that encode private implementation details and will churn during harmless refactors.
- Tests with vague assertions such as only checking non-null, truthiness, or no exception when stronger behavior should be checked.
- Tests that require excessive setup compared with the behavior being verified.
- Tests added only to increase a coverage metric.

## Test Level Guidance

- Prefer end-to-end or integration tests when the change crosses module boundaries, changes public contracts, wires a new provider/tool/runtime path, or affects user-visible workflow.
- Prefer focused unit tests when the change is a pure decision, parser, serializer, validator, edge-case branch, or error mapping with a stable local contract.
- Prefer regression tests when the change fixes a bug. The test should fail before the fix and pass after it.
- Prefer contract tests when multiple providers, adapters, implementations, or transports must obey the same shape.
- Do not demand an end-to-end test for every helper. Demand end-to-end confidence for tickets or changes whose success depends on multiple components working together.

## Coverage Map Format

Use this internal map while auditing:

```text
Changed behavior:
- <behavior or contract>
  Risk: <what can regress>
  Existing tests: <files/tests>
  Added tests: <files/tests>
  Status: covered | partial | missing | excessive
  Recommendation: <specific test to add/remove/change, if needed>
```

Do not include the full map in the final response unless it helps the user. Use it to produce concise findings.

## Reporting

Lead with findings ordered by risk:

1. Missing high-value coverage.
2. Tests that do not prove the changed behavior.
3. Redundant, brittle, or over-specified tests.
4. Validation that could not be run.

For each finding, include:

- Severity and short title.
- File and line reference when available.
- Changed behavior or risk.
- Why current tests are insufficient or excessive.
- Concrete test direction: level, scenario, assertions, and expected failure mode.

If coverage is appropriate, say so directly and list any residual risk, such as no live provider test, no browser path, or no database-backed fixture.

## Guardrails

- Do not equate line coverage with adequate testing.
- Do not ask for tests just because a line changed.
- Do not prefer unit tests by default when the risk is integration wiring.
- Do not prefer end-to-end tests by default when a small deterministic contract test catches the regression better.
- Do not rewrite or add tests unless the user explicitly asks for implementation. In audit mode, report recommendations.
- Do not ignore deleted tests. Verify whether removed tests were redundant or whether coverage was lost.
- Call out when a test passes for the wrong reason, has no meaningful assertion, or would still pass if the implementation were broken.
