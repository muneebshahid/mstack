---
name: architect
description: "Design a consequential change without implementing it. Use when explicitly invoked by the user or an active workflow; compare independent designs when useful or requested."
---

# Architect

Design a change that fits its callers and requirements. Return a proposed design and implementation handoff.

## Boundary

Architect is read-only, including when called from an implementation workflow. Keep prompts and candidate artifacts outside the repository. Save a design file only when requested; this does not authorize source changes. If a decision needs executable evidence, propose a bounded experiment through [Implement](../implement/SKILL.md). Continue independent design work where useful and leave evidence-dependent choices open.

## Understand

Investigate behavior, callers, ownership, and integration constraints; separate observed constraints from assumptions and open questions.

Use [Apply Principles](../apply-principles/SKILL.md) for relevant standards.

## Design

Start with realistic caller usage, then derive types, operations, ownership, and module boundaries. Use [Design template](references/design-template.md) for the result.

Design directly when requirements or established practice settle the approach. Use [Compare designs](references/compare-designs.md) when competing proposals could resolve a consequential choice, or when the user requests them.

The parent chooses the design, checks that usage, types, data flow, failure behavior, and sequence agree, removes unjustified machinery, and records significant rejected alternatives.

Use [Review](../review/SKILL.md) when critique would help or is requested.

## Hand off and revise

Return the design and stop.

Name the decisions implementation must preserve, details it may adapt, and evidence that would require revisiting the design. Put the smallest practical end-to-end check of the riskiest assumption early in the implementation sequence; identify prerequisites when it cannot come first.

When implementation returns evidence contradicting a decision the design must preserve, or repeated workarounds expose a structural problem, revise the design against the affected code and return the revised contract. Local corrections need no redesign.
