# Logbook: Load current MStack in Claude children and refresh model presets

## Goal

Check that MStack installs and runs correctly from Claude Code, since earlier work was verified mainly from Codex. Update both presets to current models.

## Work and decisions

`claude plugin validate .` passed and the marketplace install path matches the README. The local Claude install was still 0.3.1 because its marketplace clone was last refreshed on 2026-09-03.

A live check showed that the Claude launcher's `--add-dir <plugin>/skills` grants file access but does not register skills. A Claude child therefore saw whichever MStack version was installed in Claude Code (here the stale 0.3.1 set, including removed skills such as `claude-code` and `interrogate`), not the version doing the launching. `--plugin-dir <plugin root>` loads the packaged plugin for that session and takes precedence over the installed copy of the same name. The Codex plugin cache ships `.claude-plugin/`, so the same flag works when the launcher runs from Codex. `--add-dir` stays for read access to packaged and personal Codex skill files.

Claude Code's native Agent tool accepts model aliases but not effort. Delegate now says to launch externally when the assigned effort must apply, instead of leaving that case implied.

The Codex catalog now lists `gpt-5.6-luna` as an older model. The user chose `gpt-6-sol` `high` for `implement_worker` and `gpt-6-luna` for the explorer and smoke roles, with efforts and Fast unchanged. In the Claude preset, `implement_worker` moves from `sonnet` to `claude-opus-5-5` `high`. The other roles were already current and stay the same.

Versions are bumped to 0.4.1 so installed copies pick up the change.

## Result

Claude children load the same MStack version as their launcher. Both presets use current models.

## Verification and gaps

- `scripts/validate.py` passed, including all 22 launcher tests (one new assertion covers `--plugin-dir`) and the updated preset expectations.
- A Haiku `low` launch through `run_delegate.py` listed exactly the 12 current `mstack:` skills and served `claude-haiku-4-5-20251001`.
- A `gpt-6-luna` `low` Fast launch served `gpt-6-luna` at verified `low` effort.
- On 2026-09-26 Codex briefly dropped `gpt-6-sol` and `gpt-6-luna` from its catalog and rejected `gpt-6-luna` for the ChatGPT account. After they returned, `low` launches through the launcher served `gpt-6-luna` and `gpt-6-sol`.
- `claude-opus-5-5` was not launched. Only `low` launches were run, and these confirm availability, not production quality at the assigned efforts.
