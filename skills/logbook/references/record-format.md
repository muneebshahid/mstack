# Logbook entry templates

Every entry starts with `# Logbook: <title>`. Use the sections for its class in order. Omit Gaps when nothing is left unverified.

## Decision

```markdown
# Logbook: <title>

## Context

The problem or finding that required a choice, with the evidence that matters.

## Decision

What was chosen and why. Mark preferences as "owner's call".

## Rejected

Each option considered or tried, and why it lost. State when none were considered.

## Verification and gaps

Checks performed and what remains unverified.
```

## Incident

```markdown
# Logbook: <title>

## What happened

The symptom, and how it was found: issue, CI run, review, test, or report.

## Cause

Why it happened.

## Fix

What changed. Link commits other than this entry's own.

## Prevention

The test, check, or rule that now catches it, or why none was added.

## Gaps

What remains untested or unexplained.
```

## Investigation

```markdown
# Logbook: <title>

## Question

What was investigated and why.

## Findings

What was found, each with its source and date.

## Conclusion

What the findings mean for this repository.

## Open questions

What remains unknown, and what would change the conclusion.
```
