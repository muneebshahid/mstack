---
name: setup-mstack
description: "Configure MStack's per-role models, efforts, runners, and Fast settings for the current harness. Use for first-time setup in Codex or Claude Code, inspecting effective assignments, switching between the codex-multimodel and claude-multimodel profiles, or changing model choices."
---

# Setup MStack

Configure the models MStack uses without editing installed skills. Repository profiles supply complete defaults; the user-owned `~/.config/mstack/models.toml` selects one profile and stores only explicit overrides.

## Authority

This skill may inspect MStack's packaged configuration and available model metadata. Write the user configuration only when the user asks to set up or change MStack. Do not install models, change provider accounts, alter project files, or probe a paid model merely to infer entitlement.

## Inspect current state

Resolve this skill's directory and run:

```bash
python3 <setup-mstack-directory>/scripts/models.py profiles
python3 <setup-mstack-directory>/scripts/models.py resolve
```

The resolver reads `MSTACK_CONFIG` when set, then `$XDG_CONFIG_HOME/mstack/models.toml` when set, otherwise `~/.config/mstack/models.toml`. A missing user file is normal: the resolver detects the host and selects that host's packaged profile. Claude Code is detected through the `CLAUDECODE` environment variable; anything else is treated as Codex. `MSTACK_HOST=codex` or `MSTACK_HOST=claude-code` overrides detection.

MStack ships one profile per host:

- `codex-multimodel`: Codex-led. Native GPT roles do the work; the external `claude-code` launcher supplies independent Claude judgment.
- `claude-multimodel`: Claude Code-led. Native Claude roles do the work; the external `codex` launcher supplies independent GPT judgment.

Using the other host's profile fails at launch because its native runner does not exist here. Offer it only when the user explicitly wants it, and say why it will not run.

## Confirm capabilities

Enumerate model identifiers from the current harness's callable native-agent schema or a provider command that reports the user's available models. Check required runners as well as model names:

- `codex-native` needs the Codex host. `claude-native` needs the Claude Code host.
- `claude-code` means MStack's sibling `claude-code` skill and `scripts/run_claude.py`; its executable is `CLAUDE_CODE_BIN` when set, otherwise `claude`. Do not look for a binary named `claude-code`.
- `codex` means MStack's sibling `codex` skill and `scripts/run_codex.py`; its executable is `CODEX_BIN` when set, otherwise `codex`. It also needs a writable Codex home (`CODEX_HOME` or `~/.codex`) because served-model provenance is read from the session rollout.

Check that the external CLI for the selected profile is on `PATH` and logged in (`codex login status` or `claude auth status`). Report a missing or unauthenticated CLI as a capability gap for every role that uses it, and tell the user how to install or log in. Do not silently move those roles to the native runner.

Do not treat a packaged default, documentation example, or successful authentication as proof that a model is available. When entitlement cannot be inspected without running an expensive model, ask the user to confirm the exact identifier. If a launch probe is useful and authorized, use the cheapest suitable model: Luna `low` with Fast for Codex mechanics and Haiku `low` for Claude mechanics. Do not run a Haiku probe in Claude plan mode because the harness may route planning to a larger model. Verify served-model provenance. A cheap probe validates the runner, not a different production model.

Show the selected profile's full effective mapping. Mark any unconfirmed model or runner and ask the user whether to accept the available mapping or change specific roles. Never silently replace an unavailable assignment.

## Write configuration

Create the whole user configuration idempotently with the bundled script. Use one `--set ROLE.FIELD=VALUE` argument per override:

```bash
python3 <setup-mstack-directory>/scripts/models.py configure \
  --profile claude-multimodel \
  --set how_simple_explainer.effort=low
```

Supported assignment fields are `runner`, `model`, `effort`, and `fast`. Effort is one of `low`, `medium`, `high`, `xhigh`, or `max`. Fast is a boolean and is valid only for the `codex-native` and `codex` runners. `implement_worker` must use a native runner.

Before overwriting an existing user file, show the effective current mapping and the proposed mapping. If the user gave exact choices in the active request, that request is sufficient confirmation; otherwise obtain confirmation after resolving ambiguities. Do not preserve unknown keys or malformed values by copying them into the replacement.

## Verify

Run `models.py resolve` after writing. Confirm:

- The detected host and selected profile.
- Every effective role assignment.
- Every user override.
- Any runner or entitlement that remains unverified.

Configuration takes effect the next time an orchestrating skill resolves its roles. It does not require modifying the managed plugin cache. Report the written path and never print credentials or provider tokens.
