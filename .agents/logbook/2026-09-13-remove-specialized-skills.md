# Logbook: Remove specialized skills

## Goal

Remove the standalone TypeScript and GitHub PR comment skills from the personal engineering stack at the user's request.

## Work and decisions

The parent compared the TypeScript skill and its examples with PStack's latest version. The useful missing guidance favored existing runtime schemas over duplicate interfaces and hand-written guards. Neither upstream file recommended Effect; its schema example used Zod.

A smaller TypeScript skill with fewer examples and less overlap with Apply Principles was proposed. The user chose to remove the skill entirely for now. No upstream additions were incorporated.

The GitHub comment skill originated in OpenAI's bundled Codex skills. After learning its origin, the user decided it did not belong in the personal stack and requested removal instead of refinement. Neither the Codex nor Claude personal skills directory contained a standalone installation at its standard location.

## Result

Removed `skills/typescript-best-practices/`, `skills/gh-address-comments/`, their README entries, and the third-party notice for the removed OpenAI skill. The catalog now has 11 skills. Shared typing guidance remains in [Modeling and Types](../../skills/apply-principles/references/modeling-and-types.md).

## Verification and gaps

Repository checks passed for 11 skills, plugin manifests, 3 TOML files and packaged presets, 128 relative Markdown links, 98 files’ hygiene, and 24 Logbook entries. The diff whitespace check passed. No source behavior changed, so runtime tests were not needed. Installed plugin caches were not updated.
