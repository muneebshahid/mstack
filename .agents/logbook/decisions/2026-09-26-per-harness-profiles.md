# Logbook: Keep native plugins and give each harness its own model profile

## Goal

Decide how MStack is installed and updated in Claude Code and Codex, and where each harness's model choices live.

## Work and decisions

Native plugins keep one copy per harness, so the copies can drift. A Codex parent now passes its own copy to Claude children with `--plugin-dir` ([previous entry](../incidents/2026-09-23-claude-code-readiness-and-model-refresh.md)). The reverse direction has no equivalent. `codex debug prompt-input` showed that `skills.config` paths, local marketplace overrides, and `--add-dir` do not add skills for one run. `-c 'plugins={"mstack@mstack"={enabled=false}}'` does turn off the installed MStack and leaves other plugins loaded. Delegate already passes the parent's skill and reference paths, so a stale Codex child matters only when it invokes a skill by name or resolves roles itself.

A shared linked copy was tested and rejected. A repository folder symlinked into `~/.claude/skills/<name>` loads as a real Claude plugin (`<name>@skills-dir`, skills named `<name>:<skill>`). Linked into `~/.codex/skills/<name>`, Codex shows the same names whenever either plugin manifest is present. New skills appeared in both without an update. With the native plugin also installed, Claude Code refuses to load the linked copy and Codex lists every skill twice, so switching to a linked copy requires uninstalling the native plugins and updating with `git pull` instead of each harness's own update commands. The user chose native plugins in both harnesses and accepts separate copies.

Profiles are now per harness: `~/.config/mstack/profiles/claude-code.toml` and `~/.config/mstack/profiles/codex.toml`. Setup configures only the harness it runs in. This reverses the [host-independent profile](2026-09-13-generalize-delegation.md) decision. The orchestrator owns model choice, and children receive their assignments from Delegate, so each harness can have different settings.

The harness is passed explicitly with `--harness`, not detected from `CLAUDECODE` or similar variables. The [earlier review](../investigations/2026-09-13-review-consolidated-stack.md) reproduced children inheriting their parent's markers and resolving the wrong harness. The shared `models.toml` is no longer read. The resolver names it and tells the user to run setup in that harness, instead of silently ignoring it.

The user then asked to add the Codex flag. The launcher now passes `-c 'plugins={"mstack@mstack"={enabled=false}}'` on fresh and resumed Codex turns. The reason is version consistency: Codex cannot load the parent's MStack copy for one run, so a child launched from Claude Code would otherwise use Codex's own install, which can be a different version. With the flag, the child uses only the skill and reference paths the parent passes. Together with `--plugin-dir` for Claude children, every external child now follows its parent's version.

The flag applies to every external Codex launch, including launches from a Codex parent, where the two copies are the same version anyway. Making it depend on the parent's harness would add a check for little benefit, because a Codex parent normally uses native sub-agents for Codex models. The cost is that an external Codex child cannot invoke MStack skills by name; it follows the paths it is given.

## Result

External Codex children launch with the installed MStack turned off. `models.py resolve` and `configure` take `--harness claude-code|codex`. `MSTACK_CONFIG` still overrides the path. Setup, runtime resolution, Delegate, and the README describe per-harness profiles, and Setup suggests the preset matching the harness.

## Verification and gaps

- 20 resolver tests pass. New tests cover harness isolation, the required `--harness` flag, and the legacy shared file.
- `scripts/validate.py` passed.
- With an empty configuration directory, Haiku `low` following `mstack:setup-mstack` in Claude Code ran `resolve --harness claude-code`. `gpt-6-luna` `low` in Codex, reading the repository's skill file, ran `resolve --harness codex`. Both received the missing-profile message for their own harness.
- The user's existing `~/.config/mstack/models.toml` was left in place because the installed 0.3.1 and 0.4.0 copies still read it. It should move to per-harness profiles after both installs update.
- Comparing Codex's full skill list with and without the override showed that only MStack was removed. Other plugins and personal skills remained.
- Launcher tests now check the override on fresh and resumed Codex commands; all 22 pass. A live `gpt-6-luna` `low` launch through the launcher reported no available MStack skills.
- Two live `gpt-6-luna` `low` children tested skill use. Given the absolute path to the repository's `skills/unslop/SKILL.md`, the child read that file and its linked `references/phrases.md` from the parent's copy. Asked only for `mstack:unslop`, the child searched `~/.codex` with `rg` and followed Codex's cached 0.4.0 copy. The recorded commands confirmed both. The flag removes the skill from Codex's skill list but not its files, so Delegate now requires MStack skills to be passed by absolute path.
- Whether `codex plugin marketplace upgrade` alone refreshes the installed Codex copy was not verified.
