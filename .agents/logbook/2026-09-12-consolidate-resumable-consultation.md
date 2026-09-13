# Logbook: Consolidate Resumable Consultation

Status: implemented
Kind: simplification

## Problem

Separate Claude and Codex consultant skills duplicated instructions and process plumbing. Claude disabled session persistence; Codex captured a conversation ID without exposing resumption. Follow-up questions needed access to the original conversation.

## Decision

Consolidate the two entrypoints into [Consult](../../skills/consult/SKILL.md), using the native CLIs directly. The user explicitly deferred Herdr after its exploratory trial. Retain the existing runner names in model configuration so saved assignments keep working. Choose provider references by the consultant being launched, regardless of the parent harness; shared resumption instructions live only in the main skill.

Keep consultation read-only. Start independent assessments fresh and resume related follow-ups with the native conversation ID held in parent context. If the ID is missing or unusable, start fresh with a summary and report the restart. Native agents use the host’s conversation handles. External reports and logs default to a temporary directory; the parent removes these and temporary input prompts after review. Evaluations can retain evidence through an explicit output directory. Deleting temporary files does not delete the harness conversation.

When the external harness cannot run, the parent may use an available native subagent and must report the substitution and any lost cross-provider independence. The launcher reports failure; it cannot invoke the host's native agent tool or silently replace an explicitly requested model.

This supersedes the separate [Claude](2026-09-03-claude-as-independent-consultant.md) and [Codex](2026-09-03-codex-as-independent-consultant.md) entrypoints. Their original rationale for independent judgment and provider-specific permission boundaries remains relevant.

## Alternatives considered

- Herdr orchestration: explored successfully, then deferred by the user. It is not a dependency of Consult.
- Keep both public skills and repeat the persistence instructions: rejected because provider references can preserve meaningful differences under one workflow.
- Required persistent project/task directories and summary-file resumption: removed after user review because the native ID already identifies the conversation.
- Automatically delete reports when a process exits: rejected because the parent and user may need review or follow-up context.
- Automatically switch providers in the launcher: rejected because native delegation belongs to the host and substitutions must remain visible.

## Evidence

The parent owns skill text, caller migration, integration review, verification, and this record. A Luna `high` implementation worker consolidated the runner and tests; the parent simplified storage and resumption after user review. The configured Fast setting could not be selected through the native delegation tool and is unverified.

Live smoke runs used Haiku `low` and Luna `low` with Fast, keeping production assignments unchanged. Fresh calls returned verified models; Codex resumed the same thread, recalled the prior answer without tools, and its native runtime record confirmed the requested model, effort, checkout, and read-only sandbox. A deliberately missing Claude executable produced a failure record; a fresh native Luna `low` agent answered the same fixture successfully. This establishes native fallback mechanics, not cross-provider independence.

The first Claude run wrote two auto-memory notes when asked to remember the fixture, despite the read-only instruction. The parent preserved evidence and removed only those trial-created notes. Consult now disables auto-memory in the Claude child environment while keeping native conversation persistence. The repeat fresh and resumed calls read or recalled the fixture without writes; the resumed call returned the same native session ID and used no tools. [Claude's documented memory control](https://code.claude.com/docs/en/memory) supports this scoped change.

The parent also identified stale Codex provenance and interruption-record risks during implementation review. Resumed verification must use appended rollout records and the expected conversation ID, and interrupted runs must preserve available session identity. All 18 runner tests passed after the storage revision. Both provider tests delete first-turn artifacts before resuming by ID; default output and completion events are checked for temporary storage and returned identity. The unified suite covers resumption, missing identity, stale rollout evidence, output reuse, default storage location, failed processes, activity redaction, large I/O, descendant-held output, timeout, and interruption. The parent verified both providers live, native fallback, unchanged fixture content, and no new auto-memory notes. Repository-wide validation passed for 13 skills and 134 local links, and all six changed skill validators passed. Smoke evidence was retained; disposable fixtures and duplicate source prompts were removed. No production-model quality claim is made.


A subsequent force-loaded cross-harness smoke test used external Claude Haiku `low` to invoke the staged Consult skill with Codex Luna `low` and Fast. The first attempt stopped before Codex launch because Claude's permission system rejected temporary prompt writes. A process-scoped retry allowed reads in the disposable test directory, writes in its scratch folder, and the specific launcher and cleanup commands, using [Claude's scoped permission settings](https://code.claude.com/docs/en/permissions). No global permissions or blanket bypass were enabled. The same Claude session then read the Codex reference, launched Luna, consumed and deleted first-turn artifacts, and resumed the returned ID. Parent inspection confirmed the same Codex ID, the requested model and effort, read-only sandbox, and correct recall of a marker omitted from the follow-up prompt without tool calls. The fixture remained unchanged. Claude removed its prompts; the parent removed the remaining output, staged skills, scoped settings, and fixture after inspection. Fast remained requested but unverified. This proves invocation and resumption with the scoped grants; the initial permission failure means the default unattended path is not established in this environment. It does not test organic activation or production-model quality.

## Consequences

One public consultation skill replaces two. Process handling and provider mechanics stay in scripts, while callers retain judgment and orchestration. Temporary artifacts require parent cleanup after consumption; retained evaluation evidence remains caller-managed. Claude's read-only role remains an instruction over configured tools; Codex uses its read-only sandbox. An available native fallback can preserve useful analysis but may not provide the requested model diversity.

## Revisit when

Real use shows missing resumption context, output-capture failures, confusing retention, or a reason to support another harness. Resume any Herdr work only when requested.
