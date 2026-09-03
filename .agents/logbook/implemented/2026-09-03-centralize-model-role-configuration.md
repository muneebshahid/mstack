# Logbook: Centralize Model Role Configuration

Status: implemented
Kind: architecture

## Problem

Orchestration skills embedded model slugs, effort levels, Fast settings, and launcher choices in their prose. Changing one model required editing several skills, made installed managed copies tempting to patch, and prevented one shared package from expressing Codex-only, Claude-only, and mixed topologies cleanly.

## Decision

MStack owns model selection through named semantic roles. `config/models.defaults.toml` defines the schema and role registry. Complete packaged profiles live in `config/profiles/`, with `multimodel` as the default and `codex` and `claude-code` as native-only alternatives.

User state lives outside the managed plugin at `~/.config/mstack/models.toml`, or the path selected by `MSTACK_CONFIG` or `XDG_CONFIG_HOME`. It selects one profile and contains only explicit per-role overrides. `skills/setup-mstack/scripts/models.py` validates and resolves packaged defaults plus user overrides. Orchestrating skills resolve their roles at invocation and never silently replace an unavailable runner, model, effort, or service tier.

`setup-mstack` owns the user journey: inspect current assignments, establish which models and runners are actually available, show changes, write the complete user file idempotently, and verify the effective result. Execution smoke tests use dedicated cheap roles rather than changing production assignments.

## Alternatives considered

- Keep inline defaults in every workflow. Rejected because repeated model choices drift and require skill edits for user preferences.
- Rewrite files in the installed plugin cache during setup. Rejected because package updates replace managed copies and local mutations are difficult to audit.
- Inject one harness-specific always-applied rule. Rejected because Codex and Claude Code do not share one portable global-rule mechanism and workflows still need deterministic field validation.
- Add an MCP server solely for configuration. Rejected because local TOML and a standard-library resolver provide the required persistence without a service boundary.
- Silently choose another model when a configured assignment fails. Rejected because it destroys provenance and can invalidate multi-model independence.

## Evidence

- `config/models.defaults.toml`
- `config/profiles/multimodel.toml`
- `config/profiles/codex.toml`
- `config/profiles/claude-code.toml`
- `skills/setup-mstack/SKILL.md`
- `skills/setup-mstack/scripts/models.py`
- `skills/setup-mstack/scripts/test_models.py`
- `skills/setup-mstack/references/runtime-resolution.md`

All three profiles resolve, partial overrides preserve unspecified fields, invalid roles and unsupported Fast combinations fail, and configuration writes are validated before replacement. A Luna low/Fast read-only smoke run loaded `setup-mstack`, executed profile resolution, and caught and then verified a correction to external Claude runner detection. Clean Codex and Claude Code marketplace installations of version `0.2.0` both contained the packaged profiles and successfully resolved roles from their managed cache paths.

A Claude Code plan-mode smoke run loaded `mstack:setup-mstack` and located the packaged resolver, but the requested `haiku` alias was served as `claude-sonnet-5`. Follow-up non-plan runs verified `claude-haiku-4-5` provenance and the same skill-loading path, but their deliberately narrow Bash allowlists denied the resolver commands when Claude alternated between absolute and relative paths. No broader permission was granted. Claude resolver execution therefore remains a named validation gap rather than a claimed pass.

## Consequences

Workflows gain one source of model truth and users can change a role without forking MStack. Every orchestration launch now incurs one small local resolution step. Profiles must remain complete and versioned with the role registry. Harness support depends on real runner capabilities; configuration can describe a role but cannot manufacture an unavailable model or native-agent API.

## Revisit when

- Either harness provides a portable native user-configuration mechanism that can replace local resolution without splitting the package.
- Role count grows enough that users cannot understand the effective mapping during setup.
- A harness cannot dynamically express the configured model or effort for native subagents.
- Repeated evidence shows the native-only profiles do not preserve useful model diversity.
