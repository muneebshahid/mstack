---
name: claude-code
description: "Use when a workflow explicitly requires an external Claude Code model as an independent consultant, critic, judge, or bounded analyst. Runs a caller-selected Claude model and effort with configured Claude tools, then returns verified model provenance and report artifacts to the parent Codex agent. Do not use for ordinary Codex tasks or implementation work."
---

# Claude Code Consultant

Run a caller-selected Claude Code model as an external, independent consultant. This skill owns the Claude Code process boundary. The calling workflow owns model selection, effort, task prompting, orchestration, interpretation, and final judgment.

Use this boundary only when the user or an active workflow explicitly calls for Claude. It consumes Claude usage separately from Codex. Production workflows currently select Claude Fable 5.1 (`claude-fable-5-1`) at their declared effort; evaluation-only execution checks may deliberately select a cheaper model such as `haiku` at `low` effort.

## Prepare the Prompt

Give Claude a self-contained prompt. Include:

- The exact question or assigned role.
- The relevant code, findings, paths, or other evidence.
- Applicable repository instructions and constraints.
- The required output structure.
- Any additional role-specific limits or source priorities.

The launcher gives Claude its normal tools and configuration, including available plugins and MCP servers, and exposes the Codex skills directory with `--add-dir`. When a Codex skill is relevant, give Claude its explicit path and tell it to read that skill before proceeding; Claude does not automatically treat Codex skills as native Claude skills.

The launcher prepends a strong consultant boundary to every prompt: Claude may investigate freely, but must not edit files, run mutating commands, change external systems, create or update tickets, commit, push, or delegate implementation. This is a role instruction, not a sandbox. Claude has write-capable tools, including unrestricted shell access, so the parent must review its report and retain final judgment.

The boundary also requires Claude to report any missing or failed tool, MCP server, plugin, skill, file, permission, authentication, or other capability. When one occurs, its final report must include a `Capability and Tool Issues` section describing the attempted operation, observed problem, affected evidence or work, impact on confidence or completeness, and a useful next diagnostic or setup step. It must redact secrets, distinguish an unavailable source from a successful search with no results, continue with available evidence when possible, and avoid repeated retries. It omits the section when no issue occurred.

Write the prompt to a temporary file outside the repository. Create a separate temporary output directory.

## Run Claude

Start the launcher in a managed terminal session and let it continue in the background while independent work proceeds:

```bash
python3 <skill-directory>/scripts/run_claude.py \
  --cwd <repository-root> \
  --prompt-file <temporary-prompt-file> \
  --output-dir <temporary-output-directory> \
  --model <model-alias-or-exact-id> \
  --effort <low|medium|high|xhigh|max>
```

Use the model and effort declared by the calling workflow. The launcher's compatibility default remains `claude-fable-5-1` at `xhigh`, but callers should pass both settings explicitly when correctness or cost depends on them. Do not configure a fallback model: the result must come from the requested model or fail clearly.

The launcher accepts exact model identifiers and the Claude Code aliases `fable`, `haiku`, `opus`, and `sonnet`. It verifies that an alias resolves to the matching served model family and records both requested and served model values in `summary.json`.

Monitor the managed command session rather than assuming completion. The launcher emits start, sanitized `claude.activity`, heartbeat, and completion events. Activity events expose the current tool-level action, elapsed time, and completed tool-call count without exposing commands, tool inputs, partial reasoning, or report contents. Heartbeats include the most recent activity and total tool-call count. Treat these as operational milestones, not a reliable percentage-complete estimate.

Do not open a Codex integrated-terminal tab for the managed command session. Those tabs are independent project shells and do not display the launcher's output. Poll the managed session and relay meaningful activity changes to the user as concise commentary, with a heartbeat at least once per minute while the run remains active. Do not replay raw JSON when a short description such as “Claude is reading `src/auth.py`” is sufficient.

The launcher is open-ended by default. Do not stop Claude because a fixed elapsed-time budget has passed. Continue while surfaced events show useful progress. If activity reveals a concrete loop, repeated failed operation, irrelevant expansion, or another clearly unproductive pattern, first try one corrective instruction when the process interface supports it; otherwise interrupt only when the behavior is demonstrably unproductive. A caller may pass a positive `--timeout-seconds` only when that workflow has an explicit reason for a hard safety bound.

## Read the Result

After the launcher exits successfully, read:

- `claude.result.md`: the report to return to the caller.
- `claude.progress.log`: the persistent, sanitized activity history suitable for a clickable file link in the final response.
- `summary.json`: requested model, verified served model, effort, state, exit code, failure reason, bounded error excerpt, and artifact paths.

Use `claude.events.jsonl` and `claude.stderr.log` only for diagnosis.

Preserve and surface any `Capability and Tool Issues` section to the calling workflow; do not silently discard it while summarizing Claude's report. Do not repeatedly retry authentication, quota, model-availability, tool, or configuration failures. Report the concrete blocker to the calling workflow. The caller decides whether a degraded workflow can continue without Claude.
