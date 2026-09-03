---
name: principle-no-comments
description: "Eliminate human-authored comments and docstrings from owned source code, except temporary TODO markers and TODO pseudocode in explicitly designated pre-implementation design sketches or executable architecture scaffolds. Make completed code explain itself, encode constraints mechanically, and keep agent decisions in an external logbook."
---

# No comments

Completed owned source code contains no human-authored comments or docstrings. Code explains behavior through names, types, structure, and executable constraints. Durable agent decisions and historical rationale belong in the repository [Logbook](../logbook/SKILL.md), not beside the implementation.

The sole workflow exception is an explicitly designated, temporary pre-implementation design sketch produced during an architecture workflow such as Arena or Architect, or an executable architecture scaffold created by Implement from an accepted Architect handoff. Such an artifact may use `TODO` comments or `TODO` pseudocode to mark intentionally unimplemented bodies. The exception expires when the body is implemented or the artifact is promoted to completed source.

This is a principle, not an orchestration workflow. It does not spawn a comment-review agent and does not authorize edits outside the caller's scope.

## Apply when

- Designing or implementing code under the zero-comments policy.
- Reviewing a diff, branch, or codebase for comments and docstrings.
- Producing or completing a temporary architecture sketch or Implement scaffold containing `TODO` markers or pseudocode.
- A comment defends a workaround, surprising behavior, or unenforced constraint.
- A lint, type, formatter, or coverage suppression appears in source.

Apply it to source code, tests, scripts, and configuration. Prose documentation and `.agents/logbook/` records are separate artifacts, not source comments.

## Rule

Delete human-authored:

- Narrative inline and block comments.
- Docstrings and public API doc comments.
- Section banners and labels.
- Commented-out code.
- TODO, FIXME, HACK, IMPORTANT, and "do not remove" notes.
- Workaround explanations and historical narratives.
- Lint, type, formatter, coverage, or compiler suppression comments.
- Comments that repeat a name, signature, expression, branch, or test.

## Temporary design-sketch exception

Allow a comment only when all of these are true:

- The file or artifact is explicitly identified as a temporary pre-implementation design sketch or executable architecture scaffold.
- For project source, Implement owns the scaffold and an accepted Architect handoff names the types, signatures, or module seams it is meant to expose.
- The comment starts with `TODO` and either marks an intentionally unimplemented body or contains pseudocode for that body.
- The comment exists to make a proposed control-flow or contract shape inspectable before implementation.
- The comment will be removed when implementation fills the body.

The exception does not cover rationale, historical context, warnings, workaround explanations, suppressions, commented-out implementation, `FIXME`, `HACK`, or ordinary production TODOs. Put design rationale in the external design artifact or decision logbook. A sketch or scaffold carrying these TODOs is not complete and cannot satisfy final verification.

Do not shorten or polish a comment that should disappear. Remove it and make the code carry the information.

## Replace prose with structure

When deleting a comment would make owned code surprising, reshape the code:

- Rename symbols so their role and units are explicit.
- Extract a function or type that names the concept.
- Replace flag combinations and optional-field bags with explicit variants.
- Move responsibilities until control flow reads from intent to detail.
- Delete dead paths, obsolete parameters, and temporary compatibility layers.
- Expose a narrow API that prevents misuse instead of warning callers in prose.

If the required reshape is outside the caller's authorized scope, delete no evidence silently. Report the unresolved code smell and the exact symbol that still needs work.

## Encode constraints

Replace "do not", "must", and "only" comments with the cheapest executable enforcement that fits the scope:

- A type that makes the invalid state unconstructable.
- Boundary validation or a runtime assertion.
- A focused regression test.
- A lint, formatter, schema, or CI rule.
- An API that does not expose the forbidden operation.

If the constraint cannot be encoded in scope, report it as open work. Capture it through Logbook only when it is a durable decision maintainers may reasonably revisit; do not turn every deleted comment into a record.

## Suppressions

Treat suppressions as failures to resolve, not comments to retain.

1. Identify the rule and why the code violates it.
2. Fix the code, configuration, generated boundary, or faulty rule at the narrowest correct level.
3. Remove the suppression.
4. Run the relevant check to prove the suppression is unnecessary.

Do not weaken a correctness or safety rule to make the comment disappear.

## Files we do not own

Do not edit generated, vendored, or third-party files merely to remove their comments. Required legal or license headers also remain. Exclude these files from the owned-code count and report them separately when they affect a zero-comments audit.

If a tool requires a source directive, first try configuration, file exclusion, code restructuring, or another supported mechanism. When no comment-free mechanism exists, report the tool conflict rather than claiming full compliance.

## Verification

For a review:

1. Enumerate comments and docstrings in scope without mistaking string literals or data for comments.
2. Classify non-owned files and mandatory legal headers separately.
3. For each owned comment, identify the deletion, reshape, or executable encoding needed.
4. Classify valid temporary design-sketch or executable-scaffold TODOs separately and confirm that the artifact is still incomplete.
5. Report policy or tool conflicts explicitly.

For an authorized improvement:

1. Remove comments and docstrings in scope.
2. Implement the smallest necessary reshapes and encodings.
3. Run formatting, lint, type checks, and relevant tests.
4. Report the owned-code comment count before and after, remaining external artifacts, and unresolved constraints.

Zero owned-code comments is the completion predicate. Temporary design-sketch or executable-scaffold TODOs are allowed only before completion and must reach zero when their bodies are implemented.
