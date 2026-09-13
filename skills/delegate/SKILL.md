---
name: delegate
description: "Delegate scoped tasks natively or through an external harness, with resumable follow-ups."
---

# Delegate

Use this skill for every agent launch and follow-up. The caller owns scope and final judgment.

## Prepare

Use the caller's model assignment or resolve its role through [model configuration](../setup-mstack/references/runtime-resolution.md). Default to `delegate_default` when neither is supplied. Run Setup if role resolution lacks an active profile.

Give the child the task, collected findings, source and skill paths, working directory, edit scope, and desired output. Include relevant active assignments and inline overrides; keep the profile across harnesses.

`allow_writes` and `allow_subagents` default to false. The caller enables each independently; children cannot expand their own permissions.

Before choosing native or external execution, include these prompt boundaries:

- With writes disabled: “Investigate read-only. Do not edit project files or mutate external systems.”
- With writes enabled: state the authorized files or directory and requested changes.
- With subagents disabled: **“Work directly. Do not launch other agents, even when a skill offers delegation.”**
- With subagents enabled: permit Delegate; children still default to `allow_subagents=false`.

These are prompt instructions, not tool restrictions.

## Launch

Use native tools when they support the assigned model and task, unless an external process was requested. Otherwise use [Claude](references/claude.md) for Claude models or [Codex](references/codex.md) for GPT models. Report unsupported settings or unavailable execution; never silently substitute models.

For external launches, pass the task on stdin or use `--prompt-file`:

```bash
python3 <delegate-directory>/scripts/run_delegate.py \
  --provider <claude|codex> --cwd <checkout> \
  --model <model> --effort <effort>
```

Add `--fast`, `--allow-writes`, or `--allow-subagents` when assigned; each defaults to false on every invocation.

## Follow up

Monitor completion and check results, model evidence, and actual edits. External runs write `summary.json`; a successful process may still report blocked work.

Keep the conversation ID and settings in context. Reapply them on every native send or external `--resume <id>` unless the caller changes them. Reuse related conversations; start fresh for independent assessments. If an ID is lost or unusable, restart with relevant context and report it.

Stop an active process before redirecting it. Inspect partial edits before replacing a writer. Report failures and access gaps without repeatedly retrying them.

## Cleanup

The launcher stores prompts, reports, and logs in a temporary directory. Delete it and any temporary input file after checking results. Use `--output-dir` to retain evidence in an unused location outside the checkout.

Provider conversations remain resumable after cleanup.
