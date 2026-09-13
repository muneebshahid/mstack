# Logbook: Herdr for External Agents

Status: implemented
Kind: architecture

## Problem

Can Herdr give MStack visible, resumable external agents, separate working directories, and remote execution without adding another elaborate workflow? The user requested research before changing the skills, then authorized updating the local Herdr binary.

## Decision

The user selected Herdr for an initial consultant trial, then chose to leave it out of the implementation and use direct CLIs through [Consult](2026-09-12-consolidate-resumable-consultation.md). The local trial passed. Broader implementation-agent support and skill consolidation remain future work. The Herdr trial itself changed no launcher, role configuration, or skill.

Herdr supports named agents in visible terminals, follow-up prompts, Git worktree creation, native conversation restoration, and SSH hosts. Recommend native subagents for ordinary delegation and an optional Herdr backend for external agents whose visibility, lifetime, or location matters. The parent still assigns work and judges results.

The local binary was updated from 0.8.0 to the official 0.9.0 macOS ARM64 release, with its SHA-256 checked against GitHub release metadata. The prior binary was backed up. The subsequent authorized trial created its own named 0.9.0 server and consultant; existing sessions were not controlled. No integration was installed or remote machine added.

### Local consultant trial

The parent controlled an isolated Herdr session from Codex desktop using explicit session and pane targets. Herdr launched Claude Code interactively, submitted a read-only question about the existing runners, waited, and returned the output. The old consultant scripts were not invoked.

The trial used the Claude profile's `skill_eval_smoke_candidate` model and effort, Haiku `low`, with Herdr substituted for its native transport. The native Claude transcript verified `claude-haiku-4-5-20251001`; effort was requested explicitly but not independently verified. This establishes mechanics, not production-model quality.

Claude's repository trust dialog caused Herdr to return `agent_not_ready`. The parent read the dialog and accepted trust for the user's own repository under the existing authorization. Manual tool permissions stayed enabled; the requested reads needed no further approval. No permission bypass was used.

The initial response described copying context instead of native resumption. The parent challenged it through Herdr. The same consultant corrected its answer and recalled the earlier test marker and storage decision. The parent then exited only that consultant, confirmed the shell had returned, and relaunched it through Herdr with its explicit native session ID, model, effort, permissions, and role instruction. A third prompt recovered the earlier context without tools. Herdr reported the same native conversation ID throughout.

Prompts, terminal responses, identifiers, model evidence, and a readable report were retained under the proposed per-task MStack state directory outside the checkout. The idle consultant and dedicated server remain available for user inspection. No disposable trial files required cleanup. The working tree contained only this parent-owned investigation record after consultation. Native fallback, automatic server restart restoration, other harnesses, remote execution, and implementation worktrees were not exercised.

### Persistence and results

- At investigation time, the Claude runner explicitly passed `--no-session-persistence`. [Consult](../../skills/delegate/SKILL.md) now owns the subsequent persistence work.
- At investigation time, the Codex runner already persisted sessions and captured a thread ID, but did not expose resumption. Herdr is not required to add that capability.
- Detaching Herdr preserves running processes. Restarting its server requires native session restoration through supported integrations; layout restoration alone cannot recover conversations.
- Herdr 0.9.0 constructs Claude and Codex resume commands from the native session ID without replaying original model, effort, or permission arguments. Whether each harness restores those settings correctly needs a live test.
- Keep the host, Herdr session, pane, and native conversation ID with the result. Agent names describe live occupants and disappear when those occupants exit. They are not durable conversation identifiers.
- Herdr waits observe lifecycle state, not a specific completed turn or successful task. Its terminal reads are not equivalent to the launchers' structured reports and served-model evidence. Preserve that evidence when considering a replacement. Current website documentation describes additional alternate-screen retrieval behavior; the installed skill still describes file output as a fallback, so test the installed behavior.

### Workspaces and remote execution

A workspace groups terminals and working directories; it does not isolate files. Read-only consultants can share a checkout. Independent writers should normally use separate Git worktrees. Herdr can create these from a branch or base revision; do not assume it copies uncommitted work. Current runner temporary directories hold prompts and result artifacts, not separate source checkouts. Resumable workers need directories that remain available.

Use a workspace per task when useful, with named panes for external roles. Native harness children do not automatically become separately controllable Herdr panes. Avoid a server or checkout for every read-only question.

Version 0.9.0 adds saved SSH machines in a shared UI. Each machine retains its own server and sessions. It needs its own checkout, harness installation, MStack, dependencies, and authentication; Herdr does not copy those automatically. IDs are scoped to a server, and selecting a remote machine in the UI does not retarget an existing pane's CLI commands.

## Alternatives considered

- Require Herdr for every delegation. Not recommended: native delegation remains simpler for short tasks, and Herdr introduces terminal lifecycle and output handling.
- Merge the public consultant skills into `consult`: subsequently accepted and implemented with direct CLIs and provider references; optional Herdr integration was deferred.
- Use the existing consultant runners for external implementation. Not suitable as currently defined: they are read-only, and the resolver requires a native `implement_worker`. Supporting external writers is a separate change to that contract.
- Fix session resumption in the headless runners first. A smaller option that solves follow-up consultation without providing Herdr's visibility or remote workspace UI.

## Evidence

The parent inspected both local runners, model resolution, installed native CLI help, `herdr --skill` on 0.8.0 and 0.9.0, command-group help, upstream documentation, and the tagged resume implementation. The subsequent trial used one Haiku conversation across two process launches and three prompts. No native subagent was used.

- [Herdr 0.9.0 release](https://github.com/herdrdev/herdr/releases/tag/v0.9.0)
- [Agent automation](https://herdr.dev/docs/agent-automation/)
- [CLI reference and worktrees](https://herdr.dev/docs/cli-reference/)
- [Session restoration](https://herdr.dev/docs/session-state/)
- [Tagged native resume implementation](https://github.com/herdrdev/herdr/blob/v0.9.0/src/agent_resume.rs)
- [SSH machines](https://herdr.dev/docs/connecting-machines/)
- [Socket API](https://herdr.dev/docs/socket-api/)

The desktop task is outside a Herdr-managed pane. The bundled skill assumes `HERDR_ENV=1`, so the initial research stayed with static help, docs, and source. The user's later explicit request authorized a trial from desktop. Explicit named-session CLI targeting worked without setting a fabricated Herdr environment or using the user's focused session. A general integration still needs to distinguish inherited pane context from explicit external targets.

This extends the earlier [Claude](2026-09-03-claude-as-independent-consultant.md) and [Codex](2026-09-03-codex-as-independent-consultant.md) investigations. The subsequent Consult record owns the current launcher contracts.

## Consequences

Herdr appears useful for visible external consultation and remote workers. It does not itself provide task reasoning, source isolation, read-only enforcement, durable result capture, or model verification. A small integration should reuse native session identifiers and existing evidence rather than introduce a scheduler or mandatory pipeline.

## Revisit when

Revisit Herdr only if the user requests it again, using the successful local trial as evidence. Explicit process resumption passed with launch settings reapplied; automatic server restart recovery and UI detach/reattach were not tested. Test other harnesses, independent writing worktrees, and a user-selected SSH host when those capabilities are needed.
