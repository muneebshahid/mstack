---
name: implement
description: "Implement features, fixes, refactors, and experiments, then inspect and verify the result."
---

# Implement

Make the requested change. Use judgment on planning and verification depth.

## Approach

- Use [Explain](../explain/SKILL.md) when the affected system needs investigation; reuse existing findings.
- Apply relevant [principles](../apply-principles/SKILL.md).
- Use [Architect](../architect/SKILL.md) when a consequential design choice needs work. Architect stays read-only; Implement owns the edits.
- For failures, follow [Diagnosis](../apply-principles/references/diagnosis.md). Add targeted logs when the failing path is unclear, then remove temporary instrumentation.
- For refactors, establish which behavior must stay the same and use existing checks or a focused comparison to verify it.
- For experiments, name the question and measure it with a small disposable artifact outside the repository.

## Implement and verify

Make the edits yourself; do not spawn an implementation worker. Start larger changes with the smallest useful end-to-end slice.

Inspect the diff and verify each unit. Use [Verification](../apply-principles/references/verification.md) for required checks and the affected runtime surface.

When implementation contradicts an accepted design, return the evidence to Architect and revise the affected work. Local corrections need no redesign.

When a change makes a decision, fixes an incident, or produces findings that future agents would need, write a [Logbook](../logbook/SKILL.md) entry, including rejected approaches and why.

## Completion

Use **Changes**, **Verification**, and **Open issues** unless another format is requested. Include important decisions, observed results, and unresolved gaps. Omit empty sections.
