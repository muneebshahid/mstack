---
name: arena
description: "Run an explicit multi-model competition for a consequential artifact: generate independent candidates, score them against one rubric, select a base, graft the strongest ideas, and verify one coherent result. Use only when the user or another active skill explicitly invokes Arena."
---

# Arena

Fan out independent attempts at the same consequential artifact. Read every candidate end to end, choose the strongest base against an explicit rubric, graft only compatible strengths from the others, and verify one coherent result.

Arena is a read-only orchestration workflow, not mutation authority. Keep candidate prompts, reports, and intermediate artifacts outside the repository. Return the synthesis to the caller; route any project code changes through [Implement](../implement/SKILL.md).

## Operating boundary

- Use Arena only when explicitly invoked by the user or an active workflow.
- Use it when one attempt could lock in the wrong shape and competing concrete artifacts would expose meaningful tradeoffs.
- Skip it for mechanical work, clear precedent, tightly constrained fixes, or choices whose constraints leave one viable shape.
- Candidates work independently and do not see one another's output.
- Candidates do not edit the project, commit, push, mutate external systems, or delegate.
- An artifact explicitly designated as a temporary pre-implementation design sketch may contain `TODO` comments or `TODO` pseudocode marking intentionally unimplemented bodies. It is not completed source, and every such comment must be removed when implementation fills the body.
- Preserve candidate dropouts, capability failures, disagreements, and rejected alternatives in the synthesis record.

## 1. Frame

Define the artifact before launching candidates:

1. State exactly what each candidate must produce.
2. State the relevant constraints, grounding evidence, repository root, and applicable repository instructions.
3. Derive three to six concrete, gradeable criteria from the task. The rubric belongs to judging; do not give candidates a preferred answer.
4. Decide whether the default two candidates are enough. Add candidates only when the task contains more genuine design directions than two attempts can reasonably expose or the caller requests a larger panel.

Read [references/candidate-prompt.md](references/candidate-prompt.md) and prepare one self-contained base prompt. All default candidates receive the same task, evidence, constraints, and output contract. Process-boundary instructions may differ because Fable and native Codex use different launchers.

Record the current commit, `git status --short`, and tracked diff before launching candidates so unexpected project mutations can be detected. This is a best-effort audit, not a sandbox: the role instructions remain the primary boundary.

## 2. Fan out

Launch the default candidates concurrently:

| Candidate | Execution |
|---|---|
| A | Claude Fable 5.1, `xhigh`, through the `claude-code` skill; report the launcher-verified served model |
| B | GPT-5.6 Sol, `xhigh`, through a native Codex subagent |

For Fable:

1. Read [Claude Code](../claude-code/SKILL.md) completely.
2. Write the candidate prompt to a temporary file outside the repository and create a separate temporary output directory.
3. Start the launcher with `--model claude-fable-5-1 --effort xhigh` in a managed terminal session and yield as soon as it is running.

Immediately launch the native Sol candidate with no inherited conversation history using `model: gpt-5.6-sol` and `reasoning_effort: xhigh`. Give it the same candidate prompt and a read-only, no-delegation role. Retain its agent identifier for native wait and close operations.

Let both candidates run concurrently. Monitor Fable through its managed process and Sol through native agent status. Long elapsed time or a coarse `running` status is not a stall. Intervene only on concrete evidence of looping, repeated failure, irrelevant expansion, or another demonstrably unproductive pattern.

After Fable exits, always read `summary.json`; read `claude.result.md` only when the summary reports success. Use the verified served model from the summary in the Arena record rather than assuming a version from the requested alias. Capture the native candidate's complete final report through its native wait result, then close it after preserving the report.

Recheck the current commit, working-tree status, and tracked diff. If repository state changed unexpectedly, do not accept, revert, or hide it automatically. Because candidates ran concurrently, do not invent attribution: report that the candidate phase was compromised and stop unless the mutation can be conclusively attributed and the unaffected result remains trustworthy.

If a candidate fails, inspect the failure once, preserve the concrete blocker, and continue with the surviving output as a degraded Arena. Do not silently substitute another model. If every candidate fails, stop and report the blockers.

## 3. Cross-judge

Wait until all usable candidates are complete. A judge must never inspect partial candidate output.

Read [references/judge-prompt.md](references/judge-prompt.md). Launch one native Codex subagent with the native spawn tool and retain its identifier for wait and close operations:

- Model: `gpt-5.6-sol`.
- Reasoning effort: `xhigh`.
- No inherited conversation history.
- Read-only role; no delegation or project modification.

Give Sol the original task, rubric, every complete candidate labelled neutrally, and all candidate capability issues. Include each complete report directly or provide an exact readable temporary path. Sol scores every criterion, recommends a base, identifies compatible grafts and conflicts, and drafts a synthesis plan. Candidate labels must not reveal model names until judging is complete.

While Sol judges, the parent reads every candidate end to end and scores it independently against the same rubric.

Capture Sol's complete final report through the native wait result and close the agent after preserving it. Recheck the repository audit state after judging. If Sol fails, inspect the failure once, preserve the blocker, and let the parent complete Pick and Graft without a cross-judge; label the Arena degraded. If the judge unexpectedly mutates the repository, report the mutation and exclude its judgment.

## 4. Pick

The parent retains final lead judgment.

1. Compare its criterion-level scores with Sol's judgment.
2. Resolve disagreements by rereading the candidates and the ambiguous rubric criterion.
3. Choose the base that best satisfies the task and can be extended without breaking its own mental model.
4. Prefer the smaller public surface, clearer ownership, and lower reader load when candidates are otherwise tied.

Agreement with Sol strengthens the choice but does not replace parent judgment. Record why the base won and why each other whole shape lost.

When candidates converge independently, record the convergence as evidence; no forced graft is necessary. When they diverge because the task or rubric was under-specified, reframe and rerun instead of averaging incompatible designs. A rerun gets a corrected prompt, fresh neutral labels, new temporary artifacts, and a new run identifier; preserve the previous run and explain why it was superseded.

## 5. Graft and synthesize

Walk each losing candidate once more. Identify the small number of ideas that materially improve the base.

- Graft concepts by hand; never paste incompatible structures together.
- Preserve one vocabulary, ownership model, contract, and mental model.
- Reject a locally attractive idea when it weakens the whole.
- Record each graft's source and each material rejection with its reason.

The parent produces the final synthesized artifact in the response. Sol's synthesis plan is advice, not the deliverable. Arena does not create repository files or apply the artifact to project code.

## 6. Verify

Verify the synthesized artifact against the original task and the same rubric. When executable evidence is required, hand the artifact to Implement rather than writing or running project code inside Arena.

If verification fails, determine whether:

- The framing or rubric was wrong: return to Frame.
- A candidate contained the missing answer and the graft was missed: return to Graft.
- The selected base cannot absorb the requirement coherently: choose another base or rerun Arena.

Do not patch over a failed synthesis merely to finish the workflow.

## Output

Return one synthesized artifact and one compact synthesis record shaped by [references/synthesis-record.md](references/synthesis-record.md). Close completed native agents after their reports have been captured.
