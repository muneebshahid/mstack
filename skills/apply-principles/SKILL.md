---
name: apply-principles
description: "Select engineering standards when a design, implementation, or review needs guidance across several concerns."
---

# Apply Principles

The ten references below hold the canonical standards. This index selects which to read.

For every owned-source edit, read [Source Style](references/source-style.md) before applying the change.

## Select

Choose the smallest relevant set using the task and evidence, rather than loading the whole catalog.

| Reference | Read when |
|---|---|
| [Simplicity](references/simplicity.md) | adding or removing complexity, or reducing the work needed to trace behavior |
| [Modeling and Types](references/modeling-and-types.md) | designing domain values, states, transitions, or type constraints |
| [Ownership and Contracts](references/ownership-and-contracts.md) | assigning responsibility, changing public contracts, parsing or validating boundary data, translating errors, or correcting dependencies and cycles |
| [Concurrency and Retries](references/concurrency-and-retries.md) | actors may write concurrently, or operations may repeat or partially fail |
| [Delivery and Migration](references/delivery-and-migration.md) | sequencing multi-step work or migrating APIs and callers |
| [Diagnosis](references/diagnosis.md) | investigating a bug, failed check, crash, or workaround |
| [Verification](references/verification.md) | checking a completion claim, changed artifact, delegated result, or user path |
| [Design Decisions](references/design-decisions.md) | choosing an experience, comparing consequential alternatives, or reconsidering a shape that fights a requirement |
| [Automation and Learning](references/automation-and-learning.md) | considering automation or preventing a recurring correction |
| [Source Style](references/source-style.md) | editing owned source, auditing comments, docstrings, or suppressions, or making sketches and scaffolds |

## Apply

Read selected references completely. Reuse guidance still available in context; reread it when changed or unavailable. New evidence may warrant another reference. Prefer a concrete requirement, contract, failure, or material risk over a broad heuristic.

Resolve links relative to the containing MStack skill or reference in the same plugin installation, never the consumer project's working directory. Selected filenames resolve under this skill's `references/` directory.

For panels and delegated reviewers, the parent selects and reads the references, then passes the same ordered absolute paths to every participant. Each participant reads those documents in full without running another selector. They are reference documents, not skill entrypoints.

Report important outcomes, evidence, and tradeoffs.
