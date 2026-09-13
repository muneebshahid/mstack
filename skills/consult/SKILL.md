---
name: consult
description: "Ask an independent agent for analysis, critique, or judgment, with resumable follow-ups. Read-only; use for consultation requested by the user or another workflow."
---

# Consult

Get another agent's judgment. The parent owns the question, checks the evidence, and decides what to accept. Consultants stay read-only.

## Choose and brief

Resolve the caller's role through [model configuration](../setup-mstack/references/runtime-resolution.md), or `consultant_default` for a direct request. Use the assigned native agent or external CLI. For external calls, read the reference for the consultant being launched: [Claude](references/claude.md) or [Codex](references/codex.md), regardless of the parent harness.

Give the consultant the question, relevant paths and findings, constraints, and desired output. Include explicit skill paths when needed; an external process does not inherit the parent's loaded context. Start independent assessments in fresh conversations. Reuse a conversation for related follow-ups.

## Run and follow up

Launch an external consultation in a managed command session:

```bash
python3 <consult-directory>/scripts/run_consult.py \
  --provider <claude|codex> \
  --cwd <checkout> --prompt-file <prompt-file> \
  --model <model> --effort <effort>
```

Monitor the returned process handle and activity events. After it exits, read `summary.json` and its report. Check the actual result, served model, and reported capability gaps; process completion alone is insufficient.

Keep the returned conversation ID in context. For a follow-up, write the new prompt and add `--resume <conversation-id>` with the same provider and checkout. If the ID is unavailable or no longer works, start a new conversation with a summary and mention the restart. To redirect active work, interrupt the managed process if needed, then resume after it stops. Native consultations use the host's send, wait, and resume tools.

## Files and cleanup

The launcher writes reports and logs to a temporary directory. After reading them, the parent removes that directory and its temporary input prompt. Use `--output-dir` for evidence worth retaining, such as evaluations; choose an unused location outside the checkout.

Resumption uses the harness's conversation, so temporary files need not survive follow-ups. No extra checkout is needed for read-only consultation.

## Failures and fallback

If the external harness is unavailable, use an available native subagent and report the substitution. Keep it read-only and retain its identity for follow-ups. If native delegation is also unavailable, report the gap and continue directly when useful.

Do not call a native substitute an independent cross-provider review or claim an explicitly requested model ran when it did not. Preserve authentication, quota, permission, and tool failures; do not repeatedly retry them.
