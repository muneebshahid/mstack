---
name: how
description: "Use for 'how does X work', code walkthroughs before changing something, subsystem architecture and runtime flow, or placement, ownership, and layering questions such as 'where should this live' and 'is this the right layer'. Can critique architecture after explaining it. Use why for historical motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce clear architectural explanations at the level of a senior engineer onboarding onto a subsystem: enough to build a working mental model, not annotated source code.

Two modes:

1. **Explain** (default). Explore the codebase and produce a clear explanation.
2. **Critique.** Explain first, then ask independent models to identify architectural issues and apply parent lead judgment.

How explains current purpose, structure, runtime flow, ownership, and placement. Do not infer historical motivation from code. Use `why` when the question requires design lineage, rejected alternatives, incidents, or business constraints.

Before launching any role, read [MStack runtime model resolution](../setup-mstack/references/runtime-resolution.md) completely and resolve only the roles required by the selected mode.

## Operating Boundary

- Inspect read-only. Do not edit project files, mutate external systems, commit, or push.
- Keep temporary orchestration artifacts outside the repository.
- Agents have no elapsed-time deadline. A long-running or merely `running` agent is not stalled.
- Do not interrupt visible progress. When the orchestration API exposes only coarse status, do not invent progress judgments or send routine pings.
- Intervene only when surfaced activity shows a concrete loop, repeated failed operation, irrelevant expansion, or another clearly unproductive pattern. Start with one non-interrupting correction; interrupt only if the behavior continues.
- Preserve agent gaps and capability failures. Never silently convert an unavailable path into a successful investigation.
- Close completed native agents after capturing their reports.

## Explain Mode

### 1. Understand the Question and Assess Complexity

Parse what the user is asking about:

- "How does the rate limiter work?" — a subsystem.
- "How do we handle billing for on-demand usage?" — a feature flow.
- "How is the auth service structured?" — an architectural overview.
- "Walk me through what happens when a user submits a form" — a runtime trace.

Identify the scope. If ambiguous, state the best-guess interpretation before exploring. Do not stop for clarification unless different interpretations would materially change the answer or authorized scope; let the user redirect a reasonable interpretation.

Choose the lightest path that can produce a trustworthy mental model:

- **Simple:** A single module, small utility, or narrow function-level question. Skip explorers and use direct explanation.
- **Complex:** A subsystem spanning multiple files or services, a cross-cutting feature, or a broad architectural overview. Run parallel exploration before synthesis.

When in doubt, lean simple. Escalate to explorers if direct investigation exposes meaningful independent slices.

### 2a. Explore Complex Questions

Decompose the question into two to four distinct exploration angles so agents do not repeat the same work. For example, a rate limiter might split into:

- Data model and state management.
- Request path and enforcement.
- Configuration and metrics infrastructure.

Resolve `how_explorer` once and launch every explorer concurrently with that assignment:

- Use the resolved runner, model, effort, and Fast setting exactly.
- Start without inherited conversation history and provide a self-contained assignment.
- Read-only role; no delegation or file modification.

Read [references/explorer-prompt.md](references/explorer-prompt.md) in full. Give every explorer the same base prompt plus exactly one named angle. Each explorer returns components, flow, files read, boundaries, non-obvious behavior, and open questions.

Overlap is acceptable where slices meet; the explainer reconciles it. Wait for all useful reports under the operating boundary above.

### 2b. Explain Directly

For a simple question, resolve and launch `how_simple_explainer`:

- Use the resolved runner, model, effort, and Fast setting exactly.
- Start without inherited conversation history and provide the question, repository root, known target, and applicable repository instructions.
- Read-only role; no delegation or file modification.

Read [references/explainer-prompt.md](references/explainer-prompt.md) in full. Tell the agent that no explorer reports exist and it must perform the bounded exploration itself before explaining.

### 3. Synthesize Complex Questions

After the explorers return, resolve and launch `how_complex_explainer`:

- Use the resolved runner, model, effort, and Fast setting exactly.
- Start without inherited conversation history.
- Read-only role; no delegation or file modification.

Build its prompt from [references/explainer-prompt.md](references/explainer-prompt.md). Include the original question, repository root, every explorer report including gaps or contradictions, and applicable repository instructions. The explainer may read the code to reconcile conflicts and fill focused gaps; it should not restart the whole exploration.

