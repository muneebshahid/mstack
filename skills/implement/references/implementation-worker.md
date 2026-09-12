# Implementation worker

Resolve `implement_worker` through [model configuration](../../setup-mstack/references/runtime-resolution.md) and use its native runner.

Give it the requested outcome, relevant context and principles, owned scope, design constraints, and verification target. Ask for the changes, check results, and any design conflicts or blockers. The parent writes Logbook records.

Inspect the actual diff and check results. Send concrete feedback to the same worker and retain it across related units and design revisions. Close it when finished.

If the worker fails, report the failure and use judgment to retry, replace it, or continue directly. Stop any active writer and inspect partial edits before transferring ownership. Honor explicit model or delegation requirements and report substitutions.
