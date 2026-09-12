# MStack

An opinionated engineering skill stack for Codex and Claude Code. It combines small, reusable engineering principles with explicit workflows for investigation, architecture, implementation, review, evaluation, and technical communication.

The stack is designed around one rule: the parent agent keeps lead-engineer judgment. Specialist agents gather evidence, produce alternatives, write bounded implementation units, or challenge a result. They do not silently take over the final decision.

## Install in Codex

Add the repository marketplace and install MStack:

```text
codex plugin marketplace add muneebshahid/mstack
codex plugin add mstack@mstack
```

Start a new task after installation so Codex loads the plugin catalog. The official OpenAI plugin-directory submission is pending.

## Install in Claude Code

Add the repository marketplace, then install MStack:

```text
/plugin marketplace add muneebshahid/mstack
/plugin install mstack@mstack
```

Start a new Claude Code session after installation.

To verify the repository before publishing or installing it, run:

```bash
python3 scripts/validate.py
```

The same validation runs in GitHub Actions. Marketplace installation tests remain explicit release checks because they require the Codex or Claude Code CLI and network access.

## Configure models

Run `$setup-mstack` in Codex or `/mstack:setup-mstack` in Claude Code. MStack ships one complete profile per host:

- `codex-multimodel`: Codex-led. Native GPT workers, with the external `claude-code` launcher supplying independent Claude judgment.
- `claude-multimodel`: Claude Code-led. Native Claude workers, with the external `codex` launcher supplying independent GPT judgment.

Without a user configuration, the resolver detects the host and uses that host's profile, so a fresh install works in either harness. Packaged defaults live in [`config/`](config/). User choices live in `~/.config/mstack/models.toml`; managed plugin files are never rewritten. Orchestrating skills resolve their role assignments when invoked, so a configuration change applies to the next workflow run. Invalid or unavailable assignments fail visibly instead of falling back to another model.

Cross-vendor roles need the other CLI installed and logged in: `claude` for `codex-multimodel`, `codex` for `claude-multimodel`. Setup checks for it and reports the gap for the affected roles.

To inspect or install one skill without the plugin, use its directory under `https://github.com/muneebshahid/mstack/tree/main/skills/`.

Some workflows have optional external dependencies:

- `claude-code` requires the Claude Code CLI and a requested Claude model that the account can serve.
- `codex` requires the Codex CLI and a requested GPT model that the account can serve.
- GitHub evidence and PR workflows require the `gh` CLI.
- `explain` can use project-declared source connectors such as Linear. Those integrations are deliberately not bundled here.
- Native multi-agent workflows require the selected host to expose subagent spawn, wait, message, and close operations.

Model slugs and effort levels in the selected profile describe the requested topology. If a host does not offer one, the workflow must report the capability gap rather than claim that the requested model ran.

When upgrading from separate How/Why workflows, remove retired `how_*` and `why_*` overrides from your model configuration. Explain handles simple questions directly and uses one or two native `explain_explorer` agents when exploration benefits from delegation: Luna at `max` effort on Codex, Sonnet at `high` on Claude Code. Optional independent judgment uses `consultant_default`.

Interrogate is now `review`. Rename any `interrogate_reviewer_a` and `interrogate_reviewer_b` model overrides to `review_reviewer_a` and `review_reviewer_b`; their assignments are unchanged. Test Coverage Auditor is removed; Review checks coverage and test usefulness within the requested scope.

Arena is now an optional comparison method within Architect. Rename `arena_candidate_a` and `arena_candidate_b` overrides to `architect_candidate_a` and `architect_candidate_b`; assignments are unchanged. Remove `arena_cross_judge` overrides; optional judgment uses `consultant_default`. Grill Me is removed.

## Workflow map

| Skill | Purpose | Agent flow |
| --- | --- | --- |
| `implement` | Single entry point for feature, bug-fix, refactoring, and prototype code changes | Parent scopes and verifies; one persistent configured worker writes small, verifiable units |
| `architect` | Read-only design for consequential changes | Parent designs directly or compares independent proposals, then returns the design and implementation handoff |
| `explain` | Explain mechanics, rationale, and changes | Parent investigates and answers in a consistent template; optional consulting for bounded questions |
| `review` | Review code, designs, simplicity, and test usefulness | Two configured reviewers for adversarial review; focused reviews can run directly; parent verifies findings and proposed remedies |
| `skill-eval` | Test an existing skill or compare it with a proposed revision | Disposable scenarios and a configured blinded judge; dedicated cheap assignments are used only for execution smoke tests |
| `apply-principles` | Select engineering standards for a broad task | Routes to the smallest relevant set of canonical reference documents |
| `logbook` | Preserve non-trivial work and meaningful investigation outcomes | Records work, accepted and rejected reasoning, verification, and gaps in `.agents/logbook/` |

## Focused skills

- `bro`: explicitly restate the immediately preceding answer in shorter, plain language.
- `claude-code`: reusable process boundary for an independent Claude consultant or judge, used from Codex.
- `codex`: the reciprocal boundary for an independent Codex consultant or judge, used from Claude Code.
- `setup-mstack`: detect the host, select a profile, validate available runners and models, and write user-owned role overrides.
- `gh-address-comments`: inspect and address all GitHub review comments unless the user narrows the scope.
- `tdd`: focused red-green bug-fix workflow when a cheap, meaningful regression test exists.
- `typescript-best-practices`: TypeScript-specific type, API, module, and runtime-boundary guidance.
- `technical-writing`: Diátaxis, developer style, simplified technical English, and ambiguity control.
- `unslop`: remove generic AI prose patterns without changing facts or requested voice.

## Engineering principles

The canonical engineering standards live in ten references under [`skills/apply-principles/references/`](skills/apply-principles/references/). [`apply-principles`](skills/apply-principles/SKILL.md) selects only the references triggered by the task:

- [Simplicity](skills/apply-principles/references/simplicity.md)
- [Modeling and Types](skills/apply-principles/references/modeling-and-types.md)
- [Ownership and Contracts](skills/apply-principles/references/ownership-and-contracts.md)
- [Concurrency and Retries](skills/apply-principles/references/concurrency-and-retries.md)
- [Delivery and Migration](skills/apply-principles/references/delivery-and-migration.md)
- [Diagnosis](skills/apply-principles/references/diagnosis.md)
- [Verification](skills/apply-principles/references/verification.md)
- [Design Decisions](skills/apply-principles/references/design-decisions.md)
- [Automation and Learning](skills/apply-principles/references/automation-and-learning.md)
- [Source Style](skills/apply-principles/references/source-style.md)

## Repository decisions

Records live in [`.agents/logbook/`](.agents/logbook/). The first records reconstruct the major decisions that produced this stack. Every non-trivial change adds or updates a relevant record; meaningful investigation and review outcomes belong there too, including rejected suggestions and their evidence. [Logbook](skills/logbook/SKILL.md) defines the mechanical/local exemptions and parent authorship.

## Origins and licensing

This stack adapts and extends work from Cursor's [PStack](https://github.com/cursor/plugins/tree/main/pstack) and draws workflow inspiration from Jesse Vincent's [Superpowers](https://github.com/obra/superpowers). See [THIRD_PARTY.md](THIRD_PARTY.md) and the per-skill license files.

MStack is available under the MIT License. Upstream-derived material remains subject to its preserved upstream notices; see [THIRD_PARTY.md](THIRD_PARTY.md).