### 4. Validate and Present

The parent agent retains final judgment. Check material file and symbol references, resolve demonstrable contradictions, and ensure the explanation distinguishes observed mechanics from inferred historical intent. Lightly edit for clarity without replacing the explainer's mental model.

Use this structure as relevant:

- **Overview.** What the subsystem is, what it does, and its current role.
- **Key Concepts.** The types, services, or abstractions needed to understand the flow.
- **How It Works.** The trigger-to-effect path, data movement, decisions, side effects, and failure behavior.
- **Where Things Live.** A compact map of the files and directories needed to start working in the area.
- **Gotchas.** Non-obvious behavior, sharp edges, and explicitly documented context. Do not speculate about historical reasons.

## Critique Mode

Use Critique mode when the user asks for architectural issues, improvements, responsibility placement, ownership, or layering judgment rather than understanding alone. Do not auto-apply recommendations.

### 1. Explain First

Complete Explain mode before critiquing. Reuse an explanation produced in the current task when it is still accurate. Architecture cannot be judged responsibly from file names or a narrow diff alone.

### 2. Prepare One Shared Critic Prompt

Resolve and read these files in full:

- [references/critic-prompt.md](references/critic-prompt.md)
- [references/critique-rubric.md](references/critique-rubric.md)
- [references/architecture-principle-routing.md](references/architecture-principle-routing.md)

Use the completed explanation and relevant code to select the core and concretely triggered conditional principles. Resolve them to absolute paths and read every selected `SKILL.md` completely. How selects these leaves directly; do not invoke `apply-principles` inside the panel.

Fill the critic template with:

1. The completed architectural explanation.
2. The relevant absolute file paths.
3. The critique rubric contents.
4. The ordered list of absolute selected principle skill paths.
5. Applicable repository instructions.

Both critics receive exactly the same prompt and inspect the actual code. Diversity comes from the models, not assigned personas.

Record `git status --short` before launching critics so unexpected mutations can be detected.

### 3. Run Critics Concurrently

| Critic | Assignment |
|---|---|
| Critic A | Resolved `how_critic_a` |
| Critic B | Resolved `how_critic_b` |

1. Resolve both critic roles and confirm both configured runners are callable.
2. Launch both immediately with no inherited conversation context and the exact same prompt. For a `claude-code` assignment, read [Claude Code](../claude-code/SKILL.md) in full and pass the resolved model and effort explicitly.
3. Let both critics run concurrently under the operating boundary. Monitor each through its configured process or native agent status.
4. Capture each complete report and its available model provenance before closing native agents.
5. Recheck `git status --short`. If a critic changed the repository, do not accept, revert, or hide the changes automatically. Report the mutation and exclude the violating result.

If one critic fails, inspect its failure once, preserve the concrete blocker, and continue with a clearly degraded panel. If both fail, stop the critique and return the explanation plus the blockers.

### 4. Apply Parent Lead Judgment

Read [Interrogate's lead-judgment reference](../interrogate/references/lead-judgment.md) in full. Do not invoke Interrogate itself.

The parent is a pragmatic lead, not an aggregator:

1. Parse and deduplicate findings.
2. Treat independent agreement as stronger signal without making it mandatory.
3. Note explicit disagreements.
4. Verify concrete execution paths and architectural claims in the code.
5. Reject hypothetical, preference-only, premature-abstraction, or context-blind findings.
6. Categorize every finding as **Act on**, **Consider**, **Noted**, or **Dismissed**, with the critic names and a concise rationale.

Present the standalone explanation first, then the critique verdict with Critic summaries, Act On, Consider, Noted, Dismissed, and an Agreement Map. If the architecture is sound, say so; an empty Act On section is valid.

## Failure Modes

- Spawning explorers for a narrow question that one agent can trace directly.
- Splitting explorers by arbitrary file ranges instead of independent system angles.
- Letting explorers write polished answers rather than factual reports.
- Treating code shape as proof of historical motivation.
- Critiquing before establishing the current flow and boundaries.
- Sending different rubrics or personas to critics and mistaking prompt diversity for model diversity.
- Aggregating every critic suggestion without parent judgment.
- Interrupting an agent solely because it has run for a long time.
