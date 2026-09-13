# Codex

Use `--provider codex`. The executable is `CODEX_BIN` or `codex`; pass the assigned model and effort, adding `--fast` when configured.

Fresh and resumed turns keep the checkout read-only unless `--allow-writes` enables workspace writes. The prompt supplies narrower edit scope.

The launcher verifies the turn's model and effort from the native rollout under `CODEX_HOME` or `~/.codex`, which must be writable for sessions. Fast is requested; the served tier is unverified.

With `--allow-subagents`, the launcher uses a per-process permission profile enabling network access, temporary files, and Claude's `projects`, `session-env`, and `debug` directories under `CLAUDE_CONFIG_DIR` or `~/.claude`. This supports nested Claude authentication and resumable sessions while preserving the checkout's write setting. User configuration is unchanged.

The parent must grant this access before launch; a child cannot relax an enclosing sandbox. Report unsupported permission profiles or remaining access failures without disabling the sandbox.
