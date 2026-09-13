# Codex

Use `--provider codex` for the `codex` runner. The executable is `CODEX_BIN` or `codex`; pass the assigned model and effort, adding `--fast` when configured.

Fresh and resumed turns run in Codex's read-only sandbox. The launcher verifies the current turn's model and effort using the native rollout under `CODEX_HOME` or `~/.codex`. That location must be writable for session storage.

Fast is requested, but the served tier is not verified.
