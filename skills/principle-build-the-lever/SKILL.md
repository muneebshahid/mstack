---
name: principle-build-the-lever
description: "Apply to repetitive, large, error-prone, or audit-sensitive work when a small codemod, script, generator, or delegate contract makes execution reproducible and reviewable."
---
# Build the Lever

When scale, repetition, error risk, or reproducibility will repay the cost, build the smallest tool that does or proves the work instead of repeating it by hand.

**Why:** Two payoffs. Throughput: a codemod, generator, or script does the work the same way every time and reruns for free. Confidence: the tool is one artifact a reviewer can read and rerun to check the work. Hand-done changes can only be re-verified by redoing them. A deterministic script turns "trust me" into "run this".

**Decision test:** Build the lever when it is cheaper than repeated manual work or materially improves confidence. Skip it when direct work is smaller, clearer, and just as easy to verify. Never build a framework to automate a handful of obvious edits.

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning it on that unit and diffing against your hand-done version. Make the lever safe to rerun. A reviewer will.
- Codemod or script for edits, generator for repetitive files, a dump-to-sqlite query for analysis, a rerunnable check for verification.
- A deterministic lever beats fan-out. If the tool can process every unit in one pass, run it yourself; don't fan out delegates to hand-apply what a script can do.
- When you fan work out to subagents, write the lever as a skill they all read: the recipe, the verification contract, and the do-not-touch fences in one artifact, so every delegate inherits the same hardened version instead of re-explaining it per prompt and watching each one drift. Keep it outside the delegates' write scope so they can't quietly edit the contract.
- Applying this principle produces a concrete rerunnable artifact. If no artifact is warranted, report that the principle was considered but not applied.
- Commit the lever when the work outlives the session, so the next run reruns it instead of redoing it.

**Balance:** A one-off can still earn a lever when the lever is what makes consequential work checkable. Per the [Laziness Protocol section of Minimize Reader Load](../principle-minimize-reader-load/SKILL.md#laziness-protocol), build the smallest script that does or proves the job, never a framework.

Distinct from [Encode Lessons in Structure](../principle-encode-lessons-in-structure/SKILL.md), which makes a recurring instruction a durable guardrail. This is throughput and reviewability on the work in front of you. For scripting the verification itself, see [Prove It Works](../principle-prove-it-works/SKILL.md).
