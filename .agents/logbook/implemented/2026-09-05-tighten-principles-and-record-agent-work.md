# Logbook: Tighten Principles and Record Agent Work

Status: implemented
Kind: process

## Problem

The consolidated principles still repeat generic instructions. Typing guidance discourages preventive constraints, temporary-comment exceptions weaken the requested source style, and Logbook can omit meaningful agent work that falls outside its durable-decision threshold.

## Decision

The selector and ten references use shorter wording while preserving their engineering distinctions. Types encode domain constraints proactively. Source Style prohibits comments unless the user explicitly requests them, including in sketches and scaffolds. Concurrent writes and retries remain separate concerns. One internal-migration cleanup rule replaces the migration section; the duplicate outcome-oriented section is removed.

Logbook covers non-trivial changes and meaningful investigation or review outcomes: work performed, accepted and rejected choices with reasons, verification, and gaps. Mechanical or routine local edits remain exempt. The parent writes records using the existing flat lifecycle folders and format. Identify consequential consultant contributions and available session references without creating a persistence subsystem.

Implement, Architect, Arena, TypeScript guidance, and repository instructions follow the revised policies. This broadens the capture threshold in [Log Durable Decisions at the Parent](2026-09-03-log-durable-decisions-at-the-parent.md) and revises the typing and source-style choices in [Consolidate Principles](2026-09-05-consolidate-principles-as-references.md). Their original rationale remains recorded.

## Alternatives considered

- Keep the generic authority passages. Rejected because they repeat governing instructions without helping select a principle.
- Strengthen types only after an observed failure. Rejected because domain constraints should prevent errors before they occur.
- Permit comments in temporary sketches and scaffolds. Rejected because the user wants one source-style rule throughout the work.
- Keep Logbook limited to durable design choices. Rejected because meaningful implementation and negative review outcomes also help explain agent work.
- Record every command or review hypothesis. Rejected because that would obscure the consequential work and choices.
- Delete migration guidance entirely. Rejected in favor of one sentence preventing obsolete dual paths while preserving real compatibility requirements.
- Classify every investigation recommending future work as proposed. Rejected during review: a completed investigation can establish a verified conclusion while recommending unimplemented changes.

## Evidence

The user reviewed the references and accepted these policy changes before implementation. The parent inspected DeepSeek Harness's Agent Notes policy and representative implemented and rejected notes; its broader recording threshold and evidence-backed rejections inform Logbook without importing its directory taxonomy or archive machinery.

The parent directed and inspected edits by the same persistent Luna High worker. The selector, ten references, Logbook skill, and format guide fell from 4,725 to 2,607 whitespace-separated words. The references alone fell from 2,661 to 1,577. These counts measure document size, not model effectiveness.

Fable High reviewed that draft through the read-only Claude Code consultant. The launcher verified `claude-fable-5-1` at high effort and reported no capability failures. The parent accepted clearer agent-inclusive comment wording, explicit investigation lifecycle placement, portable validator resolution, and cuts to duplicated or abstract instructions. Its suggested blanket demotion of investigations recommending further work was rejected. The parent also corrected that lifecycle distinction in the final text.

Repository validation and all six changed-skill validators pass. Fifteen TypeScript example blocks compile with strict checking and unchecked-index protection; the parent verified their exact match to the document and independently ran their compilation and runtime assertions. Five invalid-use cases failed compilation as intended. A generated-module import and two contextual object-argument illustrations were excluded. No production-model behavior benchmark was run.

## Consequences

Shorter guidance should reduce repetition without weakening types, boundary validation, ownership, or verification. Broader Logbook coverage creates more records; updating existing topic records and omitting routine edits limits noise. Required license headers are retained, shebangs remain executable syntax, and generated or third-party material stays outside comment cleanup.

## Revisit when

Compression causes a material misreading, meaningful agent decisions go unrecorded, or routine entries obscure the work and reasons worth retaining.
