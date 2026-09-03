# Scenario runs

The experiment must resemble the skill's real operating environment closely enough that activation, linked resources, authority, and side effects remain meaningful.

## Complete snapshots

Stage each arm as a complete skill directory. Include the target's supporting resources and the exact dependency closure it would normally read. Baseline and proposed environments must be identical except for the target skill revision.

Never evaluate a proposed change by appending its diff to the candidate prompt. Never give the candidate the current skill plus an overlay of replacement instructions. Those shapes bypass normal instruction order, references, discovery, and contradictions.

A complete skill or prompt template may be injected for a quick wording probe, but label that result a micro-test. Promotion evidence comes from the complete staged skill.

## Isolated workspaces

Create a fresh operating-system temporary root for the run. Give each arm and scenario a neutral project-shaped directory. Avoid these words anywhere candidates can see them:

`eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, `baseline`, `treatment`, and `arena`.

Stage the skill tree beneath `.agents/skills/` in each disposable workspace and make the fixture a Git repository before launch. Start every candidate without forked conversation context and give it only the organic user request and normal skill catalog. Use a fresh host-native agent for a leaf skill. When the target skill must spawn native Codex agents, use a fresh top-level `codex exec --ephemeral --json` candidate so its own native agent tools remain available. If project-local discovery cannot be exercised through the selected boundary, test execution by attaching the complete staged skill and mark automatic activation **Unexercised**.

After the run, identify the skill path or content hash actually read. If an identically named global copy remained visible, record it. A byte-identical duplicate may still demonstrate automatic routing for a current-skill evaluation, but it does not prove project-local selection. A revision arm is valid only when the trace establishes that the exact staged snapshot was read.

When project-local discovery is unavailable, attach the complete skill directory through the native structured skill input. This exercises the skill's workflow but force-loads it, so mark activation **Unexercised**.

## Native-agent workflows

An evaluation of native worker identity, persistence, or resume behavior requires a candidate boundary that exposes native multi-agent tools. Before concluding that the capability is unavailable, search the complete callable tool catalog, including deferred tools. Use a fresh host-native candidate for a leaf skill. Use a top-level `codex exec --ephemeral --json` candidate only when the skill under evaluation must itself spawn agents; launching the evaluator's candidate through another native subagent would remove the delegation tool at the required level.

The evaluator launches and monitors `codex exec`; the candidate skill must never shell out to Codex. Capture the JSON event stream and stderr separately in parent-side artifacts outside the candidate-visible workspace. Do not assume `--ignore-user-config` removes every global skill, plugin, or connector: record visible duplicate skills and unrelated capability warnings, then verify the exact staged path or content hash actually read.

The trace must contain the native spawn call and a non-empty returned agent identifier before the candidate may claim that an agent is running. Every wait, input, resume, and close operation must use that exact identifier. For a `codex exec` candidate, also require its top-level thread identifier and successful process exit. If native spawn fails, reports `no thread with id`, or returns no worker identifier, stop that candidate before project writes. Record the capability failure and mark every worker-authorship, idle-state, continuity, and resume criterion **Unexercised** or failed according to the registered rubric. Do not wait on an empty identifier set, accept off-trace mutations as worker output, or let candidate prose substitute for native identity evidence.

Agent identities created inside `codex exec` belong to that candidate session. They prove candidate-local orchestration, not addressability, persistence, messaging, or resumption from the calling desktop task. Use the host-native path when those app-level relationships are the behavior under evaluation.

For an execution smoke test, stage model substitutions in the complete temporary skill and dependency copies rather than appending override prose to the candidate prompt. Use `gpt-5.6-luna` at `low` effort with `priority` service tier for native Codex roles and Claude `haiku` at `low` effort for external Claude roles. Keep both arms identical. These runs establish workflow mechanics only; they do not establish production-model quality. Quality evaluations and model/provenance checks use the skill's actual configuration.

Copy only the project fixture and repository instructions the scenario genuinely needs. Do not point a write-capable scenario at the live repository. Use a read-only sandbox when the skill should inspect only; use a disposable workspace-write sandbox when its real contract includes file changes.

Use fake or ephemeral boundaries for external mutations. A skill evaluation does not authorize changing real tickets, pull requests, deployments, accounts, or production systems.

## Candidate prompt

The prompt must look like something a user would naturally ask:

- State the task and desired outcome, not what is being measured.
- Do not mention another arm or the proposed change.
- Do not reveal the rubric or expected behavior.
- Do not ask which skills, principles, or files were used.
- Do not ask for self-analysis that would cue compliance.

Keep model, reasoning effort, service tier, tools, fixture, and repository instructions fixed across comparison arms. When model behavior itself is the subject, create matched pairs and state the model dimension in the parent-only experiment record.

## Evidence

Capture what the harness exposes. Prefer a machine-readable event stream written to a parent-side location outside the candidate-visible workspace. If events are exposed only live, preserve the material sequence in the report and say that no durable raw trace exists.

Record:

- Final output and exit state.
- Skill and reference reads.
- Tool calls and capability failures.
- Agents, models, efforts, and service tiers invoked.
- Files created, changed, or deleted.
- External mutation attempts.
- Verification commands and resulting evidence.
- Usage and elapsed time when available.

Trust artifacts and traces over self-report. A final message claiming that a reference was read is not proof that it was read or applied.

Run once per scenario by default. Repeat matched arms only to resolve inconsistent or decision-sensitive results. Preserve failed and incomplete runs; do not silently rerun until the preferred arm wins.
