---
name: why
description: "Use for 'why does X work this way', 'why was Y chosen', design rationale, regressions, postmortems, historical constraints, or data-backed thresholds. Investigates available evidence sources in parallel and returns a confidence-calibrated, cited account of motivation and tradeoffs. Use how for runtime behavior."
---

# Why

Investigate the motivation and intent behind code. Why was it built this way? What edge cases were considered? What product, business, or operational constraints shaped the design? What alternatives were rejected, and why?

This is the companion to the installed `how` skill. `how` explains what the code does and how it works. `why` explains the forces that led to its shape.

## Operating Posture

Work like a careful, cautious, precise investigator reconstructing a historical case from fragmentary records.

- **Evidence before narrative.** Collect the pieces before deciding what story they support.
- **Precision over polish.** Prefer an exact quote and citation over a smooth paraphrase.
- **Name the gaps.** Report cold trails, unavailable sources, failed tools, and unanswered questions.
- **Hedge on purpose.** Match language to confidence; do not upgrade inference into fact.
- **Surface contradictions and competing hypotheses.** Do not quietly select the tidiest account.
- **No shortcut by code-reading.** Code establishes mechanics and anchors; it rarely proves intent.
- **Read-only investigation.** Do not edit project files, mutate external systems, update tickets, commit, or push. Temporary orchestration artifacts must stay outside the repository.

Read [references/epistemics.md](references/epistemics.md) in full before running the investigation. The final synthesizer must follow it.

Before launching any role, read [MStack runtime model resolution](../setup-mstack/references/runtime-resolution.md) completely and resolve `why_investigator` and `why_synthesizer`.

## 1. Establish the Question and Code Anchor

Identify the target and the exact question. If the referent is vague, infer it from the conversation and state the interpretation briefly.

Before delegating, build a compact anchor:

- Relevant file paths and line ranges.
- Key symbols, constants, tests, and error strings.
- `git blame` for the target lines.
- Recent and introducing commits from `git log --follow` and `git log -S` or `-G` where useful.
- PR numbers and linked ticket IDs from commit messages.
- PR bodies and discussion through authenticated `gh` for substantive commits.
- Relevant `.agents/logbook/` records when that repository-local tree exists. Search implemented records first; use proposed and rejected records as evidence of alternatives, not shipped behavior. Cite the record and status, and verify present mechanics against current code, tests, and history.

This seed context prevents every investigator from rediscovering the same basics. Do not treat the code itself as evidence of intent.

Repository Logbook records are always in scope when present because they travel with the code. They do not require a separate investigator category: include relevant records in the anchor sent to investigators and the synthesizer. Treat a missing Logbook tree as ordinary absence, not a capability failure.

## 2. Build the Runtime Coverage Map

Discover actual callable capabilities in the current run. An installed skill or named playbook is not proof that its connector is available or authenticated. Map available tools to these evidence categories:

1. Source control history: local git and, when callable, GitHub through `gh`.
2. Issue or ticket tracking: Linear, Jira, GitHub Issues, Plane, Shortcut, or equivalent.
3. Long-form documents: Notion, Confluence, Google Docs, Coda, repository ADRs, or equivalent.
4. Real-time team chat: Slack, Discord, Teams, Mattermost, or equivalent.
5. Infrastructure observability: Datadog, New Relic, Honeycomb, Grafana, Splunk, or equivalent.
6. Error or exception tracking: Sentry, Rollbar, Bugsnag, Airbrake, or equivalent.
7. Product analytics warehouse: Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift, or equivalent.

Availability alone does not put a source in scope. Follow the user's or repository's declared project source profile and do not search unrelated personal connectors merely because they are callable. The current profile for this user's engineering workflow is GitHub plus Linear. The other playbooks remain supported but inactive until the user says the project uses that source or the active task explicitly places it in scope. Treat an inactive source as `Not searched; not in the current project source profile`, not as unavailable.

Local git is the minimum source-control path. Treat GitHub PR data as a separate capability of that category when `gh` is unavailable. For every other category, spawn an investigator only when a matching source is callable. Preserve unavailable categories in the coverage map.

Use these distinct outcomes:

- **Searched; evidence found.** Cite the evidence.
- **Searched; no relevant result.** A first-class null result.
- **Not searched; capability unavailable or failed.** Report the tool and impact as a gap.
- **Not searched; provably irrelevant.** Give a narrow, explicit justification. Mere expectation of no result is insufficient.

Read [references/source-playbook.md](references/source-playbook.md) to select the source-specific playbook. Keep future playbooks available even when their integrations are not currently configured.

