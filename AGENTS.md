# Repository instructions

- Record decisions, incidents, and investigations that future agents would need with `skills/logbook/SKILL.md`. The parent agent decides and writes; workers return evidence and never edit `.agents/logbook/`.
- Engineering standards: `skills/apply-principles/SKILL.md` and its references.
- Before release, run `python3 scripts/validate.py` (skills, manifests, presets, links, hygiene, tests, Logbook). In Codex, also run the bundled `skill-creator` validator on changed skills.
- Do not commit credentials, private keys, access tokens, personal data, private repository material, machine-specific absolute paths, or generated caches.
- Keep cross-skill links repository-relative so the stack remains portable.
