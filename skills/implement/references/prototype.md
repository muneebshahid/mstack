# Prototype

Use this mode when a disposable experiment can settle an observable uncertainty more cheaply than discussion. Own the decision, not the code. The result is evidence and a recommendation; production implementation follows [Feature](feature.md), while architectural interpretation may pass through read-only [Architect](../../architect/SKILL.md).

## 1. Name the decision

- State the exact layout, interaction, behavior, timing, performance, or technical fork the prototype must decide.
- Define the observation that would favor each option. If no decision depends on the result, do not prototype; use [Feature](feature.md).
- For user or caller experience, read [Experience First](../../principle-experience-first/SKILL.md) and evaluate from that user's seat.

## 2. Explore cheaply

- Read [Exhaust the Design Space](../../principle-exhaust-the-design-space/SKILL.md). Build two or three genuinely different variants at the cheapest fidelity that exposes the tradeoff. One design with cosmetic flavors does not count.
- Default to a fresh operating-system temporary directory outside the repository. Use the lightest suitable artifact: a small visual mock, script, benchmark, replay, or switchable set of variants. If the user explicitly requires repository-local placement, use a path that is ignored and excluded from builds, imports, packaging, and test discovery.
- Read [Subtract Before You Add](../../principle-subtract-before-you-add/SKILL.md) and the Laziness Protocol in [Minimize Reader Load](../../principle-minimize-reader-load/SKILL.md). Minimize the instrument and setup, not the number of meaningful alternatives.
- Apply [No Comments](../../principle-no-comments/SKILL.md). Throwaway status does not require commented code or rationale; keep rationale in the prototype report.
- Do not add production abstractions, compatibility, migrations, generalized types, defensive layers, or a test suite unless one of those is the property being tested. A prototype is not a low-quality first draft of the final implementation.

## 3. Observe the real question

- Read [Prove It Works](../../principle-prove-it-works/SKILL.md), interpreting proof as direct observation of the decision variable.
- For visual or interaction work, render and drive each variant and capture comparable screenshots or recordings.
- For behavioral, runtime, or performance work, log or print the relevant output, timing, state transition, or trace. Assertions are optional; the observation is the evidence.
- Keep inputs and conditions comparable across variants. Record uncertainty and observer effects rather than smoothing them away.

If repetition or measurement error makes a tiny rerunnable harness worthwhile, apply [Build the Lever](../../principle-build-the-lever/SKILL.md); the harness should remain smaller than the uncertainty it resolves.

## 4. Decide and hand off

- Compare the variants, state tradeoffs, and recommend one direction based on the observations.
- For an architectural question, feed the evidence to read-only [Architect](../../architect/SKILL.md). For intended production behavior, hand the chosen direction to [Feature](feature.md) and reimplement it under production principles.
- Do not copy the prototype wholesale into production, commit it, open a pull request, or deploy it unless the user explicitly changes its status and authorizes that action.
- Keep the temporary artifact through comparison and user review when it is needed as evidence; label it disposable and report its absolute path and ephemeral status. Otherwise remove it before completion. Remove repository-local scratch before completion unless the user explicitly requests retention; retained repository-local scratch must remain ignored and build-excluded.

The remaining architecture and delivery principles are intentionally not loaded unless the experiment is directly testing one of their properties. Production rigor belongs to the subsequent Feature, Bug Fix, or Refactoring workflow.

Reply with the decision tested, variants, direct observations, tradeoffs, recommendation, uncertainty, and scratch artifact status.
