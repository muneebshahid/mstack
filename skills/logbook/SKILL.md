---
name: logbook
description: "Capture, update, or refresh repository-local decision records that preserve rationale, genuine alternatives, evidence, consequences, and revisit conditions. Use explicitly, or from Implement when work makes a durable decision maintainers may otherwise relitigate."
---

# Logbook

Preserve the parts code and ordinary documentation cannot carry: why a durable direction was chosen, which genuine alternatives lost, what evidence supported the choice, what it cost, and what would justify revisiting it.

The default repository root is `.agents/logbook/` with three lifecycle folders:

- `proposed/`: a durable direction is under active implementation or separately recorded before implementation.
- `implemented/`: the decision is present-tense shipped reality.
- `rejected/`: a previously durable proposal was declined and remains useful because it prevents plausible re-litigation.

Keep records flat within each lifecycle. Classification belongs in the record, not another directory layer. Do not create an index; search filenames, headings, kinds, and content.

## Authority

Logbook may write only inside the repository's declared logbook root. It does not authorize source edits, commits, staging, branches, pushes, pull requests, tickets, deployments, or external mutations.

- An explicit request to capture or refresh the logbook authorizes the corresponding logbook-only edits.
- An active Implement workflow may invoke Capture for a decision-bearing authorized change. The Implement parent writes and validates the record; this logbook-only authorship is distinct from project source writing and does not grant commit authority.
- Architect, Arena candidates, reviewers, investigators, and external consultants remain read-only. They may supply rationale or evidence but never write records.
- The configured implementation worker supplies factual implementation evidence and clarification but never creates, updates, moves, or deletes a record.
- Preserve unrelated records and user changes. Do not delete a record unless the active request clearly authorizes cleanup and the record meets the retirement rules below.

## What deserves a record

Capture or update a record when maintainers may reasonably revisit a non-obvious choice, especially:

- A load-bearing architecture, ownership, boundary, dependency, or domain-model decision.
- A public, persistent, wire, configuration, or cross-package contract.
- A choice among credible alternatives whose tradeoffs are not visible from the resulting code.
- A non-obvious bug mechanism, failed approach, or operational constraint likely to recur.
- A meaningful removal whose reintroduction conditions matter.
- A process or testing strategy that constrains future work.

Skip mechanical edits, routine local implementation choices, temporary experiments, speculative ideas, and facts already obvious from code, types, tests, schemas, or user documentation. Do not create one record per commit or implementation unit. One record owns one durable decision and may be updated by several related units.

## Evidence and authority

Search before writing. If an active record already owns the same decision, update it rather than creating a duplicate.

- Current code, tests, schemas, and contracts are authoritative for present mechanics.
- An implemented record is evidence of recorded rationale and tradeoffs, but stale factual paths or symbols must be corrected.
- Proposed and rejected records are historical context, not authority for shipped behavior.
- Record only alternatives actually considered. Never invent alternatives to fill the format.
- Separate verified facts from interpretation and unresolved uncertainty.

Read [references/record-format.md](references/record-format.md) completely before creating, moving, or materially updating a record.

## Capture mode

Use Capture when the user explicitly requests a record or Implement identifies decision-bearing work.

1. Search `.agents/logbook/` and relevant repository history for an existing owner, duplicates, superseded decisions, and useful cross-links.
2. Decide whether the threshold above is met. If not, do not manufacture a record; explain briefly why the code, tests, or ordinary documentation already carry the information.
3. Choose the lifecycle:
   - Create `proposed` when a substantial decision will span multiple verifiable commits or the user explicitly wants a pre-implementation proposal recorded.
   - Create `implemented` directly for a verified decision completed in one change.
   - Move a durable proposal to `implemented` only after the corresponding behavior is implemented and freshly verified; rewrite proposal language into present-tense reality.
   - Move a durable proposal to `rejected` when it was genuinely declined and retaining the reason prevents a plausible future mistake.
4. Write the smallest record that preserves the decision. Include genuine rejected alternatives from Architect or investigation, but do not create separate records for ordinary Arena losers or discarded hypotheses.
5. Keep factual paths, names, defaults, and mechanisms aligned with the actual diff. If implementation changes the accepted design, record only the parent-approved resulting decision.
6. Run `scripts/validate_logbook.py <repository>/.agents/logbook` and resolve every applicable violation.
7. Report the record path, lifecycle, decision it owns, and any unresolved staleness or evidence gap.

During Implement, the parent writes or moves the record after inspecting the relevant implementation unit and its fresh verification. It combines accepted rationale, Architect's note-ready material when available, and factual evidence from the configured worker without delegating authorship or lifecycle judgment to that worker. The parent may ask the worker for missing implementation facts, consequences, constraints, or evidence, then updates and validates the record itself. When commits are authorized, the record change belongs in the same decision-bearing commit as the code it explains.

## Refresh mode

Use Refresh only when explicitly requested. Scope it to the named records or affected subsystem unless the user asks for a repository-wide pass.

1. Compare implemented records with current code, tests, schemas, and contracts. Correct factual realization such as moved paths, renamed symbols, defaults, and mechanisms without rewriting the original rationale into a different decision.
2. Find duplicate owners and partial or full supersession. Cross-link partial supersession. A reversed decision gets a new record; do not edit the old record into its opposite.
3. Move an obsolete proposal to `rejected` when its rejection remains useful. Recommend deletion when it no longer prevents a plausible mistake; delete only with authority.
4. Consolidate only when one current record can preserve every unique rationale, alternative, consequence, evidence gap, and revisit condition. Repair inbound links in the same change.
5. Validate the resulting tree and report refreshed, moved, consolidated, stale, and intentionally retained records.

Do not add archive manifests, translations, sidecars, generated indexes, or CI integration unless actual scale or repeated drift demonstrates that the extra machinery earns its cost.

## Integrations

- **Architect:** reads relevant implemented records during grounding and returns note-ready Problem, Decision, Alternatives considered, Consequences, Evidence, and Revisit when material. It never writes.
- **Implement:** owns conditional automatic Capture and record lifecycle during code-changing work.
- **Why:** treats relevant records as repository evidence of stated rationale while checking shipped mechanics against current code and history.
- **Bug Fix:** uses `Kind: bug-fix` for a non-obvious solved problem; there is no separate solved-problems tree.
- **No Comments:** routes durable historical rationale here only when the decision-bearing threshold is met. Logbook is not a dumping ground for deleted comments.

## Failure modes

- Recording every non-trivial edit until the logbook becomes a changelog.
- Treating a record as stronger evidence of current behavior than the code and tests.
- Inventing alternatives, certainty, or evidence after the fact.
- Writing `implemented` before the decision is both realized and freshly verified.
- Creating a rejected record for every Arena candidate or failed debugging hypothesis.
- Rewriting an old rationale to pretend the current decision was always intended.
- Letting a record substitute for types, tests, schemas, runtime checks, or ordinary user documentation.
