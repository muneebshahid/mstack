# Logbook: Add Sharpen and skip Statechart from PStack

## Context

A review of PStack's current skills against MStack looked for ideas MStack had not already merged or removed. Two were evaluated individually: `sharpen`, a short prompt that deepens a task before rewriting it, and `statechart`, which model-checks a TLA+ spec and draws the result as a Mermaid statechart.

## Decision

Add [Sharpen](../../../skills/sharpen/SKILL.md) as an explicit-only conversation utility beside Bro. It asks what a top professional would add, what raw material they would start from, which methods they would use, and what external check would show the result is right, then rewrites the prompt while leaving the user's choices open. It does not start the task. It differs from [Grill Me](2026-09-13-add-grill-me.md), which is an interactive interview; Sharpen is a single pass that returns a better prompt. Explicit invocation matches Bro and Grill Me, because it changes what the conversation produces.

## Rejected

- **Port Statechart.** It depends on about 3,900 lines of TypeScript, Java and TLC installed through mise, a TypeScript-capable runtime, and Cursor's renderer. That exceeds all of MStack's scripts combined, conflicts with the Python-only tooling and portability goals, and serves only protocol and state-flow modeling. Install PStack alongside MStack when that is needed; Show Me can already draw a plain Mermaid state diagram.
- **Fold Sharpen into Grill Me.** Rejected because Grill Me's interview loop would bury a one-pass rewrite.

## Verification and gaps

Repository validation passed. No live Sharpen run has been performed.
