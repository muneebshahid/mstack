---
name: implement
description: "Implement features, fixes, refactors, and experiments, then inspect and verify the result."
---

# Implement

Make the requested change. Use judgment on planning and verification depth.

## Approach

- Apply relevant [principles](../apply-principles/SKILL.md).
- Use [Architect](../architect/SKILL.md) when a consequential design choice needs work. Architect stays read-only; Implement owns the edits.
- For failures, add targeted logs when the failing path is unclear, then remove temporary instrumentation.
- For refactors, establish which behavior must stay the same and use existing checks or a focused comparison to verify it.
- For experiments, name the question and measure it with a small disposable artifact outside the repository.

## Implement and verify

Start larger changes with the smallest useful end-to-end slice.

Inspect the diff. Always verify your changes are working if possible.

When implementation contradicts an accepted design, return the evidence to Architect and revise the affected work. Local corrections need no redesign.

When a change makes a decision, fixes an incident, or produces findings that future agents would need, write a [Logbook](../logbook/SKILL.md) entry, including rejected approaches and why.

## Completion

Use **Changes**, **Verification**, and **Open issues** unless another format is requested. Include important decisions, observed results, and unresolved gaps. Omit empty sections.
