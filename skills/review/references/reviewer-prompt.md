# Reviewer prompt

Fill this template and send the same prompt to both reviewers.

---

Review the supplied code or design against its requirements, complexity, and test usefulness. Report problems supported by evidence. No findings is a valid result.

This is a read-only assignment in an existing panel. Do not edit project files, change external systems, invoke orchestration or selection workflows, or delegate. Read surrounding code to check claims.

## Scope and requirements

{SCOPE_AND_REQUIREMENTS}

## Review target

{SNAPSHOT_PATH_OR_CONTENT}

## Project instructions

{PROJECT_INSTRUCTIONS}

## Review references

Read these documents in full; the parent has selected them:

{REVIEW_CRITERIA_AND_PRINCIPLE_PATHS}

## Findings

For each finding, return:

- A local ID such as `R-1` and a verified file/line or symbol.
- The problem, consequence, and severity based on that consequence.
- The violated requirement or reachable failure path, with preconditions and evidence. For change reviews, distinguish introduced from pre-existing issues.
- Unresolved assumptions or evidence that weakens the claim.
- The smallest useful correction, if known. For test findings, name the regression at risk or explain why the test adds no protection.

Security and concurrency claims need demonstrated paths. Exclude invented requirements, hypothetical defenses, style preferences, and tests added merely for completeness.

Report checks performed, access failures, and evidence gaps. If no findings are justified, say so.
