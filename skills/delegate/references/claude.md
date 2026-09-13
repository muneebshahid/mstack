# Claude

Use `--provider claude`. The executable is `CLAUDE_CODE_BIN` or `claude`; pass the assigned model and effort.

Claude uses its configured tools and `auto` permissions. Read-only and edit scope are prompt instructions, not a sandbox. Resolve permission prompts within the user's authorization; do not enable blanket permission bypass.

`--allow-writes` does not grant Claude tool permissions. Report denied writes as blocked work even if the process exits successfully.

The launcher exposes packaged MStack and available personal Codex skills, with auto-memory disabled. It verifies the served model; effort is recorded as requested. Fast is unsupported.
