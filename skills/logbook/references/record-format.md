# Logbook record format

Store records at:

```text
.agents/logbook/{proposed,implemented,rejected}/YYYY-MM-DD-topic-title.md
```

The date is when the durable topic was first recorded. Keep that date when moving a record between lifecycles. Use a short lowercase hyphenated topic title.

The first five lines are:

```markdown
# Logbook: <title>

Status: proposed
Kind: architecture

```

`Status` must match the lifecycle folder. `Kind` is one of:

- `architecture`
- `behavior`
- `bug-fix`
- `simplification`
- `process`
- `testing`

Use this body for `proposed` and `rejected` records:

```markdown
## Problem

The durable problem or pressure, stated without assuming the proposal.

## Proposal

The concrete direction that is being considered or was rejected.

## Alternatives considered

Only genuine alternatives and why each lost or remained unresolved.

## Evidence

Observed code, tests, incidents, measurements, tickets, prototypes, or verification relevant to the choice. Name gaps.

## Consequences

What the proposal buys, costs, constrains, or deliberately gives up.

## Revisit when

Concrete observations, invalidation signals, or changed constraints that justify reopening the decision.
```

Use this body for `implemented` records:

```markdown
## Problem

The durable problem or pressure, stated without assuming the decision.

## Decision

Present-tense shipped reality. Name the owner, boundary, contract, or mechanism precisely enough to guide later work without duplicating an implementation inventory.

## Alternatives considered

Only genuine alternatives and why each lost.

## Evidence

The implementation and fresh verification that support the record. Link repository paths relatively when useful and name remaining gaps.

## Consequences

What the decision buys, costs, constrains, or deliberately gives up.

## Revisit when

Concrete observations, invalidation signals, or changed constraints that justify reopening the decision.
```

Additional technical sections are allowed between the primary `Proposal` or `Decision` section and `Alternatives considered` when they materially clarify a contract, schema, flow, or migration. Do not append chronological updates. Keep current factual realization in place and let version control carry chronology.

For a rejected record, state the rejection and its evidence in the existing sections. Retain it only while the rationale prevents a plausible mistake. For a superseded implemented decision, create the replacement record and cross-link both; never rewrite the old rationale into its opposite.
