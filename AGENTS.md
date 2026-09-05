# Repository instructions

- Use `skills/logbook/SKILL.md` to add or update records for every non-trivial change and meaningful investigation or review outcome. Reuse the record that owns the topic; mechanical or local edits are exempt under that skill.
- The parent agent owns Logbook judgment and writes. Workers may return work and outcome evidence but must not edit `.agents/logbook/`.
- Treat the ten references under `skills/apply-principles/references/` as the canonical engineering standards. Use `skills/apply-principles/SKILL.md` to select the smallest relevant references when they are not already known.
- Validate every changed skill with the bundled Codex `skill-creator` validator. Validate Logbook records with `skills/logbook/scripts/validate_logbook.py`.
- Resolve Skill Eval's dedicated smoke roles for execution checks; packaged defaults use Luna `low` with Fast for Codex mechanics and Haiku `low` for Claude mechanics. Keep production assignments unchanged, record every substitution, and do not treat smoke results as production-quality evidence. Verify the served model through the launcher's `summary.json` and do not use plan mode for a Haiku smoke run because plan mode may route the work to a larger model.
- Do not commit credentials, private keys, access tokens, personal data, private repository material, machine-specific absolute paths, or generated caches.
- Keep cross-skill links repository-relative so the stack remains portable.
