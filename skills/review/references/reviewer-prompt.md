# Reviewer prompt

Adapt this template to the assignment, giving independent reviewers the same requirements and evidence.

---

Review the supplied code or design against its requirements, complexity, and test usefulness. Report problems supported by evidence. No findings is a valid result.

This is a read-only assignment in an existing panel. Do not edit project files or change external systems. Investigate directly by default, using surrounding code and relevant references as needed. Leave panel coordination to the parent.

## Scope and requirements

{SCOPE_AND_REQUIREMENTS}

## Review target

{SNAPSHOT_PATH_OR_CONTENT}

## Project instructions

{PROJECT_INSTRUCTIONS}

## Review references

Use these references as a starting point, consulting relevant sections and further guidance as needed:

{REVIEW_CRITERIA_AND_PRINCIPLE_PATHS}

## Findings

Use this format when useful for reporting findings:

- A local ID such as `R-1` and a verified file/line or symbol.
- The problem, consequence, and severity based on that consequence.
- The violated requirement or reachable failure path, with preconditions and evidence. For change reviews, distinguish introduced from pre-existing issues.
- Unresolved assumptions or evidence that weakens the claim.
- The smallest useful correction, if known. For test findings, name the regression at risk or explain why the test adds no protection.

Security and concurrency claims need demonstrated paths. Exclude invented requirements, hypothetical defenses, style preferences, and tests added merely for completeness.

Report checks performed, access failures, and evidence gaps. If no findings are justified, say so.
