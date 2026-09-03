# Implementation worker

All project code writing in Implement goes through one persistent native Codex worker for the active task:

- Model: `gpt-5.6-luna`.
- Reasoning effort: `high`.
- Service tier: `priority` (request Codex Fast mode explicitly on the native spawn call).
- Start without inherited conversation history.
- Permit edits only within the active request and the current implementation unit.
- Do not permit delegation, commits, pushes, deployments, external mutations, or adjacent cleanup unless separately authorized.

The worker never creates, updates, moves, or deletes Logbook records. When the parent is considering Logbook capture, the worker supplies factual implementation evidence, newly observed consequences or constraints, invalidation evidence, and clarification on request. The parent alone decides whether a record is warranted, authors it, selects its lifecycle, and validates it.

Verify the served model, reasoning effort, and service tier when the launcher exposes them. If `priority` is rejected, omitted by the launcher, or reported as null, preserve that capability failure and label the worker as standard-speed rather than claiming Fast mode. Continue with the same Luna worker unless the user made Fast mode itself a completion condition.

## Start the worker

Confirm that the active toolset exposes a native subagent spawn operation. If it does not, record a failed launch and stop before project writes. Spawn the worker once after the parent has selected the mode, grounded the task, resolved any Architect checkpoint, and loaded the triggered principles. Give it a self-contained brief containing:

1. The requested outcome, mode, allowed scope, and explicit exclusions.
2. The repository root, repository instructions, and unrelated changes it must preserve.
3. The accepted design or diagnostic conclusion, its load-bearing constraints, adaptable details, unresolved uncertainties, and concrete invalidation signals.
4. The ordered principle paths it must read in full.
5. The first implementation unit's outcome, owned and expected files or surface, relevant interfaces and contracts, dependencies, settled requirements, expected tests, acceptance criteria, and required verification.
6. Any Logbook evidence request: the durable decision the parent is considering and the implementation facts, consequences, constraints, or verification evidence this unit should report. Do not provide the record format or ask the worker to draft or edit the record.
7. The instruction to edit only that unit, run focused checks, inspect its own diff, and return the verification receipt below with the architecture relationship, requested Logbook facts when any, and blockers. The architecture relationship must use exactly one classification:
   - `No deviation`: the implementation follows the contract as written.
   - `Adaptation`: it uses a detail the contract explicitly left flexible; name that latitude and the chosen detail.
   - `Deviation`: identify the affected symbols, expected shape, required shape, observed evidence, and whether the mismatch appears local or architectural.

When the first unit is an explicitly designated executable architecture scaffold, tell the worker which types, signatures, and module seams it must expose and which bodies may temporarily contain TODO markers or TODO pseudocode. The scaffold is incomplete but must keep repository-required checks green. If that is impossible, combine it with the smallest end-to-end implementation slice. Every TODO must disappear as its body is implemented, and none may remain at final verification.

## Verification receipt

Require this factual receipt after every unit:

- Files changed.
- Tests inspected.
- Tests added or changed.
- Failing-before or characterization evidence when applicable.
- Commands and runtime checks executed.
- Exact observed results, distinguishing passes, failures, and inconclusive checks.
- A justified no-test exception when no test was added or changed.
- Remaining risks, blockers, or evidence gaps.

The worker may state that a field is not applicable, but must not omit it. Its receipt is evidence to inspect, not proof by assertion.

The spawn call itself must appear in the execution trace and return a non-empty worker identifier. Surface that exact identifier in the next progress update, retain it, and use the same worker for every unit in this Implement run so feedback and implementation context remain continuous. Do not describe the worker as launched, running, idle, or resumable before this evidence exists.

Worker creation is a hard precondition for project writes. If native spawn fails or does not return an identifier:

- Stop before editing project source.
- Do not issue an empty wait, infer that an untracked process is the worker, or describe the worker as idle or resumable.
- If files change despite the failed launch, treat the run as compromised, preserve the diff, and stop without accepting the changes or inventing authorship.
- Report the exact launcher failure and leave implementation incomplete.

Only call a wait, input, or close operation with the retained identifier explicitly present in its target set. An unavailable spawn tool or a worker that was never launched is a failed worker, not a degraded implementation path.

## Parent review loop

After each unit:

1. Wait for the worker's report, then inspect the actual tree, complete unit diff, and relevant test files independently.
2. Check the receipt against the files and run or inspect the focused checks and matching runtime surface when practical.
3. Compare the unit against the accepted design, adaptation latitude, invalidation signals, principles, scope, unrelated working-tree state, and any Logbook decision the parent is considering or maintaining.
4. Classify every reported or observed difference as no deviation, an adaptable detail, a local correction, or architecture-invalidating evidence. Verify the classification from the diff and runtime evidence; the worker's label is advisory.
5. For an adaptable detail or local correction, send one concrete feedback message to the same worker. Name the observed defect, evidence, required outcome, and verification to rerun. Do not prescribe a patch when the worker can derive the smallest correct change.
6. For architecture-invalidating evidence, do not ask the worker to redesign. If it already exists, keep it idle while the parent re-invokes Architect read-only with the original contract, partial diff, failed check or runtime observation, and deviation record. Resume that same worker with the revised contract after parent judgment. If the contradiction predates worker launch, complete the Architect pass first and spawn only afterward.
7. When Logbook capture is active, decide what the verified unit warrants, ask the worker only for missing factual clarification, then create, update, move, and validate the record directly. The record and implementation must describe one decision. Never delegate Logbook authorship or lifecycle judgment to the worker.
8. Repeat with the same worker until the unit is verified or a precise blocker remains.
9. Only then send the next small unit to that same worker.

The parent may perform read-only inspection and verification commands and may write Logbook records under the Logbook skill's authority. If verification itself requires writing project code or tests, assign that work to the worker as part of the unit. The parent must not patch project source as a shortcut.

Close the worker after its final report is captured and final verification is complete. If an identified worker later becomes unusable, preserve the failure and ask for direction or report the blocker; do not silently switch models or take over code writing.
