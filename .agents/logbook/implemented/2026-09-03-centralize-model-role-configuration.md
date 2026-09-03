# Logbook: Centralize Model Role Configuration

Status: implemented
Kind: architecture

## Problem

Orchestration skills embedded model slugs, effort levels, Fast settings, and launcher choices in their prose. Changing one model required editing several skills, made installed managed copies tempting to patch, and prevented one shared package from expressing Codex-only, Claude-only, and mixed topologies cleanly.

## Decision

MStack owns model selection through named semantic roles. `config/models.defaults.toml` defines the schema, the role registry, and one default profile per host. Complete packaged profiles live in `config/profiles/`: `codex-multimodel` for a Codex host and `claude-multimodel` for a Claude Code host. Each profile keeps execution on the host's native runner and sends judgment roles to the other vendor through an external launcher. The resolver detects the host from the `CLAUDECODE` environment variable, overridable with `MSTACK_HOST`, so a fresh install resolves without a user file. Runners are `codex-native`, `claude-native`, `claude-code`, and `codex`; the two external launchers are read-only and are rejected for `implement_worker`.

User state lives outside the managed plugin at `~/.config/mstack/models.toml`, or the path selected by `MSTACK_CONFIG` or `XDG_CONFIG_HOME`. It selects one profile and contains only explicit per-role overrides. `skills/setup-mstack/scripts/models.py` validates and resolves packaged defaults plus user overrides. Orchestrating skills resolve their roles at invocation and never silently replace an unavailable runner, model, effort, or service tier.

`setup-mstack` owns the user journey: inspect current assignments, establish which models and runners are actually available, show changes, write the complete user file idempotently, and verify the effective result. Execution smoke tests use dedicated cheap roles rather than changing production assignments.

## Alternatives considered

- Keep inline defaults in every workflow. Rejected because repeated model choices drift and require skill edits for user preferences.
- Ship single-vendor `codex` and `claude-code` profiles alongside the mixed ones. Rejected because they give up the model diversity the review workflows depend on, and a user who wants one vendor can override the few cross-vendor roles.
- One global default profile regardless of host. Rejected because the Codex-led profile cannot run under Claude Code and vice versa; a fresh install must work without setup.
- Rewrite files in the installed plugin cache during setup. Rejected because package updates replace managed copies and local mutations are difficult to audit.
- Inject one harness-specific always-applied rule. Rejected because Codex and Claude Code do not share one portable global-rule mechanism and workflows still need deterministic field validation.
- Add an MCP server solely for configuration. Rejected because local TOML and a standard-library resolver provide the required persistence without a service boundary.
- Silently choose another model when a configured assignment fails. Rejected because it destroys provenance and can invalidate multi-model independence.

## Evidence

- `config/models.defaults.toml`
- `config/profiles/codex-multimodel.toml`
- `config/profiles/claude-multimodel.toml`
- `skills/setup-mstack/SKILL.md`
- `skills/setup-mstack/scripts/models.py`
- `skills/setup-mstack/scripts/test_models.py`
- `skills/setup-mstack/references/runtime-resolution.md`

Both profiles resolve, each host detects its own default and `MSTACK_HOST` overrides it, a user profile wins over the host default, partial overrides preserve unspecified fields, invalid roles, unsupported Fast combinations, and an external runner on `implement_worker` fail, and configuration writes are validated before replacement. A Luna low/Fast read-only smoke run loaded `setup-mstack`, executed profile resolution, and caught and then verified a correction to external Claude runner detection. Clean Codex and Claude Code marketplace installations of version `0.2.0` both contained the packaged profiles and successfully resolved roles from their managed cache paths.

A Claude Code execution smoke ran from a disposable plugin copy with the `haiku` alias at `low` effort. Claude served `claude-haiku-4-5-20251001`, invoked `mstack:setup-mstack`, executed the packaged resolver for the Codex-led profile's `implement_worker` role, and returned the configured `codex-native`, `gpt-5.6-luna`, `high`, and Fast assignment. A complete before-and-after content hash confirmed that the disposable plugin tree was unchanged. An earlier `auto`-permission attempt stopped at an approval request and was not counted as execution evidence; the passing run used permission bypass only inside the disposable test boundary.

The external `codex` runner and its provenance contract are owned by [Codex Runs as an Independent Consultant](2026-09-03-codex-as-independent-consultant.md).

## Consequences

Workflows gain one source of model truth and users can change a role without forking MStack. Every orchestration launch now incurs one small local resolution step. Profiles must remain complete and versioned with the role registry. Harness support depends on real runner capabilities; configuration can describe a role but cannot manufacture an unavailable model or native-agent API.

## Revisit when

- Either harness provides a portable native user-configuration mechanism that can replace local resolution without splitting the package.
- Role count grows enough that users cannot understand the effective mapping during setup.
- A harness cannot dynamically express the configured model or effort for native subagents.
- Users repeatedly ask for a packaged single-vendor profile instead of overriding the cross-vendor roles.
- A third harness or vendor needs a profile, which would strain host detection by environment variable.
