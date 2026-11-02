# Logbook: Remove Source Style

## Context

`skills/apply-principles/references/source-style.md` banned comments and docstrings in owned source, and Implement, Architect, and Apply Principles applied it by default.

## Decision

Owner's call: remove the reference and every caller, leaving nine principle references. MStack no longer sets a comment policy; agents follow the project they are working in and any explicit user preference.

## Rejected

None considered.

## Verification and gaps

- `scripts/validate.py` passed, including links.
- Source already written under the old rule keeps its current form; nothing was reworked.