## 3. Run Parallel Investigators

Spawn one configured investigator per available evidence category. Launch independent investigators together so they run concurrently.

For every investigator:

- Use the resolved `why_investigator` runner, model, effort, and Fast setting exactly.
- Start without forked conversation history; provide a self-contained assignment.
- Give it [references/investigator-prompt.md](references/investigator-prompt.md), exactly one matching source playbook, the code anchor, and the user's original question.
- Give it [references/sources/incident-postmortem.md](references/sources/incident-postmortem.md) as an additional cross-cutting angle when the target is defensive code such as retries, null guards, timeouts, rate limits, feature flags, egress guards, or OOM handling.
- Explicitly attach or identify any required skill or connector, such as the local Linear skill, when the harness supports structured skill or app mentions.
- Instruct it to investigate read-only, collect evidence rather than answer the question, and report capability or tool failures in its result.
- Let it continue until its assigned source is reasonably exhausted and it can return a complete report. Do not impose an elapsed-time deadline.

Each investigator owns one category. Do not collapse multiple source categories into a single agent. If a connector is unavailable inside a configured subagent but is callable by the parent, the parent may perform the read-only query and send the returned evidence to that same investigator for analysis. Record this as parent-mediated access in the coverage map. Never silently claim that the investigator queried a tool it could not access.

Wait for all investigators needed by the synthesis, retaining null results and tool failures. A `running` status or long elapsed time alone is not evidence of a stall. Do not interrupt an investigator that is making visible progress. The native orchestration API may expose only coarse status; in that case, do not invent progress judgments or send routine pings. Intervene only when surfaced activity shows a concrete loop, repeated failed operation, irrelevant expansion, or another clearly unproductive pattern. Start with one non-interrupting corrective message; interrupt only if the behavior continues. If an investigator becomes genuinely unusable, record the capability issue and use parent-mediated read-only evidence when practical rather than blocking synthesis. Close completed native agents after their reports have been captured.

## 4. Synthesize Evidence

Launch `why_synthesizer` through its resolved runner under the same read-only boundary. If the assignment uses an external runner, read and use the matching launcher skill, [Claude Code](../claude-code/SKILL.md) or [Codex](../codex/SKILL.md), and follow its process boundary.

Create a self-contained synthesizer prompt from [references/synthesizer-prompt.md](references/synthesizer-prompt.md). Include:

1. The original question and code anchor.
2. Every investigator report, including null results and capability failures.
3. Every skipped category and its reason.
4. The active project source profile, so the synthesizer does not widen the investigation to unrelated connectors.
5. The exact path to [references/epistemics.md](references/epistemics.md), which the synthesizer must read in full.
6. Permission to spot-verify citations with its own read-only tools, Linear connector, `git`, and `gh` when available.

Invoke the assignment with its resolved model, effort, and Fast setting. A synthesizer with broad tools still operates under the reusable non-mutation boundary. Its `Capability and Tool Issues` section is part of the result and must be preserved.

Do not configure or silently use another synthesis model. If the configured synthesizer fails, return the collected investigator evidence plus the concrete launcher failure and label the synthesis incomplete.

## 5. Apply Parent Lead Judgment and Present

The parent agent retains lead judgment. Check that the synthesizer:

- Separates Direct, Supported, Inferred, Speculative, and Unknown claims correctly.
- Cites every Direct and Supported claim.
- Does not cite code shape as proof of intent.
- Surfaces contradictions, null results, unavailable sources, and capability issues.
- Preserves a complete source coverage map.

Spot-check material citations when practical. Correct demonstrable citation or orchestration errors, but do not rewrite hedged confidence language merely to sound more decisive.

Use the final structure defined in [references/synthesizer-prompt.md](references/synthesizer-prompt.md): The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses when needed, What We Don't Know, Sources Consulted, Confidence Summary, and Capability and Tool Issues when any occurred.

If the question is a precursor to changing the code, add a concise Preserve / Change / Avoid / Risk constraint set grounded in the lineage evidence.

## Failure Modes

- Confident storytelling from thin evidence.
- Skipping an available category because it probably has nothing.
- Treating a failed or unavailable tool as a successful null search.
- Collapsing all investigators into one agent.
- Letting investigators synthesize the final answer instead of collecting evidence.
- Passing only positive findings to the synthesizer and dropping null results or contradictions.
- Silently replacing the configured synthesizer when its invocation fails.
- Hiding capability issues that would let the user repair the workflow.
