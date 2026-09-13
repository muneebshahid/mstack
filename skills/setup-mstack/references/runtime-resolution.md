# Runtime model resolution

Resolve each role using the Setup MStack script from the same plugin installation as the calling skill:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --role <role-name>
```

Use the returned assignment, host, and preset for that invocation. The resolved roles form the active profile.

## Configuration

The user file selects `preset = "codex-preset"` or `preset = "claude-preset"` and overrides individual role fields under `[roles.<role>]`. Its location is `MSTACK_CONFIG`, otherwise `$XDG_CONFIG_HOME/mstack/models.toml`, otherwise `~/.config/mstack/models.toml`.

`CLAUDECODE` identifies a Claude Code host; otherwise the resolver assumes Codex. `MSTACK_HOST=codex` or `MSTACK_HOST=claude-code` overrides detection. Without a selected preset, the resolver uses the host’s packaged default.

## Runners

| Runner | Invocation |
| --- | --- |
| `codex-native` | Codex's native subagent tool. |
| `claude-native` | Claude Code's native Agent tool. |
| `claude-code` | [Consult](../../consult/SKILL.md) with `--provider claude`. |
| `codex` | [Consult](../../consult/SKILL.md) with `--provider codex`. |

Pass the resolved model and effort, requesting Fast when configured. Native runners require their corresponding host. External runners are read-only consultants and cannot serve as `implement_worker`.

## Verification and failures

Report malformed configuration, unavailable assignments, and settings the harness cannot express. Consult owns external launch mechanics, follow-ups, and reported native fallback; fallback does not rewrite the saved assignment.

Distinguish requested settings from verified ones. A cheap smoke run verifies its own model and workflow, not another model's availability or output quality. Use the `skill_eval_smoke_candidate` assignment for runner checks. Run Claude Haiku checks outside plan mode, which can select a larger model.
