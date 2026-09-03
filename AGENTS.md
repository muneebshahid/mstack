# Repository instructions

- Use `skills/logbook/SKILL.md` for durable architecture, behavior, process, testing, and simplification decisions. Update an existing record when the decision is the same; add a record when the decision is distinct.
- The parent agent owns Logbook judgment and writes. Workers may return decision evidence but must not edit `.agents/logbook/`.
- Treat the installed `principle-*` skills as the canonical engineering standards. Use `apply-principles` when the relevant leaves are not already known.
- Validate every changed skill with the bundled Codex `skill-creator` validator. Validate Logbook records with `skills/logbook/scripts/validate_logbook.py`.
- Resolve Skill Eval's dedicated smoke roles for execution checks; packaged defaults use Luna `low` with Fast for Codex mechanics and Haiku `low` for Claude mechanics. Keep production assignments unchanged, record every substitution, and do not treat smoke results as production-quality evidence. Verify the served Claude model and do not use plan mode for a Haiku smoke run because plan mode may route the work to a larger model.
- Do not commit credentials, private keys, access tokens, personal data, private repository material, machine-specific absolute paths, or generated caches.
- Keep cross-skill links repository-relative so the stack remains portable.
