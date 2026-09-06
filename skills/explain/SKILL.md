---
name: explain
description: "Explain how code works, why a design was chosen, where behavior belongs, or what changed. Use for walkthroughs, visual explanations, teaching, architecture questions, and change recaps."
---

# Explain

Help the user understand the system. Investigate read-only; keep design critique and fixes to requested assessments.

## Sources

Read [Evidence](references/evidence.md) for sources to consider. Choose what could answer the question and follow useful leads. Check relevant connected sources when code leaves questions about requirements, decisions, or production behavior. Do not search every source by default.

- **Mechanics:** code, tests, configuration, and runtime evidence.
- **Rationale:** Git history, Logbook records, tickets, discussions, and design records. Do not infer the author's reasons from code alone.
- **Recap:** the diff against a stated baseline, including relevant uncommitted work, plus records explaining the changes.

## Optional review

Investigate directly by default. Consult another model when independent research or judgment would help, using `consultant_default` through [model configuration](../setup-mstack/references/runtime-resolution.md) and its runner. Give it a focused question and relevant context; check its evidence before using the answer.

Use [Interrogate](../interrogate/SKILL.md) for requested adversarial or multi-model critique. Include the subsystem or design, its requirements, and existing findings.

## Response template

Use these four headings in order unless the user requests another format. Skip the preamble and keep prose brief. Do not invent content to fill sections. Cite sources inline. Internal callers can reuse findings without a separate user-facing response.

### Summary

Answer the question. State the scope or comparison baseline.

### Walkthrough

Explain how it works, why it was chosen, or what changed. When a visual helps, choose the smallest view that makes the point clear:

| Topic | View |
| --- | --- |
| Logic or an algorithm | Pseudocode |
| Runtime calls | Call tree |
| UI structure | Component tree with relevant state and module boundaries |
| File responsibilities | Shallow file tree |
| Schema relationships, component interactions, data flow, or state transitions | Mermaid ER, sequence, flow, or state diagram |
| Changes to an existing shape | `diff` of the relevant code, tree, or pseudocode |
| Visual layout, state comparison, or a concept too dense for an inline view | Focused HTML diagram, infographic, or short slide deck |

Keep only the calls, files, states, and boundaries needed for the question. Show the whole block when most of it is new, omitted context would hide ownership or order, or the user needs a copyable target. Label illustrative sketches and proposed shapes so they cannot be mistaken for current code.

Place each visual beside the brief explanation it supports. Use several only when each adds something useful. For HTML, use real labels and data, match the product's visual style when relevant, support desktop and mobile, and open the file with the available preview tool.

### Implications

Explain consequences relevant to the question. State any assumptions behind risks or design judgments. Before implementation, identify constraints to preserve.

### Evidence and limits

Link the most useful files and records. Identify inferred reasons, conflicting evidence, unanswered questions, and relevant sources you could not check.
