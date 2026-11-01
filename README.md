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

Setup offers `codex-preset` and `claude-preset` with optional role customization. Each harness keeps its own profile, the selected preset plus overrides, in `~/.config/mstack/profiles/claude-code.toml` or `~/.config/mstack/profiles/codex.toml`. Run setup in each harness you use. Defaults live in [`config/presets/`](config/presets/).

The scripts require Python 3.12+. External delegation requires the model's CLI installed and logged in. GitHub workflows require `gh`.

## Skills

| Skill | What it does |
| --- | --- |
| [implement](skills/implement/SKILL.md) | Make and verify changes in the running agent. |
| [architect](skills/architect/SKILL.md) | Design consequential changes and compare alternatives when useful. Read-only. |
| [show-me](skills/show-me/SKILL.md) | Explain the current topic visually with concise diagrams, code-shape sketches, and focused HTML files. |
| [grill-me](skills/grill-me/SKILL.md) | Clarify what to build and deepen understanding through questions, explanations, and useful diagrams. |
| [review](skills/review/SKILL.md) | Review correctness, simplicity, and test usefulness, directly or with independent reviewers. Read-only. |
| [apply-principles](skills/apply-principles/SKILL.md) | Select relevant engineering standards, including simplicity, strong types, and ownership. |
| [logbook](skills/logbook/SKILL.md) | Record decisions, incidents, and investigations that future agents would need. |
| [delegate](skills/delegate/SKILL.md) | Run scoped tasks natively or through an external harness, with explicit permissions and resumable follow-ups. |
| [setup-mstack](skills/setup-mstack/SKILL.md) | Select a preset, customize role models, and check availability. |
| [unslop](skills/unslop/SKILL.md) | Remove generic AI wording while preserving meaning. |
| [bro](skills/bro/SKILL.md) | Restate the preceding answer in shorter, plain language. |

MIT licensed. Upstream credits and licenses are listed in [THIRD_PARTY.md](THIRD_PARTY.md).
