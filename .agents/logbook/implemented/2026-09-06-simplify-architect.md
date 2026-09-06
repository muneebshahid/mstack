# Logbook: Simplify Architect

Status: implemented
Kind: simplification

## Problem

Architect requires independent proposals and a cross-judge even when constraints settle the design. Architect and Arena repeat candidate instructions, design principles, and output requirements. Forced alternatives, diagrams, scores, and line-count targets add work without establishing a better design.

## Decision

Keep Architect as an explicit-only, read-only design skill with two references: a design template and optional design comparison. The parent designs directly when requirements or precedent settle the approach. Compare two independent proposals when they could resolve a consequential choice or when requested. Remove the public Arena and Grill Me skills without aliases or an interview mode.

Preserve caller usage before types and module choices, relevant grounding, canonical principle selection, and a consistency and simplicity check before handoff. Return Problem and constraints, Proposed design, Decisions and alternatives, and Implementation handoff. Diagrams and sketches are included when useful; alternatives describe choices actually considered.

Keep the distinction between decisions implementation must preserve and details it may adapt. The handoff names verifiable units, the earliest practical check of the riskiest assumption, and evidence that would reopen the design. Implement retains the same worker across a design revision. Architect stays read-only and hands back empirical questions for a bounded prototype.

Rename the two candidate roles to `architect_candidate_a` and `architect_candidate_b`, preserving their assignments. Remove `arena_cross_judge`; optional independent judgment uses `consultant_default`. The parent owns selection and combines ideas only when their contracts and ownership agree. Incomplete comparisons and capability failures remain visible.

## Alternatives considered

- Keep mandatory competition for explicit Architect invocations. Rejected because invoking design help should not require extra models when constraints settle the choice.
- Keep Arena as a general-purpose artifact competition skill. Removed under the approved consolidation; Architect retains design comparison only.
- Preserve the cross-judge as another mandatory phase or dedicated role. Replaced by optional consultation for a disputed choice.
- Force different designs, numerical scoring, fixed diagram and call-site counts, or line-count targets. Removed; actual constraints and verification determine the design and implementation units.
- Retain the separate design-red-flags guide. Removed where it duplicates canonical standards or turns signals into blanket prohibitions.
- Fold Grill Me into an interview mode. Rejected by the user; remove it entirely while preserving shared license notices for retained work.

## Evidence

The parent read Architect, Arena, their prompts and templates, Grill Me, Implement's architecture contract, model profiles and tests, and related records. The approved rewrite uses three Markdown files plus existing explicit-only UI metadata. Caller links, README, model fixtures, third-party attribution, and historical records were updated together.

This supersedes mandatory Arena in [Parent-led Architecture and Implementation](2026-09-03-parent-led-architecture-and-implementation.md) and [Model Diversity](2026-09-03-multi-model-design-and-review.md), and the Grill Me packaging in [Conversation Utilities](2026-09-03-package-explicit-conversation-utilities.md). Historical reasoning remains in those records.

Structural comparison confirmed that both packaged profiles preserve every retained assignment after renaming the candidate roles and removing the cross-judge. Architect, Implement, and Setup MStack passed the bundled skill validator.

Full repository validation passed with 16 skills, 165 relative links, three TOML files, packaged profiles, unit tests, and Logbook records. The initial rewrite reduced Architect and Arena's combined Markdown from 4,506 to 1,124 words. No new tests were added for the prose changes.

Claude Code reviewed the draft through `consultant_default`, with requested and verified served model `claude-fable-5-1` at `xhigh`. It found the handoff compatible with Implement. The parent accepted three corrections: forbid candidate selection workflows, withhold the parent's preference from an optional consultant and audit its writes, and return provenance as Logbook material. The consultant's first validator attempt lacked PyYAML; it retried through `uv` with that dependency. It also found an empty Test Coverage Auditor directory left from its earlier removal, which the parent inspected and removed. No system dependency was installed.

The changes received instruction review and structural checks, not an end-to-end behavioral evaluation of direct design or comparison. The user approved the draft after removing history guidance already covered by Explain and replacing the rerun rules with agent judgment, then authorized committing and pushing it.

## Consequences

Two fewer public skills. Ordinary architecture work needs no extra model; independent comparisons use two candidates and optional consulting. User overrides must rename the candidate keys and remove the retired judge key; README documents this. Existing installations need a refresh to remove old entry points. Implement's broader simplification remains separate work.

## Revisit when

Direct designs miss consequential alternatives, comparisons encourage incompatible combinations, or implementation cannot distinguish local corrections from evidence that invalidates the design.
