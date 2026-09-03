---
name: grill-me
description: Relentlessly interview the user to sharpen a loose plan, decision, or idea before acting. Use only when the user explicitly invokes grill-me or asks to be grilled.
---

# Grill me

Interview the user until you reach a shared understanding. Map the idea internally as a design tree: every decision branches into the decisions that depend on it.

This is an inquiry workflow, not planning or implementation. Do not write files, alter the workspace, or act on the resulting direction. Keep the state in the conversation. When the frontier is empty, summarize the resolved direction and ask the user to confirm that the shared understanding is complete.

## Work in rounds

The frontier is every unresolved decision whose prerequisites are already settled. Ask the whole current frontier in one round. Number each question and provide your recommended answer so the user has something concrete to accept, reject, or reshape.

Use this form:

```text
Q1 — <question title>
<question and any useful choices>

Recommendation: <your recommended answer and concise reason>
```

After the user answers, update the design tree and recompute the frontier. A question whose answer depends on another unresolved question belongs in a later round. Do not drip questions one at a time unless the user asks for that style.

## Separate facts from decisions

Finding facts is your job. Use available read-only tools and evidence instead of asking the user for information you can inspect. Delegate factual investigation only when that capability exists and it materially helps; delegation is not required. A running investigation leaves only its dependent questions blocked, so ask the rest of the frontier meanwhile.

The decisions remain the user's. Never turn your recommendation into an assumed answer. Treat “I don't know” as meaningful evidence: if a decision requires something concrete to react to, identify it as ungrillable through conversation and recommend the smallest throwaway prototype or observation needed to answer it.

## Finish deliberately

The session is complete only when every material branch has been visited, no decision is silently assumed, and the user confirms the resulting shared understanding. If the session grows too large, surface the scope problem and propose smaller independent subjects to grill separately. Do not produce or execute an implementation plan unless the user asks after the grilling session is complete.
