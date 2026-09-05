# Prototype

Use this mode when a disposable experiment can settle an observable uncertainty more cheaply than discussion. Own the decision, not the code. The result is evidence and a recommendation; production implementation follows [Feature](feature.md), while architectural interpretation may pass through read-only [Architect](../../architect/SKILL.md).

## 1. Name the decision

- State the exact layout, interaction, behavior, timing, performance, or technical fork the prototype must decide.
- Define the observation that would favor each option. If no decision depends on the result, do not prototype; use [Feature](feature.md).
- For user or caller experience, read [Design Decisions](../../apply-principles/references/design-decisions.md) and evaluate from that user's seat.

## 2. Explore cheaply

- Use [Design Decisions](../../apply-principles/references/design-decisions.md) to build the genuinely different variants required by the calling workflow at the cheapest fidelity that exposes the tradeoff. One design with cosmetic flavors does not count.
- Default to a fresh operating-system temporary directory outside the repository. Use the lightest suitable artifact: a small visual mock, script, benchmark, replay, or switchable set of variants. If the user explicitly requires repository-local placement, use a path that is ignored and excluded from builds, imports, packaging, and test discovery.
- Read [Simplicity](../../apply-principles/references/simplicity.md). Minimize the instrument and setup, not the number of meaningful alternatives.
- Apply [Source Style](../../apply-principles/references/source-style.md). Throwaway status does not require commented code or rationale; keep rationale in the prototype report.
- Do not add production abstractions, compatibility, migrations, generalized types, defensive layers, or a test suite unless one of those is the property being tested. A prototype is not a low-quality first draft of the final implementation.

## 3. Observe the real question

- Read [Verification](../../apply-principles/references/verification.md), interpreting proof as direct observation of the decision variable.
- For visual or interaction work, render and drive each variant and capture comparable screenshots or recordings.
- For behavioral, runtime, or performance work, log or print the relevant output, timing, state transition, or trace. Assertions are optional; the observation is the evidence.
- Keep inputs and conditions comparable across variants. Record uncertainty and observer effects rather than smoothing them away.

If repetition or measurement error makes a tiny rerunnable harness worthwhile, apply [Automation and Learning](../../apply-principles/references/automation-and-learning.md); the harness should remain smaller than the uncertainty it resolves.

## 4. Decide and hand off

- Compare the variants, state tradeoffs, and recommend one direction based on the observations.
- For an architectural question, feed the evidence to read-only [Architect](../../architect/SKILL.md). For intended production behavior, hand the chosen direction to [Feature](feature.md) and reimplement it under production principles.
- Do not copy the prototype wholesale into production, commit it, open a pull request, or deploy it unless the user explicitly changes its status and authorizes that action.
- Keep the temporary artifact through comparison and user review when it is needed as evidence; label it disposable and report its absolute path and ephemeral status. Otherwise remove it before completion. Remove repository-local scratch before completion unless the user explicitly requests retention; retained repository-local scratch must remain ignored and build-excluded.

The remaining architecture and delivery principles are intentionally not loaded unless the experiment is directly testing one of their properties. Production rigor belongs to the subsequent Feature, Bug Fix, or Refactoring workflow.

Reply with the decision tested, variants, direct observations, tradeoffs, recommendation, uncertainty, and scratch artifact status.
