---
name: codex
description: "Use when a workflow explicitly requires an external Codex model as an independent consultant, critic, judge, or bounded analyst. Runs a caller-selected GPT model, effort, and service tier in Codex's read-only sandbox, then returns verified model provenance and report artifacts to the parent agent. Do not use for ordinary tasks or implementation work."
---

# Codex Consultant

Run a caller-selected Codex model as an external, independent consultant. This skill owns the Codex process boundary. The calling workflow owns model selection, effort, task prompting, orchestration, interpretation, and final judgment.

Use this boundary only when the user or an active workflow explicitly calls for an external Codex process. It consumes Codex usage separately from the parent harness. Calling workflows resolve their named MStack role. A direct invocation without a caller-owned assignment resolves `consultant_default` through [MStack runtime model resolution](../setup-mstack/references/runtime-resolution.md). Execution smoke tests resolve their dedicated smoke roles rather than borrowing production assignments.

This skill is the reciprocal of [Claude Code Consultant](../claude-code/SKILL.md): Codex calls Claude through that skill, and Claude Code calls Codex through this one.

## Prepare the Prompt

Give Codex a self-contained prompt. Include:

- The exact question or assigned role.
- The relevant code, findings, paths, or other evidence.
- Applicable repository instructions and constraints.
- The required output structure.
- Any additional role-specific limits or source priorities.

The launcher gives Codex its normal user configuration, including installed plugins, skills, and MCP servers. Codex does not see the parent's loaded skills or conversation. When a skill is relevant, give Codex its explicit absolute path and tell it to read that skill before proceeding.

The launcher prepends a consultant boundary to every prompt and runs Codex in its `read-only` sandbox, so file writes and mutating commands inside the workspace are blocked by Codex itself rather than by instruction alone. Network access and MCP servers remain available, so the boundary still tells Codex not to change external systems, create or update tickets, or delegate implementation.

The boundary also requires Codex to report any missing or failed tool, MCP server, plugin, skill, file, permission, authentication, or other capability in a `Capability and Tool Issues` section of its final report. It must redact secrets, distinguish an unavailable source from a successful search with no results, continue with available evidence when possible, and avoid repeated retries. It omits the section when no issue occurred.

Write the prompt to a temporary file outside the repository. Create a separate temporary output directory.

## Run Codex

Start the launcher in a background shell and let it continue while independent work proceeds:

```bash
python3 <skill-directory>/scripts/run_codex.py \
  --cwd <repository-root> \
  --prompt-file <temporary-prompt-file> \
  --output-dir <temporary-output-directory> \
  --model <exact-model-slug> \
  --effort <low|medium|high|xhigh|max> \
  [--fast]
```

Pass the resolved model and effort explicitly, and pass `--fast` only when the resolved assignment has `fast = true`. The launcher has no model or effort default. Do not configure a fallback model: the result must come from the requested model or fail clearly.

The launcher accepts exact Codex model slugs such as `gpt-5.6-sol` or `gpt-5.6-luna`. Its executable is `CODEX_BIN` when set, otherwise `codex`. It reads the Codex home from `CODEX_HOME` when set, otherwise `~/.codex`, because served-model provenance comes from the session rollout Codex writes there.

Monitor the background process rather than assuming completion. The launcher emits start, sanitized `codex.activity`, heartbeat, and completion events on stdout. Activity events expose the current item type, elapsed time, and completed item count without exposing commands, tool inputs, reasoning, or report contents. Heartbeats include the most recent activity and total item count. Treat these as operational milestones, not a percentage-complete estimate.

Poll the process and relay meaningful activity changes to the user as concise commentary, with a heartbeat at least once per minute while the run remains active. Do not replay raw JSON when a short description such as "Codex is running a shell command" is sufficient.

The launcher is open-ended by default. Do not stop Codex because a fixed elapsed-time budget has passed. Continue while surfaced events show useful progress. Interrupt only when activity reveals a concrete loop, repeated failed operation, or another clearly unproductive pattern. A caller may pass a positive `--timeout-seconds` only when that workflow has an explicit reason for a hard safety bound.

## Read the Result

After the launcher exits successfully, read:

- `codex.result.md`: the report to return to the caller.
- `codex.progress.log`: the persistent, sanitized activity history suitable for a clickable file link in the final response.
- `summary.json`: requested model, verified served model, requested and served effort, requested Fast tier, thread identifier, state, exit code, failure reason, bounded error excerpt, and artifact paths.

Use `codex.events.jsonl`, `codex.rollout.jsonl`, and `codex.stderr.log` only for diagnosis.

The launcher verifies the served model and effort against the session rollout. Codex does not report the served service tier, so `served_service_tier` is always `null`; report a Fast request as requested but unverified rather than claiming Fast service ran.

Preserve and surface any `Capability and Tool Issues` section to the calling workflow; do not silently discard it while summarizing Codex's report. Do not repeatedly retry authentication, quota, model-availability, tool, or configuration failures. Report the concrete blocker to the calling workflow. The caller decides whether a degraded workflow can continue without Codex.
