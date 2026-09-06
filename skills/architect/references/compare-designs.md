# Compare designs

Use independent proposals to resolve a consequential design choice. The parent chooses the result; a separate judge is optional.

## Prepare

Define the requested design, constraints, evidence, and criteria that distinguish a good solution. Derive criteria from the task rather than numerical scores or a fixed rubric length.

Resolve `architect_candidate_a` and `architect_candidate_b` through [model configuration](../../setup-mstack/references/runtime-resolution.md). Follow the configured runners' instructions. Record the current commit, status, and diff before launching.

Give both candidates the same self-contained prompt with:

- The requested outcome, constraints, assumptions, and relevant project evidence.
- Repository instructions and the parent-selected principle reference paths.
- The [design template](design-template.md), comparison criteria, and [Source Style](../../apply-principles/references/source-style.md).
- A read-only, no-delegation assignment to produce one concrete design and report evidence gaps or tool failures. Candidates must not edit project files, read each other's output, or invoke orchestration or principle-selection workflows.

Provide paths to references and require candidates to read them. Exclude secrets and unrelated material; do not tell candidates which solution the parent prefers.

## Run

Launch the two candidates concurrently in fresh contexts. Retain their process or agent identifiers, monitor completion, and capture reports and available model provenance before closing them. Keep external artifacts outside the repository.

Do not substitute models or repeatedly retry a failed runner. With one usable candidate, return it with the blockers as an incomplete comparison. With none, report the blockers. Do not claim independent comparison with fewer than two usable proposals.

Compare repository state after the candidate phase. Report unexpected edits and exclude compromised output. If attribution is unclear, stop the comparison rather than assuming one candidate is unaffected; do not silently keep or revert the edits.

## Choose

Read every complete proposal and compare it against the requirements and criteria. Select one coherent design. Adopt ideas from another only when they improve it without conflicting with its contracts or ownership. Record the source and reason for significant adoptions and rejections.

Reframe and rerun if needed.

If a disputed choice needs independent judgment, resolve `consultant_default` through model configuration and use its runner. Give it the question, criteria, and complete proposals under neutral labels, including evidence gaps, without the parent's preference. The parent checks its reasoning and decides. Recheck repository state after consulting; report unexpected edits and exclude compromised judgment without silently keeping or reverting the edits. Report an unavailable consultant and judge directly if the evidence permits; otherwise leave the decision unresolved.

Check the final design against the task and the [design template](design-template.md). Return the selected design, reasons, remaining uncertainties, and comparison failures. Include captured model provenance in the Logbook material for the parent. Implementation belongs to the calling workflow.
