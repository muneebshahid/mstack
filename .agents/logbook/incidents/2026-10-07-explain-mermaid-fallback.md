# Logbook: Explain draws diagrams where Mermaid does not render

## Goal

Stop Explain from leaving raw Mermaid in chats that show it as code, and stop it from rationing visuals.

## Work and decisions

In a Claude Code desktop session, Explain followed the template's Mermaid bullet and the architecture diagram showed as a code block. Redrawn as SVG with the session's inline widget tool, it rendered as a diagram.

A draft also added triggers for escalating to an HTML file (user asks, several dense visuals, output to keep or share). The user rejected it and kept the original HTML bullet. The user also asked to remove "Use as few visuals as needed": visuals are wanted even for small answers.

## Result

The Mermaid bullet now says that where the response surface does not render Mermaid, such as a Claude Code chat, the diagram goes through an available inline visual tool, such as a widget or SVG renderer, with a call tree as the last fallback. The "as few visuals as needed" line is removed. HTML escalation is unchanged. Bump to 0.4.3.

## Verification and gaps

- The skill-creator `quick_validate.py` passed for `skills/explain`.
- Not tested in a fresh Explain run. Codex's chat surface and which inline tools it offers were not checked.
