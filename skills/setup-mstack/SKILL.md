---
name: setup-mstack
description: Inspect or change MStack's model assignments, efforts, and Fast settings.
---

# Setup MStack

The active profile combines a preset and user overrides; installed skills need no edits. Use judgment on capability checks and clarification.

## Inspect

Run the bundled resolver:

```bash
python3 <setup-mstack-directory>/scripts/models.py presets
python3 <setup-mstack-directory>/scripts/models.py resolve
```

Offer `codex-preset` and `claude-preset`, with optional role customization. Complete setup if no active profile is selected. See [Runtime resolution](references/runtime-resolution.md) for configuration locations and passing assignments to children.

Show the preset, effective assignments, and overrides. Check available models and relevant CLI authentication with `codex login status` or `claude auth status`. Report unknown model access without changing assignments; login alone does not verify it.

Use cheap smoke roles for launch checks and report what they verified; do not launch expensive models merely to infer access.

## Configure

Write only when setup or changes were requested. Show the proposed profile; resolve missing choices without reconfirming explicit ones.

Preview the complete replacement configuration:

```bash
python3 <setup-mstack-directory>/scripts/models.py configure \
  --preset <preset> \
  --set delegate_default.effort=high \
  --dry-run
```

`configure` replaces the user file with the selected preset and overrides. Preserve wanted overrides with one `--set ROLE.FIELD=VALUE` per field. Remove `--dry-run` to write.

Assignments contain `model`, `effort`, and `fast`. Existing roles accept partial overrides; new roles need all three. [Delegate](../delegate/SKILL.md) chooses execution and reports unsupported settings. Remove legacy runner fields and rename `consultant_default` to `delegate_default`.

## Verify

Run `models.py resolve` again. Report the configuration path, resulting assignments, and anything still unverified. Changes apply the next time a workflow resolves its roles.
