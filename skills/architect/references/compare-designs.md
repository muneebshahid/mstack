# Compare designs

Compare independent proposals for a consequential design choice. Adapt to the task; the parent decides whether separate judgment is needed and chooses the result.

## Prepare

Define the requested design, constraints, evidence, and criteria that distinguish a good solution. Derive criteria from the task rather than numerical scores or a fixed rubric length.

Use [Delegate](../../delegate/SKILL.md) for `architect_candidate_a` and `architect_candidate_b`, with its default read-only scope and no further delegation. Record the current commit, status, and diff before launching.

Give both candidates the same self-contained prompt:

- The requested outcome, constraints, assumptions, collected findings, and relevant source paths.
- Repository instructions and the parent-selected principle reference paths.
- The [design template](design-template.md), comparison criteria, and [Source Style](../../apply-principles/references/source-style.md).
- Propose a concrete design, investigate directly, and report evidence gaps or tool failures. Do not edit project files or read the other candidate's output before submitting. The parent coordinates comparison.

Exclude secrets, unrelated material, and the parent's preferred solution.

## Run

Launch both concurrently in fresh contexts. Monitor completion; retain reports, model provenance, and conversation IDs for follow-ups. Keep external artifacts outside the repository.

Use judgment about retrying, reframing, or continuing with available evidence after a failure. Honor explicit model choices and report what ran, any substitutions, and resulting limits. One usable proposal can inform a design but does not establish an independent comparison.

Compare repository state after the candidate phase. Report unexpected edits and exclude compromised output. If attribution is unclear, assess what evidence remains trustworthy before continuing; do not silently keep or revert the edits.

## Choose

Assess the complete proposals against the requirements and criteria. Select one coherent design. Adopt ideas from another only when they improve it without conflicting with its contracts or ownership. Record the source and reason for significant adoptions and rejections.

Reframe and rerun if needed.

For disputed choices needing independent judgment, use Delegate with `delegate_default`. Supply the question, criteria, evidence gaps, and complete proposals under neutral labels; omit the parent's preference. Check its reasoning and decide. Recheck repository state; report unexpected edits and exclude compromised judgment without silently keeping or reverting edits. If delegation is unavailable, report it and judge directly when evidence permits; otherwise leave the choice unresolved.

Check the final design against the task and the [design template](design-template.md). Return the selected design, reasons, remaining uncertainties, and comparison failures. Include captured model provenance in the Logbook material for the parent. Implementation belongs to the calling workflow.
