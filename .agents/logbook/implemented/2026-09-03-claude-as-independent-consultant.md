# Logbook: Claude Runs as an Independent Consultant

Status: implemented
Kind: process

## Problem

Several workflows need a non-Codex model for independent design, critique, or judgment. Claude Code has its own process, tools, model aliases, permissions, and failure modes, so each caller should not improvise the boundary.

## Decision

Use `claude-code` as the reusable launcher contract. The calling workflow resolves the Claude model and effort from its named MStack role and owns the task and role prompt. The launcher runs Claude with its configured capabilities, exposes MStack's packaged skills plus the user Codex skills directory when present, verifies the served model, and returns result and provenance artifacts.

Prompts strongly require non-mutation for consultant roles, but the workflow does not pretend Bash is physically read-only. Callers audit repository state when mutation would compromise a result. Claude must report missing tools, authentication failures, unreadable paths, and other capability gaps instead of hiding them.

Expose the installed Codex skills directory to Claude so it can read whichever referenced skills a workflow requires. Do not build bespoke prompt packets for every caller.

## Alternatives considered

- Maintain a separate packet of copied skill text per workflow. Rejected because dependency graphs differ and copied text would drift.
- Give Claude a narrowly wrapped read, blob, and grep tool surface. Rejected because Claude Code already has broader capabilities and the restriction would provide misleading assurance.
- Inline Claude launch logic into every orchestration skill. Rejected because model provenance, output capture, and failure reporting need one reusable owner.

## Evidence

- `skills/claude-code/SKILL.md`
- `skills/claude-code/scripts/run_claude.py`
- `skills/arena/SKILL.md`
- `skills/why/SKILL.md`
- `skills/interrogate/SKILL.md`

This record reconstructs the decision from the installed stack because version control begins with this public repository.

## Consequences

Claude sessions are external process runs rather than native children of the current Codex task. Callers must preserve process identity, output artifacts, served-model evidence, and capability failures. A consultant's report is evidence for parent judgment, not mutation authority.

## Revisit when

- Codex gains a native Claude subagent boundary with equivalent tools and model provenance.
- Claude Code offers enforceable read-only permissions that cover every invoked tool.
- Persistent Claude sessions become necessary for materially better iteration.
