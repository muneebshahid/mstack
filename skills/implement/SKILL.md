---
name: implement
description: "Implement features, fixes, refactors, and experiments. Work directly or delegate, then inspect and verify the result."
---

# Implement

Make the requested change. Use judgment on planning, delegation, and verification depth.

## Approach

- Use [Explain](../explain/SKILL.md) when the affected system needs investigation; reuse existing findings.
- Apply relevant [principles](../apply-principles/SKILL.md), including [Source Style](../apply-principles/references/source-style.md) for owned edits.
- Use [Architect](../architect/SKILL.md) when a consequential design choice needs work. Architect stays read-only; Implement owns the edits.
- For failures, follow [Diagnosis](../apply-principles/references/diagnosis.md). Add targeted logs when the failing path is unclear, then remove temporary instrumentation.
- For refactors, establish which behavior must stay the same and use existing checks or a focused comparison to verify it.
- For experiments, name the question and measure it with a small disposable artifact outside the repository.

## Implement and verify

Work directly when delegation would cost more than it saves. Otherwise use a [persistent worker](references/implementation-worker.md). Start larger changes with the smallest useful end-to-end slice.

Inspect the diff and verify each unit. Use [Testing](references/testing.md) to judge whether new tests would help and [Verification](../apply-principles/references/verification.md) for required checks and the affected runtime surface.

When implementation contradicts an accepted design, return the evidence to Architect and revise the affected work. Keep an existing worker for the revised design. Local corrections need no redesign.

The parent maintains [Logbook](../logbook/SKILL.md) records for non-trivial work, including accepted and rejected approaches and why.

## Completion

Use **Changes**, **Verification**, and **Open issues** unless another format is requested. Include important decisions, observed results, and unresolved gaps. Omit empty sections.
