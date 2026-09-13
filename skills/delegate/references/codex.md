# Codex

Use `--provider codex`. The executable is `CODEX_BIN` or `codex`; pass the assigned model and effort, adding `--fast` when configured.

Fresh and resumed turns use Codex's read-only sandbox by default. `--allow-writes` selects workspace-write; the prompt supplies any narrower edit scope.

The launcher verifies the turn's model and effort from the native rollout under `CODEX_HOME` or `~/.codex`, which must be writable for sessions. Fast is requested; the served tier is unverified.

`--allow-subagents` does not expand sandbox, tool, network, or filesystem access.

A nested harness needs access to its session storage and credentials. Report blocked access; do not bypass permissions or claim completion.
