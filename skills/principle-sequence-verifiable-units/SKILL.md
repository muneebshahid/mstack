---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer."
---

# Sequence work into verifiable units

Order work as a sequence of coherent units, each ending in a state you can check. The same discipline runs at two altitudes: how you execute and how you deliver.

**Why:** A break caught at the unit that caused it is cheap to localize. A break caught after a batch is buried, and you have already built further on a broken base. Sequencing those same units into a delivery a reviewer can replay turns "trust me" into "watch it go red, then green."

**Execution.** In a sweep, migration, or any run of similar edits, define the smallest meaningful unit that can be verified without leaving the codebase in an incoherent state. Verify that unit before building further on it. A unit may contain several tightly related edits; do not confuse every file save with a checkpoint.

**Foundations.** If a small scaffold concretely benefits every later phase, establish it before feature units. Shared types, CI, linting, and test infrastructure can qualify. First remove dead weight under [Subtract Before You Add](../principle-subtract-before-you-add/SKILL.md), then add only the foundation the planned units will actually use. Each increment should land one coherent abstraction or deepen an existing one rather than spreading special-case coordination through callers.

**Delivery.** Make each meaningful, verifiable change a coherent commit whenever commit authority is part of the task. Prefer green commits suitable for `git bisect`; a deliberately red commit is exceptional and must serve a clear review or testing purpose. Useful story orders include subtraction before reshape, baseline before treatment, scaffold before feature, or a focused regression test with its fix. Each commit should stand on its own and the sequence should read as an argument.

**Pattern:**
- Pick the smallest unit that ends in a check: an edit plus its test, or a commit that stands alone.
- Verify before advancing. Red to green per unit, never deferred to a final batch.
- Order the units so the sequence builds confidence on its own, for you while executing and for a reviewer reading the stack.

**Size guidance:** Aim for roughly 400-500 changed lines per commit. Treat roughly 1,000 changed lines in a pull request as a strong signal to decompose, not a hard limit. Generated files, lockfiles, and genuinely mechanical transformations can justify larger units when the semantic change remains reviewable.

The sequencing complement to the **prove-it-works** principle skill, which keeps each check real, and the **build-the-lever** principle skill, which makes the per-unit check cheap.
