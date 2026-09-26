---
name: delegate
description: "Delegate scoped tasks natively or through an external harness, with resumable follow-ups."
---

# Delegate

Use this skill for every agent launch and follow-up. The caller owns scope and final judgment.

## Prepare

Use the caller's model assignment. Otherwise resolve the role before launching, using `delegate_default` when no role is named:

```bash
python3 <setup-mstack-directory>/scripts/models.py resolve --harness <claude-code|codex> --role <role>
```

If resolution fails, stop and run [Setup](../setup-mstack/SKILL.md) before launching. Never launch with harness defaults or a preset the user did not choose. See [model configuration](../setup-mstack/references/runtime-resolution.md) for locations and passing assignments to children.

Give the child the task, collected findings, source and skill paths, working directory, edit scope, and desired output. Refer to MStack skills by absolute path in this installation, not by name; a child given only a name can find and follow its harness's installed copy, which may be another version. Include relevant active assignments and inline overrides; children use these rather than their own harness profile.

`allow_writes` and `allow_subagents` default to false. The caller enables each independently; children cannot expand their own permissions.

Before choosing native or external execution, include these prompt boundaries:

- With writes disabled: “Investigate read-only. Do not edit project files or mutate external systems.”
- With writes enabled: state the authorized files or directory and requested changes.
- With subagents disabled: **“Work directly. Do not launch other agents, even when a skill offers delegation.”**
- With subagents enabled: permit Delegate; children still default to `allow_subagents=false`.

These are prompt instructions, not tool restrictions.

## Launch

Use native tools when they support the assigned model and task, unless an external process was requested. Claude Code's Agent tool selects `fable`, `opus`, `sonnet`, or `haiku` but not effort; launch externally when the assigned effort must apply. Otherwise use [Claude](references/claude.md) for Claude models or [Codex](references/codex.md) for GPT models. Report unsupported settings or unavailable execution; never silently substitute models.

For external launches, pass the task on stdin or use `--prompt-file`:

```bash
python3 <delegate-directory>/scripts/run_delegate.py \
  --provider <claude|codex> --cwd <checkout> \
  --model <model> --effort <effort>
```

Add `--fast`, `--allow-writes`, or `--allow-subagents` when assigned; each defaults to false on every invocation.

External flags also configure provider permissions: checkout edits for Claude writers, and network/session access for Codex processes allowed to delegate. See the provider references for scope.

## Follow up

Monitor completion and check results, model evidence, and actual edits. External runs write `summary.json`; a successful process may still report blocked work.

Keep the conversation ID and settings in context. Reapply them on every native send or external `--resume <id>` unless the caller changes them. Reuse related conversations; start fresh for independent assessments. If an ID is lost or unusable, restart with relevant context and report it.

Stop an active process before redirecting it. Inspect partial edits before replacing a writer. Report failures and access gaps without repeatedly retrying them.

## Cleanup

The launcher stores prompts, reports, and logs in a temporary directory. Delete it and any temporary input file after checking results. Use `--output-dir` to retain evidence in an unused location outside the checkout.

Provider conversations remain resumable after cleanup.
