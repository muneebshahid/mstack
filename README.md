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
- `why` can use installed source connectors such as Linear. Those integrations are deliberately not bundled here.
- Native multi-agent workflows require the selected host to expose subagent spawn, wait, message, and close operations.

Model slugs and effort levels in the selected profile describe the requested topology. If a host does not offer one, the workflow must report the capability gap rather than claim that the requested model ran.

## Workflow map

| Skill | Purpose | Agent flow |
| --- | --- | --- |
| `implement` | Single entry point for feature, bug-fix, refactoring, and prototype code changes | Parent scopes and verifies; one persistent configured worker writes small, verifiable units |
| `architect` | Read-only architecture for consequential changes | Grounds the system, selects principles, invokes `arena`, and returns a design and invalidation criteria to `implement` |
| `arena` | Competing designs for consequential artifacts | Two configured candidates work independently; a configured cross-judge advises; parent selects and synthesizes |
| `how` | Explain current mechanics and architecture | Uses configured explorer, explainer, and optional critic roles according to complexity and mode |
| `why` | Reconstruct design rationale from evidence | One configured investigator per available source; a configured synthesizer reconciles evidence; parent verifies and presents |
| `interrogate` | Adversarial multi-model code review | Two configured reviewers work independently; parent verifies, deduplicates, and categorizes findings |
| `skill-eval` | Test an existing skill or compare it with a proposed revision | Disposable scenarios and a configured blinded judge; dedicated cheap assignments are used only for execution smoke tests |
| `teach` | Explain what something is, how it works, and why | Composes `how` and `why` into one account |
| `apply-principles` | Select engineering standards for a broad task | Routes to the smallest relevant set of canonical `principle-*` leaves |
| `logbook` | Preserve durable engineering decisions | Records rationale, alternatives, evidence, consequences, and revisit conditions in `.agents/logbook/` |

## Focused skills

- `bro`: explicitly restate the immediately preceding answer in shorter, plain language.
- `claude-code`: reusable process boundary for an independent Claude consultant or judge, used from Codex.
- `codex`: the reciprocal boundary for an independent Codex consultant or judge, used from Claude Code.
- `grill-me`: explicitly pressure-test a loose idea in decision-tree rounds before planning or implementation.
- `setup-mstack`: detect the host, select a profile, validate available runners and models, and write user-owned role overrides.
- `gh-address-comments`: inspect and address all GitHub review comments unless the user narrows the scope.
- `tdd`: focused red-green bug-fix workflow when a cheap, meaningful regression test exists.
- `test-coverage-auditor`: judge whether changed behavior has appropriate tests, not merely coverage.
- `typescript-best-practices`: TypeScript-specific type, API, module, and runtime-boundary guidance.
- `technical-writing`: Diátaxis, developer style, simplified technical English, and ambiguity control.
- `teach`: combine mechanics and rationale at the reader's pace.
- `unslop`: remove generic AI prose patterns without changing facts or requested voice.

## Engineering principles

The `principle-*` skills are canonical leaves. Workflows load only the leaves triggered by the task.

- Structure: boundary discipline, clear ownership, dependency direction, domain modeling, and separation before serializing shared state.
- Simplicity: minimize reader load, subtract before adding, redesign from first principles, and migrate callers before deleting legacy APIs.
- Correctness: fix root causes, prove the real artifact works, use type-system discipline, and make retryable operations idempotent.
- Execution: sequence verifiable units, optimize for the intended outcome, build small automation levers, and encode recurring lessons in structure.
- Product and design: put experience first and exhaust the design space when consequential choices have multiple viable shapes.
- Source style: completed owned source contains no human-authored comments; temporary architecture scaffolds may use `TODO` comments or pseudocode until implementation fills them.

## Repository decisions

Durable decisions live in [`.agents/logbook/`](.agents/logbook/). The first records reconstruct the major decisions that produced this stack. Future changes should update the relevant record or add a new one when they change architecture, behavior, process, testing policy, or a costly-to-reverse convention.

## Origins and licensing

This stack adapts and extends work from Cursor's [PStack](https://github.com/cursor/plugins/tree/main/pstack) and draws workflow inspiration from Jesse Vincent's [Superpowers](https://github.com/obra/superpowers). See [THIRD_PARTY.md](THIRD_PARTY.md) and the per-skill license files.

MStack is available under the MIT License. Upstream-derived material remains subject to its preserved upstream notices; see [THIRD_PARTY.md](THIRD_PARTY.md).
