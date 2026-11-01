# Repository instructions

- Use `skills/logbook/SKILL.md` to record decisions, incidents, and investigations that future agents would need. Most commits need only a commit message.
- The parent agent owns Logbook judgment and writes. Workers may return work and outcome evidence but must not edit `.agents/logbook/`.
- Treat the seven references under `skills/apply-principles/references/` as the canonical engineering standards. Use `skills/apply-principles/SKILL.md` to select the smallest relevant references when they are not already known.
- Validate every changed skill and both plugin manifests before release. Validate Logbook records with `skills/logbook/scripts/validate_logbook.py`.
- Do not commit credentials, private keys, access tokens, personal data, private repository material, machine-specific absolute paths, or generated caches.
- Keep cross-skill links repository-relative so the stack remains portable.
