# Logbook: Consolidate Explanations

Status: implemented
Kind: simplification

## Problem

How, Why, and Teach repeat investigation, synthesis, and presentation instructions. Their mandatory agent chains make narrow questions expensive, while fixed source sweeps and diagram sequences obscure the reader's actual question.

## Decision

Explain replaces the three entry points. Its source guidance covers mechanics, rationale, and recaps. After user review, the parent replaced detailed investigation procedures with a source menu: code, Git history, Logbook, issue trackers, project documents and discussions, service telemetry, deployment history, and incidents. The agent chooses relevant sources as it investigates. This makes evidence beyond code discoverable without requiring a fixed search sequence.

The parent handles simple questions directly. At the user's subsequent request, Explain delegates useful exploration to one or two native agents through `explain_explorer`: Luna at `max` effort on Codex and Sonnet on Claude Code. Sonnet uses `high`, matching the existing native Sonnet worker setting. Each receives a focused read-only question; the parent checks evidence and writes the explanation. The user corrected the initial cross-vendor Claude profile to retain Sonnet. If delegation is unavailable, the parent continues directly and reports the limitation. Optional independent judgment uses `consultant_default`. The seven How/Why roles, duplicate prompts, speculative connector playbooks, hardcoded personal source profile, and oversized output forms are removed.

Preserve documented reasons versus inference, conflicting accounts, record status, and unavailable versus empty searches. Link useful files and records. Use diagrams when helpful, without fixed counts. The user subsequently required a stable response structure: Summary, Walkthrough, Implications, and Evidence and limits. Keep these headings consistent and scale their contents to the question.

Keep ordinary placement judgment in Explain. Requested adversarial critique routes to Review (then named Interrogate); its scope and judgment guidance now cover subsystems and unimplemented designs without requiring an introducing diff. Caller workflows select canonical principles rather than adding another architecture rubric to Explain.

## Alternatives considered

- Keep separate How, Why, and Teach workflows. Rejected because distinct evidence methods do not require separate public entry points or synthesis agents.
- Add an Explain-specific consultant role. Rejected: existing configuration supplies independent judgment. A later user request added `explain_explorer` for optional Luna exploration, shared by both explorers rather than separate roles for identical assignments.
- Move the old architecture rubric unchanged. Rejected because much of it duplicates canonical principles and encourages hypothetical future-change reviews.
- Require per-claim confidence labels, one diagram, or mandatory Preserve / Change / Avoid / Risk closing labels. Rejected as presentation machinery; preserve uncertainty and relevant implementation constraints in natural language.
- Keep detailed investigation steps and five confidence tiers. Removed after user review: the useful guidance is where to look beyond code, with concise rules for uncertainty and source access.
- Leave response structure entirely open. Replaced after user review: the four-section template makes explanations predictable without restoring the old nine-section reports.

## Evidence

The parent inspected the entry points, historical-confidence guidance, callers, model registry, and Interrogate's file-target support. Fable High independently reviewed the three skill trees and migration dependencies; the launcher verified `claude-fable-5-1` with no capability failures. The parent accepted the single evidence-reference structure and the need to preserve subsystem critique, while rejecting additional roles and rigid output rules.

This supersedes the orchestration in [Separate Mechanics From Historical Rationale](2026-09-03-separate-mechanics-from-rationale.md) and the separate How panel in [Model Diversity](2026-09-03-multi-model-design-and-review.md), preserving their evidence and independent-review principles. The approved implementation adds one skill and one evidence reference, repairs callers, removes the seven retired roles, and reuses existing model fixtures for retained roles. Repository validation passes with 19 skills. All changed skills pass the bundled validator. The parent made the edits directly under the user's explicit instruction, inspected the diff, and ran the repository checks.

Fable High (`claude-fable-5-1`) reviewed the implementation and answered three fixture questions covering mechanics, missing rationale, and a recap. All used the four headings; the rationale stayed unknown, and the recap used a small diagram. The first pass also overstated caller consequences and prescribed an unrequested fix. The parent added a distinction between code facts, conditional risks, and design-quality judgments. A focused recap recheck separated concurrency risk and avoided fix prescriptions but still described an unused parameter as misleading; the final wording explicitly limits design-quality judgments to requested assessments. That last wording adjustment was inspected, not behaviorally retested. Both runs reported no capability failures. These are narrow probes, not a production-quality benchmark.

Before the source-menu revision, the replacement Markdown totaled 912 words versus 14,993 in the three retired skills and their references. File-location guidance was retained despite a suggestion that it duplicated ownership: physical reading anchors help the user navigate the code. A suggested new finding category was unnecessary because Interrogate already supports pre-existing defects and residual risks.

The parent subsequently applied Unslop and the user's source-selection feedback, shortening both Explain files while retaining the response template, useful diagrams, optional consultation, and requested Interrogate routing. The source examples describe when to investigate; no external sources were queried for this edit. Structural validation passed; the revised instructions were not behaviorally retested.

At the user's request, the parent read the installed Show Me skill and merged its presentation guidance into Explain's Walkthrough: choose among pseudocode, call/component/file trees, diffs, Mermaid, and focused HTML; keep prose brief and visuals local to the point. The four response headings and source menu remain. The first merge reduced the examples to a format table. After reviewing a Luna explanation, the user requested the full Show Me body and examples inside Walkthrough instead. The parent restored them, adjusting the nested heading and HTML-opening instruction for Explain. HTML preview uses the available tool rather than a platform-specific shell command. The installed Show Me skill was not modified. Skill and Logbook validation passed for the initial presentation edit. A subsequent Luna Medium run explained a consumer repository's plugin system using the four headings, a sequence diagram, Python examples, and a text lifecycle. The parent passed its output through unchanged for user review; this was an output-style trial, not an independent factual audit.

A fresh Luna Medium run used the same consumer-repository question and prompt with the full Show Me examples. It kept the four headings, used call trees instead of Mermaid, and added subsections and code examples. The response was longer than the first; this single comparison does not establish that the expanded instructions improve clarity. The parent returned it unchanged for user review. The user preferred the full-example output and approved keeping and committing the expanded presentation guidance.

## Consequences

The parent added the optional explorer role and updated both profiles, Explain, and README. Repository and skill validation passed; resolving the role on Codex returned `gpt-5.6-luna` at `max` through `codex-native`. No agents were launched to test this instruction change.

The parent verified Show Me's source and MIT license in `humanlayer/skills` at revision `3c2629142c5d437428269b1b722b08c0b87f574d`. [Third-party notices](../../../THIRD_PARTY.md) now credit the incorporated guidance and examples, and [HumanLayer's license](../../../LICENSES/HUMANLAYER-SKILLS-MIT.txt) is preserved unchanged. The notices also credit the Anthropic sources used in [Review's refinement](2026-09-06-simplify-review.md).

Three entry points become one, and routine explanations require no delegated model. Caller links, model fixtures, setup examples, and historical record links migrate together. Existing user overrides for retired roles must be removed; README documents the migration. The four-section template is intentionally consistent, even for short explanations. The user's current preference for Claude Code consulting guides this editing session without becoming a permanent portable default.

## Revisit when

Direct investigation misses important evidence, recap explanations fail to restore the reader's mental model, or a specific source needs a maintained search procedure.
