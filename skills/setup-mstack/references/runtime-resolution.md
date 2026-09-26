# Runtime model resolution

Resolve a role from the same installation as the calling skill:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --harness <harness> --role <role-name>
```

Assignments contain `model`, `effort`, and `fast`; [Delegate](../../delegate/SKILL.md) chooses execution.

## Active profile

Each harness has its own profile, where `<harness>` is `claude-code` or `codex`. The file selects `preset = "codex-preset"` or `preset = "claude-preset"` and overrides fields under `[roles.<role>]`. Its location is `MSTACK_CONFIG`, otherwise `$XDG_CONFIG_HOME/mstack/profiles/<harness>.toml`, otherwise `~/.config/mstack/profiles/<harness>.toml`.

Run Setup in this harness if it has no profile. Use `--preset` for inspection or a scoped run. Pass the harness you are running in; never infer it from environment variables, which children inherit from their parent.

Pass effective assignments and inline overrides to children. For a specific config file, pass its absolute path as `MSTACK_CONFIG` to external children. Caller-supplied inline assignments take precedence for the task without changing saved configuration.

## Capabilities

Preserve model settings; report controls the harness cannot express.

Use `skill_eval_smoke_candidate` for cheap execution checks; results do not establish another model's availability or quality. Run Haiku checks outside plan mode, which can select a larger model.
