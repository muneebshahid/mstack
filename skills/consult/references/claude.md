# Claude

Use `--provider claude` for the `claude-code` runner. The executable is `CLAUDE_CODE_BIN` or `claude`; pass the assigned model and effort explicitly.

Claude runs with its configured tools and `auto` permissions. Read-only consultation is a role instruction, not a shell sandbox. Check repository changes when mutation would compromise the result. Resolve actual approval prompts within the user's authorization; do not enable blanket permission bypass to make a run pass.

The launcher exposes packaged MStack skills and available personal Codex skills. Auto-memory is disabled. The served model is verified; effort is recorded as requested.
