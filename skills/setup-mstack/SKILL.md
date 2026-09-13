---
name: setup-mstack
description: Inspect or change MStack's model assignments, efforts, runners, and Fast settings for Codex or Claude Code.
---

# Setup MStack

The active profile is a preset plus user overrides. Packaged presets provide starting assignments; installed skills need no edits. Use judgment on capability checks and clarification.

## Inspect

Run the bundled resolver:

```bash
python3 <setup-mstack-directory>/scripts/models.py presets
python3 <setup-mstack-directory>/scripts/models.py resolve
```

Offer `codex-preset` and `claude-preset`, recommending the one matching the host. Users can accept a preset or customize any role. Without a user configuration, the host preset supplies the active profile. Read [Runtime resolution](references/runtime-resolution.md) for configuration locations, host overrides, and runner selection.

Show the selected preset, effective assignments, and any local overrides. Check model availability through exposed metadata and external CLI authentication with `codex login status` or `claude auth status`, as relevant. Report unknown availability or incompatible runners; keep configured choices intact. Login alone does not establish model access.

If a launch check is needed, use the configured cheap smoke roles. Report what was actually verified; do not launch expensive models merely to infer access.

## Configure

Write only when setup or configuration changes were requested. Show the proposed active profile; resolve missing choices without reconfirming explicit ones.

Preview the complete replacement configuration:

```bash
python3 <setup-mstack-directory>/scripts/models.py configure \
  --preset <preset> \
  --set consultant_default.effort=high \
  --dry-run
```

`configure` saves the selected preset and role overrides, replacing the whole user file. Include every existing override that should survive, using one `--set ROLE.FIELD=VALUE` per field. Remove `--dry-run` to write.

Supported fields are `runner`, `model`, `effort`, and `fast`; the resolver validates them. Fast applies only to Codex runners, and `implement_worker` requires a native runner.

## Verify

Run `models.py resolve` again. Report the configuration path, resulting assignments, and anything still unverified. Changes apply the next time a workflow resolves its roles.
