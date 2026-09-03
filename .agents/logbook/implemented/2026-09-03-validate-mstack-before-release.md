# Logbook: Validate MStack Before Release

Status: implemented
Kind: testing

## Problem

MStack can pass on one maintainer's machine while relying on untracked caches, installed validators, malformed cross-skill links, divergent manifests, or model configuration that a clean installation cannot resolve. Marketplace installation also depends on external CLIs and network access that ordinary repository CI does not own.

## Decision

`scripts/validate.py` is the portable repository validation entry point. It uses Python's standard library to validate skill identity and frontmatter, synchronized plugin manifests, TOML syntax, every packaged model profile, repository-relative Markdown links, tracked-file hygiene, unit tests, and Logbook records. GitHub Actions runs that command on pushes to `main` and pull requests.

Marketplace installation and live model behavior remain explicit release checks. They run from disposable environments with cheap configured smoke models and record served-model provenance without treating the result as production-quality evidence.

## Alternatives considered

- Depend on the validators installed under the maintainer's Codex home. Rejected because contributors and GitHub Actions do not share that filesystem.
- Install Codex and Claude Code in ordinary pull-request CI. Rejected for now because those checks require external binaries, authentication, network state, and model usage; they would make deterministic repository validation brittle and expensive.
- Maintain separate shell commands for each check. Rejected because release readiness would depend on remembering an undocumented sequence.

## Evidence

- `scripts/validate.py`
- `.github/workflows/validate.yml`
- `README.md`

The portable command passes against the complete repository. Official local Codex skill and plugin validators remain an additional maintainer check, and clean marketplace installation is tested separately.

## Consequences

Contributors and CI have one deterministic validation command with no package-install step. Live harness compatibility is not implied by a green CI check; release verification must still exercise marketplace installation and the relevant harness behavior.

## Revisit when

- Codex or Claude Code publishes a stable unauthenticated package validator suitable for CI.
- Marketplace installation can be tested deterministically without account credentials or model usage.
- The portable checks begin duplicating a maintained official validator that can be pinned in the repository.
