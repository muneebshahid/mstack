# Logbook: Package Explicit Conversation Utilities

Status: implemented
Kind: behavior

## Problem

`bro` and `grill-me` existed as standalone personal skills, so they were unavailable to other MStack users and would collide with managed copies after marketplace installation. The standalone `grill-me` was only an alias to an absent `grilling` skill and therefore did not carry its own interview behavior.

## Decision

MStack packages `bro` and `grill-me` as explicit-only conversation utilities. `bro` restates only the assistant's immediately preceding message without adding claims. `grill-me` keeps its design-tree, frontier-round, recommendation, factual-investigation, and user-decision boundaries, but folds the upstream `grilling` primitive into one self-contained skill. It writes no files and does not plan or implement until the user separately requests that work after confirming shared understanding.

## Alternatives considered

- Package the two-line `grill-me` alias and add a third public `grilling` skill. Rejected because the extra discovery surface exists only to satisfy an internal indirection.
- Keep both utilities as personal skills. Rejected because MStack's managed installation is now the authoritative distribution path and duplicate names create ambiguous discovery.
- Allow automatic invocation. Rejected because both utilities deliberately alter the conversation mode and should run only when the user asks.

## Evidence

- `skills/bro/SKILL.md`
- `skills/grill-me/SKILL.md`
- `skills/bro/agents/openai.yaml`
- `skills/grill-me/agents/openai.yaml`
- `THIRD_PARTY.md`
- `LICENSES/MATT-POCOCK-SKILLS-MIT.txt`

Both skills pass structural validation as part of the complete MStack package. Their Codex metadata disables implicit invocation, while their shared descriptions and instructions preserve the explicit-only boundary in every harness without using frontmatter rejected by Codex's validator. A disposable Claude Code smoke served `claude-haiku-4-5-20251001`, explicitly invoked `mstack:grill-me`, returned one three-question frontier round with recommendations and a request for user decisions, performed no implementation, and left the plugin tree unchanged.

## Consequences

MStack installs both utilities consistently in Codex and Claude Code without a hidden skill dependency. The self-contained `grill-me` intentionally duplicates the small reusable interview primitive instead of exposing it as another independently discoverable skill.

## Revisit when

- Another MStack workflow needs the same interview primitive and duplication would result.
- Either harness provides a portable private-skill mechanism that avoids public discovery without inlining.
- Users demonstrate that automatic invocation is less surprising than the explicit conversation-mode boundary.
