# Logbook: Combine task clarification and tutoring in Grill Me

## Goal

Help the user clarify what they want to build and understand the concepts and tradeoffs before handing over implementation.

## Work and decisions

The parent read Matt Pocock's Grilling skill and MStack's Explain skill. The upstream interview organizes dependent decisions into rounds with recommended answers. The user also wanted questions that reveal their understanding, teaching where it is weak, and continued exploration for as long as useful.

One combined skill was chosen over separate interview and tutoring skills because the two activities inform each other. The user requested an initial theme overview so they can prioritize interests, with revisions as the conversation develops.

The adaptation favors focused questions over asking every available question at once. Recommendations remain useful for design choices; understanding probes wait for the user's answer before supplying one. Explain supplies explanations and diagrams without imposing its full report template on each exchange. Exhausting every possible branch and a fixed round limit were not adopted.

## Result

Added [Grill Me](../../skills/grill-me/SKILL.md) with a learning overview, task clarification, understanding probes, corrective teaching, and a closing summary. Project investigation is read-only. The user can redirect, pause, or proceed.

The README lists the skill, and third-party notices credit Matt Pocock's Grilling. The existing MIT notice is retained. With the pending removal of the TypeScript and GitHub comment skills, the catalog has 12 skills.

## Verification and gaps

The bundled skill validator passed. Repository checks passed for 12 skills, plugin manifests, 3 TOML files and packaged presets, 131 relative Markdown links, 101 files’ hygiene, and 25 Logbook entries. The diff whitespace check passed. No live tutoring evaluation has been run. The skill remains uncommitted for user review.
