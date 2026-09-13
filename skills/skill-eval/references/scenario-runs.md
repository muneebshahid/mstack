# Running candidates

Keep the evaluator in the parent conversation. Choose a fresh candidate environment that supports the workflow being tested:

- A native subagent is sufficient when the candidate needs no further delegation.
- If the candidate must delegate, check the tools available at the candidate's depth and its remaining nesting depth. Use a native subagent when it can still spawn the required workers.
- Otherwise, the evaluator launches a fresh top-level harness process in the disposable workspace: `codex exec --json` or `claude -p --output-format stream-json --verbose`, with the selected model and effort. The candidate uses that process's native agent tools.

Nesting limits vary by harness, version, and configuration. Do not assume identical limits or silently raise them. An external process tests its own agent tree; it cannot establish integration with the calling desktop task. Test that relationship through the actual host when it matters.

Give candidates the skill through the harness's discovery mechanism when testing automatic selection. Attaching a skill explicitly tests execution only. Check the loaded path or content against the intended version, especially when an installed copy remains visible.

Use read-only access for analysis and bounded write access to disposable files for writing workflows. Check access to temporary prompts, outputs, and evidence before unattended runs. Do not use Consult's read-only launcher for candidates that must edit files.

Retain the process result and material tool events. When a native operation is being tested, its returned ID and follow-up operations are the evidence. Avoid ephemeral sessions when testing resumption across process restarts.
