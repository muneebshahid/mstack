# Logbook: Codex Runs as an Independent Consultant

Status: implemented
Kind: process

## Problem

Claude Code-led workflows need a non-Claude model for independent design, critique, and judgment, exactly as Codex-led workflows need Claude. Codex has its own CLI, sandbox, model slugs, effort configuration, service tiers, and session records, so each caller should not improvise the boundary, and Claude Code should not be a second-class host.

## Decision

Use `codex` as the reciprocal launcher contract to `claude-code` ([Claude Runs as an Independent Consultant](2026-09-03-claude-as-independent-consultant.md)). The calling workflow resolves the model, effort, and Fast setting from its named MStack role and owns the task prompt. The launcher runs `codex exec --json` in Codex's `read-only` sandbox, prepends the same consultant boundary the Claude launcher uses, streams sanitized activity, and verifies the served model and effort from the session rollout Codex writes under its home directory before accepting a result.

The launcher deliberately does not pass `--ephemeral`, because the JSON event stream does not name the served model and the rollout is the only provenance source. Codex does not report the served service tier, so a Fast request is recorded as requested but unverified.

External launchers in both directions are read-only consultants. The resolver rejects them for `implement_worker`; that rule and the `claude-multimodel` profile are owned by [Centralize Model Role Configuration](2026-09-03-centralize-model-role-configuration.md).

## Alternatives considered

- Depend on OpenAI's `codex-plugin-cc` Claude Code plugin. Rejected because it exposes review and rescue commands without a per-role model, effort, and provenance contract, needs Node, and lets Codex write by default in rescue mode. It can coexist with MStack.
- Drive Codex through its app-server protocol. Rejected because `codex exec` already exposes model, effort, sandbox, and JSON events, and a subprocess boundary mirrors the Claude launcher.
- Trust the requested model without provenance. Rejected because multi-model independence depends on knowing which model actually answered.
- Share process plumbing between the two launchers through a common module. Rejected for now because each skill must stay installable on its own; the duplication is contained to two files with matching tests.

## Evidence

- `skills/codex/SKILL.md`
- `skills/codex/scripts/run_codex.py`
- `skills/codex/scripts/test_run_codex.py`
- `skills/setup-mstack/references/runtime-resolution.md`
- `config/profiles/claude-multimodel.toml`

A real `gpt-5.6-luna` `low` Fast run from Claude Code on this repository returned a report, and the launcher verified `gpt-5.6-luna` and `low` from the rollout's `turn_context` record. The rollout's `turn_context` payload carries the served effort in its top-level `effort` field, not the nested `reasoning_effort`; reading the wrong field fails provenance, so the fake-Codex tests mirror the real rollout shape.

## Consequences

Claude Code can now lead every MStack workflow with the same cross-vendor topology Codex has. Callers must treat Codex sessions as external processes, preserve thread identifiers and artifacts, and surface capability failures such as unauthenticated MCP servers that Codex reports on stderr. Each Codex run leaves a rollout in the user's Codex home.

## Revisit when

- `codex exec --json` reports the served model and service tier directly, which would allow `--ephemeral`.
- Claude Code gains a native Codex subagent boundary with equivalent provenance.
- A workflow needs a write-capable Codex worker from Claude Code.
