# MStack

Engineering skills for Codex and Claude Code: understand systems, design changes, implement them, review results, and communicate clearly. The main agent keeps final judgment and delegates when useful.

## Setup

### Codex

```text
codex plugin marketplace add muneebshahid/mstack
codex plugin add mstack@mstack
```

Start a new task, then run `$setup-mstack`.

### Claude Code

```text
/plugin marketplace add muneebshahid/mstack
/plugin install mstack@mstack
```

Start a new session, then run `/mstack:setup-mstack`.

Setup selects the host's model profile and configures overrides in `~/.config/mstack/models.toml`. Defaults live in [`config/`](config/).

External consultants require the other CLI installed and logged in: Claude Code for Claude consultation, Codex for GPT consultation. GitHub workflows require `gh`. Explain can use connected sources such as Linear and service logs when available.

## Skills

| Skill | What it does |
| --- | --- |
| [implement](skills/implement/SKILL.md) | Make and verify changes directly or with a persistent worker; add tests where they provide useful protection. |
| [architect](skills/architect/SKILL.md) | Design consequential changes and compare alternatives when useful. Read-only. |
| [explain](skills/explain/SKILL.md) | Explain behavior, decisions, and changes using relevant sources, a consistent template, and useful visuals. |
| [review](skills/review/SKILL.md) | Review correctness, simplicity, and test usefulness, directly or with independent reviewers. Read-only. |
| [apply-principles](skills/apply-principles/SKILL.md) | Select relevant engineering standards, including simplicity, strong types, ownership, diagnosis, and verification. |
| [logbook](skills/logbook/SKILL.md) | Record work, accepted and rejected approaches, reasoning, and evidence. |
| [claude-code](skills/claude-code/SKILL.md) | Consult an external Claude model. |
| [codex](skills/codex/SKILL.md) | Consult an external GPT model. |
| [setup-mstack](skills/setup-mstack/SKILL.md) | Configure model assignments and check runner availability. |
| [skill-eval](skills/skill-eval/SKILL.md) | Evaluate skills with disposable scenarios and independent judgment. |
| [gh-address-comments](skills/gh-address-comments/SKILL.md) | Address comments on the current GitHub pull request. |
| [typescript-best-practices](skills/typescript-best-practices/SKILL.md) | Guide TypeScript types, APIs, modules, and runtime boundaries. |
| [unslop](skills/unslop/SKILL.md) | Remove generic AI wording while preserving meaning. |
| [bro](skills/bro/SKILL.md) | Restate the preceding answer in shorter, plain language. |

MIT licensed. Upstream credits and licenses are listed in [THIRD_PARTY.md](THIRD_PARTY.md).
