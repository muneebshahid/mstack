# Logbook: Review the consolidated stack with Astra and Fable

## Goal

Review the completed 12-skill consolidation for consequential defects, contradictions, unnecessary complexity, and useful verification.

## Work and decisions

The parent gave fresh Astra max and Fable max reviewers the same read-only assignment at `f7bfb6d`. The scope included all current skills and references, model configuration, the consultant launcher, validation, installation documentation, attribution, and relevant history. Bro and the intentional removals were not redesign targets. Both reviewers reported that the consolidation was coherent; neither found a reason to add skills or expand the workflows.

Accepted findings and recommendations:

- **REV-001 — Consultant host identity, P2.** Astra R-01 and Fable R-4 identified inherited parent environment markers in [process_environment](../../skills/delegate/scripts/run_delegate.py). The parent reproduced a Codex child resolving `claude-native` under `CLAUDECODE=1`, and a Claude child resolving `codex-native` under `MSTACK_HOST=codex`. This affects consultants that resolve another MStack role. Set the child's host from its provider, preserving the user's configuration. This is inherited behavior, not a newly introduced consolidation defect.
- **REV-002 — Python prerequisite, P3.** Astra R-02 identified Python 3.12 type-alias syntax in the launcher, while Setup parses under Python 3.11. The parent reproduced this using Python's versioned grammar parser. Document Python 3.12+ in setup; no compatibility layer is needed.
- **REV-003 — Grill Me invocation, P2.** Fable R-1 identified the missing explicit-invocation policy in the reintroduced skill. The parent verified that the earlier skill disabled implicit invocation and its Logbook rejected automatic conversation-mode changes. Restore that setting and an explicit-request trigger. The missing setting is confirmed; unwanted automatic invocation has not been demonstrated in a live session.
- **REV-004 — Release identity, P3.** Fable R-2 identified substantially different trees sharing version 0.4.0, including removed skills and incompatible configuration keys. Bump the three versioned manifests when releasing the consolidation. Stale installed copies are a known separate state; a version bump alone has not been demonstrated to refresh them.
- **REV-005 — Historical entry correction, P3.** Fable R-3 identified pre-commit wording in [the Grill Me entry](2026-09-13-add-grill-me.md). Its references to pending removals and an uncommitted skill describe the draft, not the committed result: removals were committed as `69ad879`, followed by Grill Me as `f7bfb6d`. This entry records the correction without rewriting the historical account.

Considered but not treated as blocking findings:

- Fable R-5: repository instructions could name the portable validator and omit duplicated preset values. These values are currently consistent; this is small maintenance cleanup.
- Fable R-6: Explain could explicitly place HTML artifacts outside the checkout. The read-only boundary already applies, and no violating write was demonstrated. A short location clarification would be reasonable.

Rejected suggestions and concerns:

- Fable R-7 proposed disabling Fast for native smoke roles because earlier runs could not express it. The setting reflects the user's preference, and runtime guidance already requires capability gaps to be reported. Do not change the preset solely because a particular host cannot express the setting.
- Claude's instruction-only read-only boundary and unverified served Fast tier are disclosed limitations, not newly discovered defects.
- Fewer tests alone do not establish lost regression protection. No new test suite or coverage target is justified by this review.
- The GitHub dependency note remains relevant to PR review. PStack attribution still covers retained derived guidance. Neither requires removal simply because standalone skills were deleted.

## Result

Review only. No skills, scripts, presets, or manifests were changed. Recommended next work is the host-environment correction, Python prerequisite, and Grill Me invocation setting; release versioning and optional wording cleanup can follow. No commit or push was performed.

## Verification and gaps

The parent ran `python3 scripts/validate.py`: all 12 skills, manifests, packaged presets, 131 repository-relative links, 101 files' hygiene, unit suites, and Logbook validation passed. Targeted environment-to-resolver checks reproduced both host errors. Python 3.11 grammar checking rejected the launcher at its type alias and accepted the resolver; an actual Python 3.11 interpreter was not run.

Reviewers left HEAD and the working tree unchanged. This record is the parent's only repository edit. Fable also checked the installed CLI help and relevant cache state. No additional provider smoke calls, live nested Codex execution, or tutoring evaluation were run. Temporary consultation files were removed after reading; the provider conversation remains resumable.

Astra ran as a native `gpt-6-astra` agent with requested effort `max`, agent ID `01a09ad0-bdf6-7a50-b008-327aacb5951e`. Fable ran through Consult as verified `claude-fable-5-1`, requested effort `max`, session ID `954f3108-edae-43c4-9e3c-9cf7a33fd2ed`. Fable completed successfully; its provider does not expose served effort verification. Neither reviewer was substituted.
