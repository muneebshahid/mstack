---
name: principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
---

# Encode Lessons in Structure

Encode recurring fixes in mechanisms (tools, code, metadata, automation) instead of textual instructions. Every error, human correction, and unexpected outcome is a learning signal. Capture it, route it, and close the loop.

**Why:** Textual instructions are easy to miss. They require the reader to notice, remember, and comply. Structural mechanisms (lint rules, metadata flags, runtime checks, automation scripts) enforce the rule without cooperation.

**Pattern:**
When evidence shows a correction or failure mode is recurring:
1. Ask: can this be a lint rule, a metadata flag, a runtime check, or a script?
2. If yes, choose the lightest mechanism that reliably prevents the recurrence, encode it, and delete superseded instructions
3. If no (genuinely requires judgment), make the instruction more prominent and add an example of the failure mode

**Pick a proportionate rung.** Prefer an unrepresentable state, lint or banned API, canonical helper, runtime check, or focused automation according to recurrence, impact, and enforcement cost. Do not add organization-wide machinery for an isolated correction.

**Corollary:** Don't paper over symptoms. If the fix is structural, ONLY use the structural fix. The instruction IS the symptom.

**Feedback loop:**
- **Evaluate every correction.** When the human intervenes or tests fail, decide from evidence whether it is a one-off or a pattern.
- **Route to the right layer.** One-off -> brain note. Recurring fix -> skill or lint rule. Systemic issue -> principle.
- **Close the loop.** Don't just record. Apply now or create a concrete todo.

**Anti-patterns:**
- Acknowledging without recording ("I'll keep that in mind" does not persist)
- Recording without routing (a brain note about a lint rule that should exist is wasted unless the lint rule gets implemented)
- Fixing without generalizing (fixing one instance while leaving the recurring pattern intact)
