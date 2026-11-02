---
name: setup-mstack
description: Inspect or change MStack's model assignments, efforts, and Fast settings.
---

# Setup MStack

Each harness has its own profile: a preset plus user overrides. Setup configures only the harness it runs in; installed skills need no edits.

## Inspect

Run the bundled resolver:

```bash
python3 <setup-mstack-directory>/scripts/models.py presets
python3 <setup-mstack-directory>/scripts/models.py resolve --harness <harness>
```

Pass `--harness claude-code` in Claude Code and `--harness codex` in Codex.

Offer both presets, suggesting the one matching the harness, with optional role overrides; complete setup if this harness has no profile. See [Runtime resolution](references/runtime-resolution.md) for configuration locations and passing assignments to children.

Show the preset, effective assignments, and overrides. Check available models and relevant CLI authentication with `codex login status` or `claude auth status`. Report unknown model access without changing assignments; login alone does not verify it.

Use a cheap model for launch checks and report what they verified; do not launch expensive models merely to infer access. Run Haiku checks outside plan mode, which can select a larger model.

## Configure

Write only when setup or changes were requested. Show the proposed profile.

Preview the complete replacement configuration:

```bash
python3 <setup-mstack-directory>/scripts/models.py configure \
  --harness <harness> \
  --preset <preset> \
  --set delegate_default.effort=high \
  --dry-run
```

`configure` replaces the user file with the selected preset and overrides. Preserve wanted overrides with one `--set ROLE.FIELD=VALUE` per field. Remove `--dry-run` to write.

The shared `~/.config/mstack/models.toml` is no longer read; offer its preset and overrides when configuring each harness, and remove it once the user confirms.

## Verify

Run `models.py resolve` again. Report the configuration path, resulting assignments, and anything still unverified.
