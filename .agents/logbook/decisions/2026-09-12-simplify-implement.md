# Logbook: Simplify Implement

Status: implemented
Kind: simplification

## Problem

Implement and TDD contain 5,824 words of overlapping workflows, mode-specific checklists, mandatory delegation, and reporting requirements. Much of this repeats canonical principles or ordinary agent judgment. The user wants aggressive deletion and will add instructions later if actual failures justify them.

## Decision

Keep one Implement entry point with optional persistent-worker delegation and focused testing guidance. Remove the four mode references and standalone TDD skill. A few conditional bullets cover diagnosis, refactoring, and experiments; no mode selection or separate debugging workflow remains.

The parent may implement directly when delegation adds overhead. With a worker, retain continuity, inspect actual edits and checks, and transfer ownership explicitly after failures. Existing model assignments remain unchanged. Revisit design when implementation contradicts it; remove deviation labels, fixed repetition thresholds, line-count targets, and mandatory receipts.

Testing guidance favors consequential regression protection, observed behavior, and test-first when requested or useful. It does not require a new test or a no-test justification for every unit. Existing useful coverage remains valuable. Completion uses Changes, Verification, and Open issues. The parent retains Logbook authorship.

This supersedes mandatory worker ownership and unit-size guidance in [Parent-Led Architecture and Worker-Owned Implementation](2026-09-03-parent-led-architecture-and-implementation.md) and extends the discretion established in [Use Judgment in Refined Workflows](2026-09-06-use-judgment-in-workflows.md).

## Alternatives considered

- Keep four shorter mode workflows. Rejected because their useful differences fit a few bullets.
- Add a debugging reference. Rejected because Diagnosis already covers reproduction and causal investigation; a short logging reminder suffices here.
- Keep mandatory workers, receipts, and fixed architecture triggers. Rejected because they impose overhead even when the parent can complete the task directly.
- Restore generic safety lectures and exhaustive diagnostic techniques. Rejected at the user's request; each future instruction needs evidence that it helps.

## Evidence

The parent inspected Implement, TDD, canonical principles, Architect callers, model resolution, and earlier Logbook records. It edited the workflow directly under the user's authorization, removed obsolete files, and updated the Architect link, README, and invocation prompt. The explicit-only invocation policy is preserved.

At the user's request, an independent `gpt-6-astra` subagent at `max` effort reviewed the committed baseline and replacement draft read-only. It found no integration breakage and supported the deletions and two remaining references. The parent accepted its suggestions to restore an early end-to-end slice, remove redundant production-scope approval wording, and omit empty completion sections.

The user also requested Fable Max. The Claude Code launcher verified `claude-fable-5-1` at `max`, completed successfully, and reported no capability failures. The parent compared repository file hashes before and after consultation; no files changed. Fable found no lost essential behavior or broken integration. The parent clarified the delegation cost comparison, removed repeated sequencing and identifier instructions, placed disposable experiments outside the repository, and added the TDD migration note. It retained the user's logging reminder and explicit rejection of coverage-driven test accumulation. Additional Logbook-search wording was declined because Explain already covers that source.

The user rejected the README migration note and clarified that README should contain only the repository summary, setup, and skill descriptions. The parent removed migration history, internal process details, and duplicated principle listings, and consolidated the skill catalog into one linked table. Third-party credits remain linked.

Repository validation passed with 15 skills, including packaged profiles, manifests, links, hygiene, unit tests, and Logbook records. Implement and the adjusted Architect entry point passed skill validation. This was an instruction review, not a behavioral trial.

## Consequences

Implementation guidance is much smaller and relies more on agent judgment. TDD remains available as a technique within Implement. The public skill count falls from 16 to 15. Existing uncommitted Explain and attribution changes are separate from this consolidation.

## Revisit when

Actual use reveals lost verification, ineffective tests, unnecessary delegation, conflicting writers, or recurring design problems that a specific instruction would prevent.
