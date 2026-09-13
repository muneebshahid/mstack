# Runtime model resolution

Before launching a model role, resolve its assignment:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --role <role-name>
```

Resolve `setup-mstack` from the same installed MStack plugin as the calling skill. Do not use an identically named standalone copy from another installation. The returned assignment is authoritative for that invocation. The payload also reports the detected `host` (`codex` or `claude-code`) and the effective `profile`.

## Runners

- `codex-native`: use Codex's native subagent operation with the resolved model and effort. Request Fast service only when `fast` is true. Available only when the host is Codex.
- `claude-native`: use Claude Code's native Agent tool with the resolved model and effort. Available only when the host is Claude Code.
- `claude-code`: use [Consult](../../consult/SKILL.md) with `--provider claude` and the resolved model and effort. The executable is `CLAUDE_CODE_BIN` or `claude`.
- `codex`: use [Consult](../../consult/SKILL.md) with `--provider codex`, the resolved model and effort, and `--fast` when configured. The executable is `CODEX_BIN` or `codex`.

The two external runners are read-only consultants. They may hold reviewer, critic, judge, candidate, investigator, and synthesizer roles but never `implement_worker`; the resolver rejects that combination.

Start independent assignments in fresh contexts. Reuse retained workers and consultant conversations for related follow-ups. Pass a self-contained prompt, retain the real process or agent identifier, and use that identifier for monitoring, feedback, waiting, and closing.

Runner selection does not relax the calling workflow's authority. Read-only candidates and reviewers remain read-only; implementation workers retain only the bounded write authority granted by Implement.

## Failure behavior

Report malformed configuration or unavailable assignments. [Consult](../../consult/SKILL.md) permits an available native subagent when the external harness cannot run; report the substitution and any lost independence. Do not rewrite saved profiles, silently change an explicit model request, or treat a degraded run as satisfying an unavailable assignment.

When provenance is exposed, report the requested and served model, effective effort, runner, and Fast status. Both external launchers verify the served model; the Codex launcher also verifies effort but cannot verify the service tier. A successful cheap smoke assignment proves mechanics only, not the quality or availability of another production assignment.
