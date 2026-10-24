# Logbook: Use Judgment in Refined Workflows

Status: implemented
Kind: process

## Problem

Some refined skills still prescribe exhaustive reference reading, automatic panels, fixed failure responses, and sequential checkpoints. The user wants agents to choose methods for the task while preserving read-only boundaries.

## Decision

Apply the pass to Apply Principles, Explain, Review, and Architect and their relevant references. State that workflow steps, depth, delegation, and reruns are defaults. Rewrite conflicting instructions rather than relying on a general disclaimer.

Review invocation alone no longer requires a panel. The agent chooses direct or independent review while honoring explicit panel and model requests. Snapshots and tracking IDs are optional where they add value. Failed runs permit judgment about retrying, narrowing, or continuing directly, with honest reporting of the resulting evidence and limits.

Reference reading follows the decision's needs. Reuse context and allow participants to consult further guidance rather than requiring full rereads or forbidding selection. Shared requirements and relevant evidence still support meaningful comparisons.

Architect can continue independent work while an empirical choice remains open. It can request useful critique without automatically adding a panel. Candidate failures and uncertain mutation attribution call for assessing usable evidence rather than an unconditional stop. Read-only assignments, independent proposals, and truthful comparison claims remain intact.

Apply Principles now emphasizes task-specific judgment, and delivery guidance allows related edits to be verified together. Preserve the user's typing, no-comments, meaningful-test, and consistent Explain-output preferences. Keep the complete Show Me examples. Required behavior and evidence remain constraints on the result.

## Alternatives considered

- Add only an overarching flexibility statement. Rejected because nearby mandatory wording would still drive behavior.
- Treat every rule as optional. Preserve explicit user instructions, read-only boundaries, and truthful reporting; discretion applies to the method.
- Extend this pass to Implement, Skill Eval, and all remaining skills. Deferred because the user limited this request to the skills already refined.
- Create a new shared policy skill or reference. Rejected as unnecessary routing for a short instruction that belongs in each workflow.

## Evidence

The parent read the four entry points, review and design references, relevant principle references, and remaining mandatory language. It changed the instructions and inspected the resulting diff for conflicts with the user's existing preferences.

This updates the process rules in [Simplify Review](2026-09-06-simplify-review.md) and [Simplify Architect](2026-09-06-simplify-architect.md), including the earlier automatic panel trigger and candidate reference-selection prohibition. Those records retain the reasons for their earlier choices.

All four changed skills passed the bundled validator. Full repository validation passed with 16 skills, 169 relative links, packaged manifests and model profiles, unit tests, and Logbook records. Diff checks passed. No model consultation or behavioral evaluation was run for this pass. The user approved committing and pushing the changes.

## Consequences

Agents can reduce or adapt process without requesting exceptions. Review quality depends on their judgment about effort and evidence, so reports must make actual execution and remaining limits clear. Model defaults and invocation metadata are unchanged.

## Revisit when

Agents use flexibility to skip requested work, make unsupported claims, violate read-only scope, or still follow unnecessary process despite these defaults.
