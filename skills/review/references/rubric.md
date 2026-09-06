# Review criteria

Apply relevant criteria without requiring a finding from each category.

## Behavior and contracts

Trace whether the implementation meets its requirements, including callers and boundaries. Show how input or state reaches the claimed failure. Examine error handling, authorization, data integrity, concurrency, and retries where relevant.

For a project-rule violation, cite the rule and show that it applies to the reviewed code. Report observed formatter or linter failures under verification without repeating each as a separate finding; do not assume checks passed or will catch an issue.

Check whether a fix addresses the cause at its owner. Establish the underlying contract violation before replacing a guard or fallback.

## Simplicity

Identify unnecessary validation, forwarding layers, unused flexibility, compatibility paths, or extra states. Show how simplifying them preserves required behavior. Reject shorter rewrites that hide control flow, combine unrelated responsibilities, or remove useful boundaries.

Apply the same scrutiny to proposed fixes. Preserve protections for real external boundaries, security, data integrity, and concurrency. Avoid defenses for states already ruled out by construction or validation.

## Tests and verification

Check meaningful coverage and whether added, changed, and relevant existing tests detect realistic regressions. Inspect deleted tests for lost protection.

For a questionable test, name the regression its setup and assertions should catch. Flag tests that pass with broken behavior, repeat the implementation, check mock activity while missing the required outcome, or duplicate protection without catching a different failure. Mocks, snapshots, and interaction assertions are useful when they verify the contract.

Recommend a new test only for a consequential failure that existing checks miss. Name the scenario and expected failure; choose the smallest test at the level where that failure is observable. Changed lines, uncovered branches, and coverage percentages alone do not justify more tests. Direct verification can suffice when new automation would not repay its maintenance cost.

Strengthen, replace, or consolidate weak tests. Recommend removal only with evidence that a test catches no meaningful failure, duplicates surviving protection, or covers an obsolete contract. Name the protection that must survive. Manual checks do not replace useful regression coverage. Do not require tests at every layer or for every mechanical fix.

Run focused checks when useful and permitted. Use a disposable copy if demonstrating a test's weakness requires code changes. Distinguish inspecting a test, observing it pass, and demonstrating that it catches the intended failure.
