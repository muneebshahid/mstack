# Logbook: Centralize Model Role Configuration

Status: implemented
Kind: architecture

## Problem

Orchestration skills embedded model slugs, effort levels, Fast settings, and launcher choices in their prose. Changing one model required editing several skills, made installed managed copies tempting to patch, and prevented one shared package from expressing Codex-only, Claude-only, and mixed topologies cleanly.

## Decision

MStack owns model selection through named semantic roles. `config/models.defaults.toml` defines the schema, the role registry, and one default preset per host. Complete packaged presets live in `config/presets/`: `codex-preset` and `claude-preset`. The active profile combines a selected preset with user overrides. Execution roles use the host's native runner; judgment roles can use native agents or external consultants. The resolver detects the host from the `CLAUDECODE` environment variable, overridable with `MSTACK_HOST`, so a fresh install resolves without a user file. Runners are `codex-native`, `claude-native`, `claude-code`, and `codex`; the two external launchers are read-only and are rejected for `implement_worker`.

User state lives outside the managed plugin at `~/.config/mstack/models.toml`, or the path selected by `MSTACK_CONFIG` or `XDG_CONFIG_HOME`. It selects a `preset` and contains only explicit per-role overrides. `skills/setup-mstack/scripts/models.py` validates and resolves packaged defaults plus user overrides. Orchestrating skills resolve their roles at invocation and never silently replace an unavailable runner, model, effort, or service tier.

`setup-mstack` owns inspection, requested configuration changes, and verification. Its shortened entry point links to one runtime reference for configuration locations, host detection, and runner selection; Consult owns external launch details. Execution smoke tests use dedicated cheap roles rather than changing production assignments. Unknown model availability is reported without requiring another confirmation. The configure command replaces the user file, so callers include existing overrides they intend to retain and can preview with `--dry-run`.

## Alternatives considered

- Keep inline defaults in every workflow. Rejected because repeated model choices drift and require skill edits for user preferences.
- Ship single-vendor `codex` and `claude-code` profiles alongside the mixed ones. Rejected because they give up the model diversity the review workflows depend on, and a user who wants one vendor can override the few cross-vendor roles.
- One global default profile regardless of host. Rejected because the Codex-led profile cannot run under Claude Code and vice versa; a fresh install must work without setup.
- Rewrite files in the installed plugin cache during setup. Rejected because package updates replace managed copies and local mutations are difficult to audit.
- Inject one harness-specific always-applied rule. Rejected because Codex and Claude Code do not share one portable global-rule mechanism and workflows still need deterministic field validation.
- Add an MCP server solely for configuration. Rejected because local TOML and a standard-library resolver provide the required persistence without a service boundary.
- Repeat launcher behavior and fixed confirmation steps in setup prose. Removed during simplification because Consult owns the launcher and explicit user choices already authorize configuration changes.
- Silently choose another model when a configured assignment fails. Rejected because it destroys provenance and can invalidate multi-model independence.

## Evidence

- `config/models.defaults.toml`
- `config/presets/codex-preset.toml`
- `config/presets/claude-preset.toml`
- `skills/setup-mstack/SKILL.md`
- `skills/setup-mstack/scripts/models.py`
- `skills/setup-mstack/scripts/test_models.py`
- `skills/setup-mstack/references/runtime-resolution.md`

Both profiles resolve, each host detects its own default and `MSTACK_HOST` overrides it, a user profile wins over the host default, partial overrides preserve unspecified fields, invalid roles, unsupported Fast combinations, and an external runner on `implement_worker` fail, and configuration writes are validated before replacement. A Luna low/Fast read-only smoke run loaded `setup-mstack`, executed profile resolution, and caught and then verified a correction to external Claude runner detection. Clean Codex and Claude Code marketplace installations of version `0.2.0` both contained the packaged profiles and successfully resolved roles from their managed cache paths.

A Claude Code execution smoke ran from a disposable plugin copy with the `haiku` alias at `low` effort. Claude served `claude-haiku-4-5-20251001`, invoked `mstack:setup-mstack`, executed the packaged resolver for the Codex-led profile's `implement_worker` role, and returned the configured `codex-native`, `gpt-5.6-luna`, `high`, and Fast assignment. A complete before-and-after content hash confirmed that the disposable plugin tree was unchanged. An earlier `auto`-permission attempt stopped at an approval request and was not counted as execution evidence; the passing run used permission bypass only inside the disposable test boundary.

The external `codex` runner originated in [Codex Runs as an Independent Consultant](2026-09-03-codex-as-independent-consultant.md); [Consult](2026-09-12-consolidate-resumable-consultation.md) now owns both external launchers.

The parent simplified Setup MStack and its runtime reference, removed repeated permission and confirmation instructions, and checked the replacement-file semantics against the existing script. Resolving both current profiles found no local override file, and both installed profile files matched the repository versions. That prose-only pass left model defaults, resolver code, user configuration, and invocation policy unchanged. Skill validation, configuration resolution, Markdown links, repository hygiene, and Logbook validation passed. No paid model probes or user configuration writes were needed.

The user then renamed the packaged choices to presets and requested new defaults. Codex implementation uses Luna `max` with Fast off. Both Architect B and Reviewer B use Astra at `xhigh` and `max`, respectively. The quality judge is native Astra `medium` on Codex and native Fable `medium` on Claude. Claude's default external consultant is Astra `xhigh`. Other assignments remain unchanged, including cheap smoke roles. Setup now offers a preset or role customization; runtime and CLI terminology use `preset`, `presets`, and `--preset`. The resolver rejects the old user `profile` key with a migration message rather than ignoring it. No local user file existed to migrate, and installed plugin caches were not edited. All 13 model tests and repository validation passed. A disposable configuration exercised preset selection, a saved role override, and the merged active profile; a separate resolver check verified every requested assignment. Temporary verification files were removed. No paid models were launched.

A fresh native Luna `low` agent subsequently installed the public GitHub marketplace and plugin at commit `bf4dca5` into isolated Codex and configuration directories, read the installed Setup MStack skill and runtime reference, previewed and saved `codex-preset` without overrides, and resolved all ten assignments. The parent compared eight installed source files with the pushed commit and confirmed the resolved roles exactly matched the installed preset. All 13 installed model tests passed. The external Claude executable was available and authenticated. The isolated Codex home had no login; no credentials were copied and no paid model launches were attempted. The native agent API could not request the smoke role's Fast tier, so that setting remains unverified. This establishes fresh installation and explicitly loaded setup execution, not automatic skill discovery or model availability. Existing user configuration and MStack cache hashes were unchanged. The parent closed the agent and removed the disposable installation and evidence after recording the result.

## Consequences

Workflows gain one source of model truth and users can change a role without forking MStack. Every orchestration launch now incurs one small local resolution step. Presets must remain complete and versioned with the role registry. Harness support depends on real runner capabilities; configuration can describe a role but cannot manufacture an unavailable model or native-agent API.

## Revisit when

- Either harness provides a portable native user-configuration mechanism that can replace local resolution without splitting the package.
- Role count grows enough that users cannot understand the effective mapping during setup.
- A harness cannot dynamically express the configured model or effort for native subagents.
- Users repeatedly ask for a packaged single-vendor profile instead of overriding the cross-vendor roles.
- A third harness or vendor needs a profile, which would strain host detection by environment variable.
