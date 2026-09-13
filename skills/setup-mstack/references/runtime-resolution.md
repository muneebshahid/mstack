# Runtime model resolution

Resolve a role from the same installation as the calling skill:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --role <role-name>
```

Assignments contain `model`, `effort`, and `fast`; [Delegate](../../delegate/SKILL.md) chooses execution. Presets do not depend on the harness.

## Active profile

The user file selects `preset = "codex-preset"` or `preset = "claude-preset"` and overrides fields under `[roles.<role>]`. Its location is `MSTACK_CONFIG`, otherwise `$XDG_CONFIG_HOME/mstack/models.toml`, otherwise `~/.config/mstack/models.toml`.

Run Setup if no profile is selected. Use `--preset` for inspection or a scoped run. Never switch presets based on the harness or inherited environment.

Pass effective assignments and inline overrides to children. For a specific config file, pass its absolute path as `MSTACK_CONFIG` to external children. Caller-supplied inline assignments take precedence for the task without changing saved configuration.

## Capabilities

Preserve model settings; report controls the harness cannot express.

Use `skill_eval_smoke_candidate` for cheap execution checks; results do not establish another model's availability or quality. Run Haiku checks outside plan mode, which can select a larger model.
