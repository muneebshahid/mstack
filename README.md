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

Setup offers `codex-preset` and `claude-preset` with optional role customization. Your active profile combines the selected preset and overrides in `~/.config/mstack/models.toml`. Defaults live in [`config/presets/`](config/presets/).

The scripts require Python 3.12+. External delegation requires the model's CLI installed and logged in; Skill Eval always uses an external CLI. GitHub workflows require `gh`. Explain can use connected sources such as Linear and service logs when available.

## Skills

| Skill | What it does |
| --- | --- |
| [implement](skills/implement/SKILL.md) | Make and verify changes directly or with a persistent worker; add tests where they provide useful protection. |
| [architect](skills/architect/SKILL.md) | Design consequential changes and compare alternatives when useful. Read-only. |
| [explain](skills/explain/SKILL.md) | Explain behavior, decisions, and changes using relevant sources, a consistent template, and useful visuals. |
| [grill-me](skills/grill-me/SKILL.md) | Clarify what to build and deepen understanding through questions, explanations, and useful diagrams. |
| [review](skills/review/SKILL.md) | Review correctness, simplicity, and test usefulness, directly or with independent reviewers. Read-only. |
| [apply-principles](skills/apply-principles/SKILL.md) | Select relevant engineering standards, including simplicity, strong types, ownership, diagnosis, and verification. |
| [logbook](skills/logbook/SKILL.md) | Record each commit’s work, decisions, rejected approaches, and verification. |
| [delegate](skills/delegate/SKILL.md) | Run scoped tasks natively or through an external harness, with explicit permissions and resumable follow-ups. |
| [setup-mstack](skills/setup-mstack/SKILL.md) | Select a preset, customize role models, and check availability. |
| [skill-eval](skills/skill-eval/SKILL.md) | Compare inline skill variants in fresh external scenarios before adopting changes. |
| [unslop](skills/unslop/SKILL.md) | Remove generic AI wording while preserving meaning. |
| [bro](skills/bro/SKILL.md) | Restate the preceding answer in shorter, plain language. |

MIT licensed. Upstream credits and licenses are listed in [THIRD_PARTY.md](THIRD_PARTY.md).
