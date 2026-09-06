---
name: architect
description: "Design a consequential change without implementing it. Use when explicitly invoked by the user or an active workflow; compare independent designs when useful or requested."
---

# Architect

Design a change that fits its callers and requirements. Return a proposed design and implementation handoff.

## Boundary

Architect is read-only, including when called from an implementation workflow. Keep prompts and candidate artifacts outside the repository. Save a design file only when requested; this does not authorize source changes. If a decision needs executable evidence, hand back a bounded [Prototype](../implement/references/prototype.md) question and stop until the evidence is available.

## Understand

Use [Explain](../explain/SKILL.md) to understand relevant behavior, callers, ownership, and integration constraints. Reuse established findings. Distinguish observed constraints from assumptions and unanswered questions.

Use [Apply Principles](../apply-principles/SKILL.md) to select and read the relevant standards. Apply [Source Style](../apply-principles/references/source-style.md) to sketches. Keep design rules in those references rather than building another checklist here.

## Design

Start with realistic caller usage, then derive types, operations, ownership, and module boundaries. Use [Design template](references/design-template.md) for the result. Include only the sketches and diagrams needed to inspect the design.

Design directly when requirements or established practice settle the approach. Use [Compare designs](references/compare-designs.md) when competing proposals could resolve a consequential choice, or when the user requests them. Do not manufacture alternatives for a settled decision.

The parent chooses the design and checks that usage, types, data flow, failure behavior, and implementation sequence agree. Check complexity before handoff: remove unjustified machinery while preserving required behavior and useful boundaries. Record significant rejected alternatives and why they lost.

Use [Review](../review/SKILL.md) only for requested adversarial or multi-model critique. Independent design comparison does not require another review panel.

## Hand off and revise

Return the design and stop. The user or calling workflow decides whether to proceed through [Implement](../implement/SKILL.md).

Name the decisions implementation must preserve, details it may adapt, and evidence that would require revisiting the design. Put the smallest practical end-to-end check of the riskiest assumption early in the implementation sequence; identify prerequisites when it cannot come first.

When implementation contradicts a required contract, ownership decision, boundary, dependency, shared-state assumption, or failure policy, reconsider the design using the affected code and evidence. Repeated workarounds can also reveal a structural problem. Routine local corrections and explicitly flexible details do not require redesign. Return the revised contract to the calling workflow, which retains any existing implementation worker.

Include the reasoning, alternatives, evidence, and gaps needed for the parent to write a Logbook record. Architect does not write project records itself.
