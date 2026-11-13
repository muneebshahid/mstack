---
name: apply-principles
description: "Select engineering standards when a design, implementation, or review needs guidance across several concerns."
---

# Apply Principles

The seven references below hold the engineering standards.

## Select

Read only the references the task needs.

| Reference | Read when |
|---|---|
| [Simplicity](references/simplicity.md) | adding or removing complexity, reducing the work needed to trace behavior, designing a module or API, or deciding which tests to write |
| [Modeling and Types](references/modeling-and-types.md) | designing domain values, states, transitions, or type constraints |
| [Ownership and Contracts](references/ownership-and-contracts.md) | assigning responsibility, changing public contracts, parsing or validating boundary data, translating errors, or correcting dependencies and cycles |
| [Concurrency and Retries](references/concurrency-and-retries.md) | actors may write concurrently, or operations may repeat or partially fail |
| [Delivery and Migration](references/delivery-and-migration.md) | sequencing multi-step work or migrating APIs and callers |
| [Design Decisions](references/design-decisions.md) | choosing an experience, comparing consequential alternatives, or reconsidering a shape that fights a requirement |
| [Automation and Learning](references/automation-and-learning.md) | considering automation or preventing a recurring correction |

## Apply

Resolve links relative to the containing MStack skill or reference in the same plugin installation, never the consumer project's working directory.
