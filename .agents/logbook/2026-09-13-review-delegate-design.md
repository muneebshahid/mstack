# Logbook: Review the proposed Delegate flow

## Goal

Get independent Astra max and Fable max feedback on model-only presets, generalizing Consult to Delegate, and a shared `allow_subagents` option for native and external launches.

## Work and decisions

Both reviewers received the same proposal and relevant repository paths in fresh contexts. Their assignment included: “Work directly. Do not launch other agents, even when a skill offers delegation.” The review covered the design, not another full-stack audit. The parent separately mapped affected callers, configuration, and launcher interfaces.

The proposed contract is:

- Presets suggest role-specific model, effort, and Fast settings. The active profile is a selected preset plus user overrides; runtime launch methods do not belong in it.
- Delegate replaces Consult. It chooses native execution when suitable, otherwise the model's external harness, and honors requests for an external process. The caller supplies findings, context, work scope, and output expectations.
- `allow_subagents` defaults to false before launch-method selection. Both native prompts and external turns receive the same no-delegation instruction. Explicit true permits delegation, but each new child independently defaults to false.
- Skill Eval uses fresh external scenario processes that execute the target skill themselves and may receive true. The original parent assesses results. There is no additional evaluator-to-candidate-to-worker layer.
- Existing session IDs, follow-ups, provenance, monitoring, temporary artifacts, and cleanup remain. No new Delegate-plus-Consult pair, task registry, or Herdr integration is proposed.

Both reviewers found this simpler and coherent. The parent accepted these recommendations for the implementation proposal; they have not yet been implemented:

1. **Explicit active configuration.** Both identified the current `CLAUDECODE` fallback in [resolve_config](../../skills/setup-mstack/scripts/models.py). Removing `MSTACK_HOST` alone does not remove host-based selection. The parent favors requiring a saved selection or an explicit preset/configuration for runtime resolution, with Setup handling the initial choice. Carry nondefault configuration paths or explicit selections into children rather than assuming they inherit CLI arguments. Astra also offered one fixed host-independent fallback; that is simpler than host switching but less explicit than the user's chosen-profile model.
2. **Conversation permission on follow-up.** Both recommend retaining the original assignment with the conversation ID and explicitly reapplying its permissions on sends and resumes. New children default false; a resumed conversation keeps its assigned setting unless deliberately changed. No permanent MStack session registry is needed.
3. **Evaluation scenario model.** Astra noted that a multi-model skill has no single unambiguous candidate model. The eval caller should specify the external scenario's model settings; existing smoke assignments cover mechanics checks. Its workers use the shared active profile. No new evaluator-role flag is needed.
4. **Replace the existing boundary.** Fable noted that the launcher's current prohibition on delegating implementation would conflict with an allowed writable delegation. Separate read/write scope from delegation permission and replace the old wording. Both fresh and resumed Codex commands currently hardcode read-only; both need to honor caller-authorized access. This work generalizes the existing launcher rather than replacing its session mechanics.

Rejected or narrowed suggestions:

- Neither reviewer supported an added depth counter. The boolean defaults do not promise an absolute depth cap: an explicitly permitted agent can itself explicitly authorize a child. A child assigned false cannot override its own assignment merely by loading another skill or launching a CLI.
- No tool-level containment claim is made. Prompt policy is the common mechanism across native and external launches; it does not prove a model will obey it.
- Fable asserted that a headless Codex sandbox would block a nested Claude call. The proposed hop was not exercised, and the review did not establish the effective sandbox/network configuration. The parent treats this as an unresolved capability check, not a confirmed universal restriction, and rejects routing all cross-provider evals through Claude without evidence.
- No provider registry, speculative environment filtering, new role taxonomy, or tests that only match wording are justified.

## Result

Both reviewers support proceeding with the design after clarifying configuration, resume semantics, and the scenario model. No implementation or configuration changes were made during this review. The existing uncommitted host-override removal and earlier review records were preserved.

## Verification and gaps

A repository-content hash comparison before and after the panel found no reviewer edits. The parent checked the cited resolver and prompt/command paths. This was design review: no new unit suite, live nested launch, writable-worker evaluation, or permission-adherence experiment was run.

Recommended focused validation after implementation: exercise a mixed-profile external scenario with an authorized write scope, let it launch a worker using default false, resume that worker, and inspect prompts, actual tool activity, files, conversation IDs, and served-model evidence. Cover native and external worker paths. Test the disputed Codex-to-Claude hop before claiming it works or fails. A no-config resolver check should verify the selected missing-configuration behavior.

Astra used native `gpt-6-astra`, requested effort `max`, agent ID `01a09b2f-3810-7393-8614-3583535b8df2`. Fable completed through Consult with served model `claude-fable-5-1` verified, requested effort `max`, session ID `dc0508e8-6374-46ab-b489-d275a455eb5c`; served effort is not exposed by the provider. Neither model was substituted. Temporary prompts and outputs were removed after reading; the provider conversation remains resumable.
