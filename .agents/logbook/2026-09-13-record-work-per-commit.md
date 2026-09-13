# Logbook: Record work per commit

## Goal

Preserve what was tried, accepted, and rejected for each commit, with reasons and verification, while simplifying Logbook.

## Work and decisions

The parent updated the local DeepSeek Harness checkout to `c291e7961a` and read its Agent Notes policy and examples. Its decision records preserve useful rejection reasons, but their topic ownership, lifecycle folders, classification, and maintenance rules exceeded the user's needs.

The user chose a detailed entry alongside each commit. Reusing a living topic record was rejected because later edits obscure the sequence of work. Recording every command or inventing alternatives would add noise. Workers supply findings; the parent writes the entry.

The 22 existing records were moved into the flat directory. Their original text and formatting were retained, apart from relative links adjusted for the move. They remain historical topic records; this migration does not reconstruct an entry for every earlier commit. This replaces the lifecycle workflow described in [Log Durable Decisions at the Parent](2026-09-03-log-durable-decisions-at-the-parent.md).

## Result

[Logbook](../../skills/logbook/SKILL.md) now uses one entry per commit with four sections: Goal, Work and decisions, Result, and Verification and gaps. Capture happens during work and is finalized before committing. Later work gets a new entry; meaningful investigations can produce entries without code changes.

The validator checks flat placement, dated filenames, and titles. Template consistency and factual accuracy are reviewed by the parent. Lifecycle and classification checks were removed. Repository instructions, Implement, the README, and third-party attribution were updated to match.

## Verification and gaps

The validator self-test passed for flat entries and rejection of nested entries, impossible dates, missing titles, and undated files. Both changed skills passed the bundled skill validator. Repository checks passed for all 13 skills, 136 relative Markdown links, 105 files’ hygiene, and 23 Logbook entries. The 22 moved records were compared against Git: only the required relative-link adjustments changed their contents. The diff whitespace check passed.

No model evaluation was run; this is a workflow and format change. The entries preserve reported work and evidence, not complete agent transcripts.
