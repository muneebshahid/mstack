# Logbook record format

Store records at `.agents/logbook/{proposed,implemented,rejected}/YYYY-MM-DD-topic-title.md`. Use the date the topic was first recorded and keep it across lifecycle moves. Filename topics are lowercase and hyphenated.

The header has this exact layout, including the blank line after `Kind`:

```markdown
# Logbook: <title>

Status: implemented
Kind: architecture

```

`Status` matches the folder. `Kind` is `architecture`, `behavior`, `bug-fix`, `simplification`, `process`, or `testing`.

Keep these sections in order. For proposed and rejected records, replace `Decision` with `Proposal`.

```markdown
## Problem

The problem or question, without assuming the solution.

## Decision

The accepted result and its rationale. Distinguish realized changes and verified conclusions from pending recommendations.

## Alternatives considered

What was actually considered, accepted or rejected, and why. State when no alternatives were considered or the historical record is unavailable.

## Evidence

Consequential work performed, verification, and gaps. Distinguish observations from interpretation and uncertainty. Include agent attribution or session references when useful and available. Link repository files relatively.

## Consequences

Benefits, costs, constraints, and capabilities given up.

## Revisit when

Concrete evidence or changed constraints that would reopen the topic.
```

A Proposal states the direction under consideration or declined; a rejected record explains the verdict and evidence. Optional technical sections may follow Decision or Proposal before Alternatives considered. Update facts in place; do not append dated Update sections or command logs. Preserve historical rationale when superseding a record, and cross-link its replacement.
