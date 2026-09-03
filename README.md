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

Start a new Claude Code session after installation. Claude-specific runtime validation is still in progress; the current orchestration defaults describe the Codex runtime.

To inspect or install one skill without the plugin, use its directory under `https://github.com/muneebshahid/mstack/tree/main/skills/`.

Some workflows have optional external dependencies:

- `claude-code` requires Claude Code and a requested Claude model that the account can serve.
- GitHub evidence and PR workflows require the `gh` CLI.
- `why` can use installed source connectors such as Linear. Those integrations are deliberately not bundled here.
- Native multi-agent workflows require a Codex host that exposes subagent spawn, wait, message, and close operations.

Model slugs and effort levels describe the current preferred topology. If a host does not offer one, the workflow must report the capability gap rather than claim that the requested model ran.

## Workflow map

| Skill | Purpose | Agent flow |
| --- | --- | --- |
| `implement` | Single entry point for feature, bug-fix, refactoring, and prototype code changes | Parent scopes and verifies; one persistent GPT-5.6 Luna `high` Fast worker writes small, verifiable units |
| `architect` | Read-only architecture for consequential changes | Grounds the system, selects principles, invokes `arena`, and returns a design and invalidation criteria to `implement` |
| `arena` | Competing designs for consequential artifacts | Fable 5.1 `xhigh` and Sol `xhigh` produce independent candidates; Sol `xhigh` cross-judges; parent selects and synthesizes |
| `how` | Explain current mechanics and architecture | Simple: Sol `medium`; complex: Luna `xhigh` Fast explorers followed by Sol `high`; critique adds Fable 5.1 `xhigh` and Sol `xhigh` |
| `why` | Reconstruct design rationale from evidence | One Luna `xhigh` Fast investigator per available source; Fable 5.1 `xhigh` synthesizes; parent verifies and presents |
| `interrogate` | Adversarial multi-model code review | Fable 5.1 `max` and Sol `max` review independently; parent verifies, deduplicates, and categorizes findings |
| `skill-eval` | Test an existing skill or compare it with a proposed revision | Disposable scenarios and a blinded Claude judge; cheap Luna/Haiku substitutions are allowed only for execution smoke tests |
| `teach` | Explain what something is, how it works, and why | Composes `how` and `why` into one account |
| `apply-principles` | Select engineering standards for a broad task | Routes to the smallest relevant set of canonical `principle-*` leaves |
| `logbook` | Preserve durable engineering decisions | Records rationale, alternatives, evidence, consequences, and revisit conditions in `.agents/logbook/` |

## Focused skills

- `claude-code`: reusable process boundary for an independent Claude consultant or judge.
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
