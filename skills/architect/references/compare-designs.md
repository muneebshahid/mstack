# Compare designs

Compare independent proposals for a consequential design choice. Adapt to the task; the parent decides whether separate judgment is needed and chooses the result.

## Prepare

Define the requested design, constraints, evidence, and criteria that distinguish a good solution. Derive criteria from the task; no numerical scores.

Use [Delegate](../../delegate/SKILL.md) for `architect_candidate_a` and `architect_candidate_b`.

Give both candidates the same self-contained prompt:

- The requested outcome, constraints, assumptions, collected findings, and relevant source paths.
- Repository instructions and the parent-selected principle reference paths.
- The [design template](design-template.md) and comparison criteria.
- Propose a concrete design, investigate directly, and report evidence gaps or tool failures. Do not read the other candidate's output before submitting.

Exclude secrets, unrelated material, and the parent's preferred solution.

## Run

Launch both concurrently in fresh contexts. Report what ran, any substitutions, and resulting limits. One usable proposal can inform a design but does not establish an independent comparison.

Exclude output from candidates that edited the repository.

## Choose

Assess the complete proposals against the requirements and criteria. Select one coherent design. Adopt ideas from another only when they improve it without conflicting with its contracts or ownership. Record the source and reason for significant adoptions and rejections.

For disputed choices needing independent judgment, use Delegate with `delegate_default`. Supply the question, criteria, evidence gaps, and complete proposals under neutral labels; omit the parent's preference. Check its reasoning and decide.

Return the result in the [design template](design-template.md).
