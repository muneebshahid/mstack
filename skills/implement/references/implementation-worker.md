# Implementation worker

Use [Delegate](../../delegate/SKILL.md) with `implement_worker` and `allow_writes=true` for the assigned edit scope. Leave `allow_subagents=false`.

Provide the outcome, collected findings, source and principle paths, edit scope, constraints, and verification target. Request changes, check results, and conflicts or blockers. The parent writes Logbook records.

Inspect the diff and check results. Keep the same worker for feedback, related units, and design revisions; close it when finished.

If the worker fails, report the failure and use judgment to retry, replace it, or continue directly. Stop any active writer and inspect partial edits before transferring ownership. Honor explicit model or delegation requirements and report substitutions.
