# Logbook: Simplify Review

Status: implemented
Kind: simplification

## Problem

Interrogate repeats review and orchestration rules across its entry point, rubric, reviewer prompt, and lead-judgment guide. Its adversarial language and consensus weighting encourage speculative findings. A separate test-coverage auditor adds another workflow and can encourage more tests without useful regression protection.

## Decision

The user chose `review` as the public name because it describes the task without encouraging adversarial theater. Rename the directory, invocation metadata, caller links, plugin prompt, and configured roles to `review_reviewer_a` and `review_reviewer_b`. Keep their model, effort, runner, and Fast assignments unchanged; README documents migration of user overrides.

Remove Test Coverage Auditor entirely, including its UI metadata. Keep a test-usefulness clause in Review's criteria: check meaningful coverage, what realistic regression each questionable test would catch, and protection lost through deleted tests. Missing lines or branches alone do not justify new tests. Strengthening, replacing, consolidating, or removing weak tests can be preferable to adding more; preserve any useful protection.

Keep the two configured independent reviewers for explicit skill invocations and requested adversarial or multi-model review. Other reviews run directly, including focused tests-only or simplicity-only requests. Preserve target resolution, common review evidence, selected principles, runner identity and failure handling, read-only boundaries, and parent validation. No model assignments change.

Fold lead judgment into the entry point and remove its separate guide. Judge findings by evidence rather than reviewer agreement. Check both the reported problem and the complexity of its proposed correction. Keep stable finding IDs and reviewer attribution, but drop principle receipts and the separate agreement map. The final report uses Verdict, Findings, Rejected suggestions, and Verification and limits.

## Alternatives considered

- Merge the entire auditor workflow under Interrogate. Rejected by the user: retain the useful question about test quality without behavior maps, exhaustive checklists, or pressure to add tests.
- Require a two-model panel for every narrow assessment. Rejected because focused reviews can be handled directly; explicitly requested panels still run.
- Treat consensus as high confidence or single-implementation abstractions as premature. Removed because evidence and contract value determine whether a finding is justified.
- Collapse all instructions into one file. Keep the reviewer prompt and review criteria separate so panel members receive their own bounded assignment without the parent's orchestration and verdict instructions.
- Import Anthropic's four-reviewer panel, per-finding scorers, or numeric confidence cutoff. Rejected as extra orchestration; retain the parent's evidence checks. Do not adopt automatic PR exclusions or discard relevant pre-existing defects when the user includes them in the target.
- Import Code Simplifier's automatic edits and language-specific preferences. Rejected because Review is read-only and uses the project's standards. Retain its warning against compact rewrites that make code harder to follow.

## Evidence

The parent read the existing Interrogate files, Test Coverage Auditor, canonical Simplicity and Verification references, runtime model resolution, README, and the earlier model-diversity record. Repository search found the removed skill in its own files and README, with no dedicated model role to retire. The parent rewrote the review instructions and repaired the historical lead-judgment reference.

This refines [Model Diversity](2026-09-03-multi-model-design-and-review.md), retaining independent reviewers and parent ownership of the final judgment. The user reviewed the files, requested removal of two scope sentences, and approved committing and pushing the changes.

Claude Code reviewed the instructions through the configured consultant role: requested and verified served model `claude-fable-5-1`, effort `xhigh`, with no reported capability failures. The parent accepted clarifications for ordinary-review routing, known constraints and Logbook decisions, prompt hygiene, test-removal evidence, and testing at the level where the failure is observable. A concern that pre-existing defects had no place was already covered by target scoping; the parent made their label explicit in the report rather than adding another category.

The removal rule now distinguishes avoiding unnecessary new automation from deleting useful regression coverage. A proposed deletion needs evidence of ineffective assertions, redundant surviving protection, or an obsolete contract. UI metadata was updated to match the review scope.

Repository validation passed with 18 skills, 174 relative links, packaged model profiles, unit tests, and Logbook records. The revised skill passed the bundled validator and diff checks. This was an instruction review; the new workflow has not been behaviorally tested. Final wording and metadata adjustments received focused validation.

After the rename, full repository validation and the bundled validators for Review, Explain, Architect, and Setup MStack passed. A structural comparison confirmed that both profiles differ only in the renamed reviewer role keys. Active instructions contain no old skill references; the old name remains in migration guidance and historical records.

The parent inspected Anthropic's [Code Review README](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md) and [Code Simplifier agent](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md). Adopted explicit citation of applicable project rules, targeted history checks, and rejection of compact rewrites that obscure control flow or combine unrelated responsibilities. Routine formatter and linter failures are reported once under verification, using observed results rather than assuming the checks catch an issue.

An Unslop pass tightened the entry point, criteria, and reviewer prompt from 1,426 to 1,263 words while retaining scope, panel handling, evidence requirements, and test-addition and removal rules. Skill, Logbook, and diff validation passed. This source comparison and prose revision did not include another consultant or behavioral test.

The user subsequently made process requirements adaptable in [Use Judgment in Refined Workflows](2026-09-06-use-judgment-in-workflows.md). That pass supersedes fixed panel triggers, exhaustive reading, and unconditional failure stops while preserving read-only boundaries and explicit user requests.

## Consequences

One fewer public skill and one fewer review reference. Reviewers still assess test coverage, but every proposed addition needs a concrete failure and every proposed removal must account for the protection it provided. Existing installations may retain the removed skill until refreshed.

## Revisit when

Reviews still invent test requirements, miss consequential untested behavior, recommend deleting useful protection, or let consensus replace independent verification.
