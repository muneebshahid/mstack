# Repository instructions

- Use `skills/logbook/SKILL.md` for durable architecture, behavior, process, testing, and simplification decisions. Update an existing record when the decision is the same; add a record when the decision is distinct.
- The parent agent owns Logbook judgment and writes. Workers may return decision evidence but must not edit `.agents/logbook/`.
- Treat the installed `principle-*` skills as the canonical engineering standards. Use `apply-principles` when the relevant leaves are not already known.
- Validate every changed skill and both plugin manifests before release. Validate Logbook records with `skills/logbook/scripts/validate_logbook.py`.
- Use temporary cheap model overrides for execution smoke tests. Restore and preserve the declared production configuration before release.
- Do not commit credentials, private keys, access tokens, personal data, private repository material, machine-specific absolute paths, or generated caches.
- Keep cross-skill links repository-relative so the stack remains portable.
