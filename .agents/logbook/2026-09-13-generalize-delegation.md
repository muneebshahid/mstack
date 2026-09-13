# Logbook: Generalize delegation and inline skill evaluation

## Goal

Separate model preferences from execution, generalize consultation to scoped delegation, and evaluate proposed skills without installing each variant.

## Work and decisions

The user chose to rename Consult to [Delegate](../../skills/delegate/SKILL.md). A separate launch skill would duplicate consultation mechanics. Native tools remain the first choice when they support the assignment; external Claude or Codex handles other assignments and explicit external-process requests.

Removed host detection, including `MSTACK_HOST` and `CLAUDECODE` selection, and removed runner fields from model configuration. Presets retain their model, effort, and Fast values. The active profile must be selected explicitly through Setup; changing harnesses does not select a different profile. Complete custom roles are supported. Obsolete configuration fields produce correction instructions rather than being silently ignored.

A Luna max worker implemented and tested model configuration. The parent reviewed its diff and requested fewer migration helpers; the worker simplified them. The parent implemented the launcher, skill changes, and live checks.

The user rejected a blanket ban on further delegation after discussing Skill Eval. Instead, every launch has independent `allow_writes` and `allow_subagents` settings, both false by default. Native and external prompts receive the same boundaries. Enabling delegation does not automatically enable it for children. No numeric depth cap, host-based role selection, or special evaluator identity is needed. These are prompt rules; native capabilities and provider permissions still apply.

The launcher accepts inline task text on stdin, records the effective prompt, and reapplies flags on resumed calls. Conversation identifiers and assignments stay in parent context. Temporary artifacts remain disposable; no persistent MStack session registry was added.

Skill Eval now runs each scenario in a fresh external process with the variant and proposed role assignments in its prompt. That process executes the target skill directly. This avoids temporary skill/config installations and an extra candidate layer. The parent assesses tool activity and results before adopting changes. Explain, Architect, Review, Implement, Setup, and the README now use Delegate.

This supersedes the host-selection finding in [the stack review](2026-09-13-review-consolidated-stack.md) and implements the agreed direction following [the delegation design review](2026-09-13-review-delegate-design.md). Earlier logbook accounts retain their historical text; only moved links were repaired.

At the user's request, the parent applied Unslop to the changed skill text and references. Removed repeated instructions, shortened setup and follow-up wording, and kept test-specific permission evidence here rather than in reusable guidance. Preserved defaults, read-only boundaries, resume behavior, model selection, inline evaluation, and Explain's visual examples. No launcher or configuration behavior changed in this wording pass.

## Result

The stack still has 12 skills. Configuration chooses models; Delegate chooses execution. Evaluation can use inline variants and new roles without changing production assignments. The user approved committing and pushing after the wording pass. The installed plugin cache was not updated.

## Verification and gaps

Repository validation passed: 17 model tests, 20 launcher tests, one repository validation test, manifests, presets, links, hygiene, and Logbook layout. The seven affected skills passed the bundled skill validator. Launcher tests cover stdin, permissions on fresh/resumed calls, session IDs, failures, provenance, and process monitoring.

Live mechanics checks used the configured smoke assignments: Luna low with Fast requested, and Haiku low. Production settings were unchanged. Native Luna low was an explicit smoke substitution; the spawn tool did not expose Fast. These runs do not establish production-model quality.

| Check | Observed result |
| --- | --- |
| Native Luna, read-only and follow-up | Read the fixture, returned three items and the last item's initial on follow-up; no further agents. |
| External Haiku, read-only and resume | Read the fixture and recalled a marker in the same conversation. Reported four lines by counting the tool's displayed trailing empty line; the file contained three newline-terminated items. |
| External Luna, edits and resume | Created only the assigned result file, then recalled and appended its marker. Original fixture unchanged. Both enabled write flags were reapplied. |
| Inline Haiku scenario with delegation enabled | Launched a native Haiku child with the exact no-further-agents instruction and read-only scope. Child returned three nonempty items and the correct last item. No skill or config file was installed. |
| Inline Luna scenario delegating externally to Haiku | Outer process used Delegate with default child restrictions. Inner Claude failed on session storage/authentication inside the Codex sandbox. Outer reported the failure accurately. This path remains blocked in the tested environment. |
| External Haiku with writes enabled | Attempted the assigned Write call, but Claude's permission layer denied it. No result file was created. The process exited successfully while reporting the permission request; the task did not complete. No permission bypass or retry was attempted. |

Verified served external models were `gpt-5.6-luna` and `claude-haiku-4-5-20251001`. Codex rollout verified effort; Claude effort and Codex Fast remain requested settings. The nested native Haiku tool accepted a model but exposed no effort field. The failed nested external Claude run did not establish a served model.

External conversation IDs for follow-up: Haiku read/resume `43130b43-286b-4f36-b105-ad0de247f62e`; Luna edit/resume `01a09b4f-4105-78d0-bd53-998ca7cca703`; inline Luna `01a09b50-c300-7a32-94d6-3f0f03ea96f5`; inline Haiku `859a0abc-52d2-4c33-b239-6a86b7b731ba`; blocked Haiku writer `a279e866-136f-4d57-8669-8dbeed1b2274`.

Both permission gaps are documented in Delegate's provider references. The parent checked files and tool records rather than treating process success as task completion. Temporary fixtures and launcher artifacts were removed after recording evidence; provider conversations remain resumable.
