# Logbook: Trim instructions capable models follow anyway

## Context

Skill text carried disclaimers, restated defaults, and panel mechanics repeated across skills, much of it written for less capable models. An independent read-only review checked each cut against the scripts and Logbook.

## Decision

Owner's call: remove text a capable model follows without being told, and keep one home for repeated rules. Panel mechanics live in Delegate, whose launcher already injects read-only boundaries and refuses output inside the checkout. Setup drops migration rules that `models.py` errors already state. The "use judgment, these are defaults" disclaimers are gone.

Keep what a model cannot infer: repo facts and paths, script flags, permission boundaries, and rules that came from a real failure.

## Rejected

- **Trimming Unslop, including its worked examples:** owner's call to leave it unchanged.
- **Dropping Show Me's "include only what is relevant" line:** selection is the point of the skill.
- **Dropping the `git log -- <entry>` note in Logbook:** it explains why entries omit their own commit.
- **Dropping the `models.toml` migration offer:** legacy files still exist, and nothing else tells an agent to carry their overrides over. Remove it once they are gone.

## Verification and gaps

- `scripts/validate.py` passed.
- No trial has compared behavior before and after these cuts.
