# Runtime model resolution

Before launching a model role, resolve its assignment:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --role <role-name>
```

Resolve `setup-mstack` from the same installed MStack plugin as the calling skill. Do not use an identically named standalone copy from another installation. The returned assignment is authoritative for that invocation.

## Runners

- `codex-native`: use the host's native Codex subagent operation with the resolved model and effort. Request priority or Fast service only when `fast` is true.
- `claude-native`: use Claude Code's native Agent operation with the resolved model and effort.
- `claude-code`: read the MStack `claude-code` skill and invoke its launcher with the resolved model and effort. The launcher resolves `CLAUDE_CODE_BIN` when set and otherwise uses the `claude` executable; the runner name is not an executable name.

Every delegated role starts in a fresh context unless the calling workflow explicitly requires persistence with the same retained worker. Pass a self-contained prompt, retain the real process or agent identifier, and use that identifier for monitoring, feedback, waiting, and closing.

Runner selection does not relax the calling workflow's authority. Read-only candidates and reviewers remain read-only; implementation workers retain only the bounded write authority granted by Implement.

## Failure behavior

Do not silently fall back to another profile, runner, model, effort, or service tier. If configuration is malformed, the runner is unavailable, the selected model cannot be served, or the native tool cannot express the requested effort, preserve the concrete failure and apply the calling workflow's declared degraded or blocking behavior.

When provenance is exposed, report the requested and served model, effective effort, runner, and Fast status. A successful cheap smoke assignment proves mechanics only, not the quality or availability of another production assignment.
