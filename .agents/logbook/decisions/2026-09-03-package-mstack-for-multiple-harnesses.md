# Logbook: Package MStack for Multiple Harnesses

Status: implemented
Kind: architecture

## Problem

The original `skills` repository was a published copy of a Codex installation. It had no stable product identity or harness manifests, so users could not install the complete stack through Codex or Claude Code plugin workflows.

## Decision

The product and repository are named MStack. The canonical source remains the shared `skills/` tree. Codex and Claude Code use thin manifests around that tree through `.codex-plugin/` and `.claude-plugin/` rather than maintaining duplicated skill copies.

The repository provides self-hosted marketplace metadata for both harnesses. MStack is a skills-only plugin and does not add an MCP server merely for distribution. Runtime-specific orchestration remains an explicit compatibility layer; a manifest alone does not establish that every workflow behaves correctly in both harnesses.

## Alternatives considered

- Keep the repository name `skills`. Rejected because the name is generic, difficult to distinguish in marketplaces, and unsuitable for namespaced setup commands and configuration.
- Publish separate Codex and Claude repositories. Rejected because shared principles and workflows would drift.
- Duplicate the plugin under `plugins/mstack/` to satisfy a local marketplace layout. Rejected because repository-relative URL sources can point at the plugin root without copying the package.
- Add an MCP server for persistent configuration. Rejected because the current product is local workflow guidance and does not need a hosted service.

## Evidence

- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `skills/`
- `README.md`

Both Codex and Claude Code successfully added the public GitHub marketplace and installed the current `mstack@mstack` version `0.2.0`. The temporary installations and marketplace registrations were removed after verification. These checks establish package discovery and installation. Claude Code became a full orchestrating host once the `codex` launcher and the `claude-multimodel` profile existed; see [Codex Runs as an Independent Consultant](2026-09-03-codex-as-independent-consultant.md).

## Consequences

Consumers install managed plugin copies while maintainers edit one canonical repository. Harness-specific behavior must live in adapters or conditional references without forking the underlying principles. Releases must keep manifest versions aligned and test both installation paths.

## Revisit when

- Either harness changes its manifest or marketplace contract.
- Shared skill instructions cannot express a workflow without harmful harness-specific branching.
- MStack adds a hosted capability that genuinely requires an MCP server.
