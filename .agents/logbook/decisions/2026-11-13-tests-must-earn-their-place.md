# Logbook: Tests must earn their place

## Context

Since the testing reference went with [Implement](2026-11-01-implement-in-the-running-agent.md), no MStack text has said which tests to write, a gap [Remove Verification](2026-11-01-remove-verification.md) noted. In a repository built by agents under these principles, a review of 259 tests found 58 that could fail only if the database, a library, or the language stopped honoring a declaration, or that repeated a check made at another layer. Seven of them existed only because a per-file coverage rule failed without them. Simplicity already asked for a reachable failure before adding complexity, but its wording covered code, and agents did not apply it to tests.

## Decision

Owner's call: [Simplicity](../../../skills/apply-principles/references/simplicity.md) holds tests to the same bar as code. A test stays when it fails because logic the project wrote is wrong, written once at the layer that owns the logic. Tests of a declaration the library, language, or database enforces, repeats of another layer's check, and guards against a failure nobody can name are left out. When a coverage rule seems to demand such a test, change what the rule measures.

The Apply Principles catalog sends an agent to Simplicity when it decides which tests to write, since nothing else would lead it there while testing. Released as 0.4.10.

## Rejected

- **Restoring a testing reference:** one paragraph extends the "reachable failure" rule already in Simplicity; a separate reference would restate it.
- **Leaving the rule to each repository's instructions:** the over-testing came from agents' defaults, not from one repository.

## Verification and gaps

- `scripts/validate.py` passed.
- The rule came from removing tests. It has not been tried on an agent writing tests for new code, so whether it stops the same kinds being written is unknown.
- It does not say when a test is required.
