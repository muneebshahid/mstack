# Compare designs

Use independent proposals to resolve a consequential design choice. Adapt this method to the task; the parent chooses the result and any need for separate judgment.

## Prepare

Define the requested design, constraints, evidence, and criteria that distinguish a good solution. Derive criteria from the task rather than numerical scores or a fixed rubric length.

Resolve `architect_candidate_a` and `architect_candidate_b` through [model configuration](../../setup-mstack/references/runtime-resolution.md). Follow the configured runners' instructions. Record the current commit, status, and diff before launching.

A useful default is two independent candidates with the same self-contained prompt covering:

- The requested outcome, constraints, assumptions, and relevant project evidence.
- Repository instructions and the parent-selected principle reference paths.
- The [design template](design-template.md), comparison criteria, and [Source Style](../../apply-principles/references/source-style.md).
- A read-only assignment to propose a concrete design and report evidence gaps or tool failures. Candidates investigate directly by default and leave comparison coordination to the parent. They do not edit project files or read each other's output before proposing their own design.

Provide reference paths for candidates to consult as needed. Exclude secrets and unrelated material; do not tell candidates which solution the parent prefers.

## Run

Launch the two candidates concurrently in fresh contexts. Retain their process or agent identifiers, monitor completion, and capture reports and available model provenance before closing them. Keep external artifacts outside the repository.

Use judgment about retrying, reframing, or continuing with available evidence after a failure. Honor explicit model choices and report what ran, any substitutions, and resulting limits. One usable proposal can inform a design but does not establish an independent comparison.

Compare repository state after the candidate phase. Report unexpected edits and exclude compromised output. If attribution is unclear, assess what evidence remains trustworthy before continuing; do not silently keep or revert the edits.

## Choose

Assess the complete proposals against the requirements and criteria. Select one coherent design. Adopt ideas from another only when they improve it without conflicting with its contracts or ownership. Record the source and reason for significant adoptions and rejections.

Reframe and rerun if needed.

If a disputed choice needs independent judgment, resolve `consultant_default` through model configuration and use its runner. Give it the question, criteria, and complete proposals under neutral labels, including evidence gaps, without the parent's preference. The parent checks its reasoning and decides. Recheck repository state after consulting; report unexpected edits and exclude compromised judgment without silently keeping or reverting the edits. Report an unavailable consultant and judge directly if the evidence permits; otherwise leave the decision unresolved.

Check the final design against the task and the [design template](design-template.md). Return the selected design, reasons, remaining uncertainties, and comparison failures. Include captured model provenance in the Logbook material for the parent. Implementation belongs to the calling workflow.
