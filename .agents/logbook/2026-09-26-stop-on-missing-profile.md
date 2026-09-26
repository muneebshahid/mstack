# Logbook: Stop delegation when role resolution fails

## Goal

Make delegation stop for Setup when the harness has no model profile, instead of launching with some other model.

## Work and decisions

Live tests used the installed 0.4.1 plugin with a temporary configuration folder that held only the legacy shared `models.toml`. Each `claude -p` session was asked to delegate a one-word task with the default role.

- Sonnet `medium` skipped role resolution entirely. It launched a native Agent with no model, so the child ran on Sonnet, the session's own model.
- Opus 5.5 `medium`, with reads blocked by the test's permissions, could not resolve the role and launched on harness defaults. It reported the gap.
- Opus 5.5 `medium`, with reads allowed, ran the resolver and got the legacy-file error. Instead of running Setup, it chose `--preset claude-preset` itself and launched `gpt-6-astra` `xhigh` through Codex. It reported this, but it was not the user's previous `codex-preset`.

There were two causes. First, Delegate linked to the resolution command in a reference file and did not say what to do on failure. Second, the runtime reference allowed `--preset` for "a scoped run", which Opus read as a fallback.

Delegate now includes the resolve command. It says to stop and run Setup if resolution fails, and never to launch with harness defaults or a preset the user did not choose. The runtime reference now limits `--preset` to inspection or a preset the user asked for.

## Result

A skill that needs a model assignment now stops and runs Setup when the harness has no profile. It does not guess a model. Skills that do not delegate are unaffected.

## Verification and gaps

- The same test reran with the repository copy loaded via `--plugin-dir`. Sonnet ran the resolver, invoked `mstack:setup-mstack`, and asked which preset to configure. Opus ran the resolver, read Setup and the legacy file, and stopped without launching, listing the `configure` command. Neither wrote a profile or launched a child.
- `scripts/validate.py` passed.
- All runs were non-interactive `claude -p` sessions, which cannot ask questions. Behavior in an interactive session and in Codex was not tested.
- Sonnet suggested the harness-matching preset without offering the legacy file's `codex-preset`, which Setup asks it to offer.
- `codex plugin marketplace upgrade mstack` alone refreshed the installed Codex copy to 0.4.1. Codex's generated prompt read skills from the 0.4.1 cache. This closes an open question from [the per-harness profile entry](2026-09-26-per-harness-profiles.md).
