# Claude

Use `--provider claude`. The executable is `CLAUDE_CODE_BIN` or `claude`; pass the assigned model and effort.

Claude uses its configured tools and `auto` permissions. Read-only and edit scope are prompt instructions, not a sandbox. Resolve permission prompts within the user's authorization; do not enable blanket permission bypass.

`--allow-writes` adds an `Edit` allow rule scoped to the checkout, covering file creation and edits on fresh and resumed turns. Narrower file assignments remain in the prompt. It does not preapprove edits to added skill directories or arbitrary shell commands; existing deny and ask rules still apply. Report denied writes as blocked work even if the process exits successfully.

The launcher exposes packaged MStack and available personal Codex skills, with auto-memory disabled. It verifies the served model; effort is recorded as requested. Fast is unsupported.
