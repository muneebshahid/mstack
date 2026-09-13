# Logbook: Allow authorized edits and resumable nested Claude sessions

## Goal

Fix the two permission failures recorded in [the delegation change](2026-09-13-generalize-delegation.md): Claude denied an authorized fixture edit, and Claude launched inside Codex could not authenticate or persist its session.

## Work and decisions

The parent inspected the launcher and current CLI help, then checked official [Claude permissions](https://code.claude.com/docs/en/permissions), [Claude session storage](https://code.claude.com/docs/en/claude-directory), and [Codex permission profiles](https://developers.openai.com/codex/config-reference).

Claude's write flag previously changed only the prompt. The launcher now adds an absolute checkout-scoped `Edit` allow rule, which covers both Write and Edit tools, on fresh and resumed writing turns. Read-only calls add no rule. Kept `auto` mode rather than using `acceptEdits`, which would also preapprove edits in added skill directories. No blanket shell or permission bypass was added; existing deny and ask rules retain precedence.

A no-model sandbox check separated authentication from persistence: Claude reported logged out with networking disabled and logged in with it enabled. Enabling networking alone allowed a Haiku turn to complete, but no transcript was saved and resume failed. Allowing writes to Claude's `projects`, `session-env`, and `debug` directories made the transcript persist and resume succeed. This establishes the tested access requirements without claiming which macOS credential-service operation was blocked.

For Codex calls with `allow_subagents=true`, the launcher now supplies a per-process permission profile with networking, temporary-file access, and those three Claude runtime directories. It honors `CLAUDE_CONFIG_DIR`. The profile preserves the independent checkout write setting, including an explicit read-only checkout rule when the checkout is inside the writable temporary directory. Calls without delegation retain their existing sandbox selection. No saved configuration, credential copies, persistent MStack directories, or sandbox bypass were needed.

An initial diagnostic used an outdated `codex sandbox macos` command form; local help identified the installed syntax. A first attempt to pass quoted filesystem paths as dotted config keys failed parsing; supplying the profile as one TOML table worked. Neither failed configuration attempt launched a model.

## Result

Delegate's launcher and provider references now grant the permissions needed for the tested assignments. The parent can launch and resume a Claude consultant inside a sandboxed Codex process, and authorized Claude writing tasks can create and edit checkout files. The user approved committing and pushing after reviewing the test results.

## Verification and gaps

- Haiku low created the exact requested fixture content, then resumed conversation `bfe7a519-6989-4cb1-b243-b979f63a3a42` and appended the requested line through Edit. Original input remained unchanged.
- A sandbox probe using the launcher's read-only delegation profile denied a checkout write while allowing a temporary probe in Claude's session metadata directory. The probe was removed.
- A sandboxed Haiku turn with runtime storage enabled persisted conversation `4ba3f940-c48d-46b1-b8f4-430df741daf3`; its resumed turn recalled `cedar-56` without being given the marker again.
- Luna low, Fast requested, ran the full launcher path as a read-only delegating process (`01a09b77-3f97-70c1-8c18-e1fe043dab98`). It launched Haiku without further delegation, read its actual ID, and resumed conversation `e7f7c4e5-bb63-477d-9553-1c198aa5a591`. Haiku returned the correct fixture line and recalled `birch-82`; both child summaries kept writes and delegation disabled. The parent checked outputs and workspace files.
- Served external models were `gpt-5.6-luna` and `claude-haiku-4-5-20251001`. Codex effort was verified as low; Claude effort and Codex Fast remain requested settings. These configured smoke roles test mechanics, not production quality.
- All 22 launcher tests passed, including new coverage for scoped Claude write rules on fresh/resumed calls and read-only nested runtime access with a custom Claude directory. Existing coverage also checks resumed writable Codex delegation and unchanged default permissions.

Live checks used macOS, Codex 0.153.4, and Claude Code 2.1.257. Other platforms, older Codex permission-profile support, credential refresh writes, and Claude features needing additional runtime directories were not tested. Enclosing or managed restrictions still apply. Temporary fixtures and launcher artifacts were removed after recording the evidence; provider conversations remain available.
