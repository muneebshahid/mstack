---
name: unslop
description: Remove AI writing tells and add a natural, specific human voice. Use when drafting or revising substantive prose, or when the user asks to unslop, de-AI, humanize, remove AI patterns, or make text sound natural. Preserve exact quotations, facts, citations, technical terminology, and an explicitly requested house style.
---

# Unslop

Edit prose to remove predictable AI patterns and restore a specific human voice. Clean writing is not enough: sterile, voiceless text is also an AI tell.

Apply this skill to substantive prose you draft unless the user requests exact wording or a conflicting style. Do not rewrite code, structured data, legal quotations, source quotations, or other text whose wording must remain exact.

## Process

1. **Protect the writing contract.** Identify the meaning, facts, citations, audience, register, authorial perspective, and any wording that must survive.
2. **Scan for AI patterns.** Check content, language, structure, tone, formatting, repetition, and rhythm.
3. **Rewrite.** Preserve meaning and evidence while cutting filler, formula, puffery, and vague claims.
4. **Add soul.** Restore a credible point of view, concrete detail, and natural rhythm without inventing facts, feelings, anecdotes, or opinions for the author.
5. **Self-audit.** Ask: "What makes this obviously AI-generated?" Fix the remaining tells, then remove anything the revision added only to sound human.

For a normal drafting request, apply the process silently. When editing supplied text, return the revised text first; explain changes or score the draft only when requested or useful.

## Add soul

Removing patterns is half the job. The result should sound like someone with a reason to write it.

- **Take a position when the material supports one.** React to the evidence instead of mechanically balancing every point. Do not manufacture the user's beliefs.
- **Vary rhythm.** Mix concise sentences with longer ones that carry a complete thought. Avoid metronomic paragraphs and stacks of fragments.
- **Acknowledge real complexity.** Preserve tensions and mixed reactions when they matter. Do not flatten them into generic hedging.
- **Use first person when it fits.** "I" and "we" are valid when the speaker and genre support them. Never invent personal experience.
- **Allow controlled irregularity.** Natural prose need not force every section, paragraph, or list into the same shape.
- **Be specific.** Replace mood labels and vague significance with the mechanism, observation, example, source, or number that creates the reaction.

Match the intended register. A blog can be conversational. Scientific and technical writing should remain precise and appropriately formal: retain domain terms, use "we" for the authors' work when suitable, and name or cite sources instead of invoking unnamed experts.

## Patterns to detect and fix

Treat these as diagnostics, not a reason to distort accurate prose. A pattern used once may be natural; repetition and clustering are stronger evidence.

### Content

- Cut puffery, promotional language, grandiose stakes, and generic conclusions. State what happened and why it matters in concrete terms.
- Replace media or company name-dropping with one relevant source and what it actually said.
- Delete superficial participle phrases such as "highlighting," "ensuring," "showcasing," and "underscoring," or replace them with a supported analytical claim.
- Name the source behind "experts believe," "reports suggest," or "critics argue." Delete the attribution when no source exists.
- Replace formulaic challenge-and-triumph paragraphs with the actual constraint, response, and outcome.
- Do not invent analytical labels such as "the supervision paradox" unless the text defines and needs the term.

### Language

- Prefer plain words over AI vocabulary and business jargon: "use" over "leverage," "is" over "serves as," and the concrete domain noun over "landscape," "substrate," "paradigm," or "ecosystem."
- Cut filler, throat-clearing, excessive hedging, empty intensifiers, and adverbs propping up weak verbs.
- Avoid synonym cycling. Repeat the accurate term when changing it would blur meaning.
- Replace false ranges with a real list or a genuine scale.
- Preserve precise scientific and technical terminology. Specialized language is not slop when it names the actual concept.

### Structure and style

- State the point directly instead of using repeated "not X, but Y," negative countdowns, self-answered rhetorical questions, or fake suspense.
- Do not force ideas into threes. Use the number the material requires.
- Avoid anaphora, dramatic fragments, listicles disguised as prose, repeated paragraph endings, and fractal summaries.
- Prefer active voice and named actors when the actor matters. Passive voice is acceptable when the actor is unknown, irrelevant, or the genre convention calls for it.
- Split sentences that make readers backtrack. Keep related clauses together when splitting would make the prose choppy.
- Avoid em dashes by default; use a period or comma when it reads naturally. Do not replace every dash with parenthetical clutter.
- Use colons for actual lists or examples, not as a habitual dramatic connector.
- Use sentence-case headings. Remove decorative emoji, excessive bolding, smart quotes, and repetitive bold-label-colon bullets unless the requested format requires them.

### Communication artifacts

- Remove chatbot phrases, automatic praise, sycophancy, cutoff disclaimers, and invitations such as "I hope this helps" or "Let me know if."
- Cut pedagogical hand-holding such as "Let's unpack this" and "Think of it as" unless the audience genuinely needs an analogy.
- Do not simulate vulnerability or personal experience. Specific honest experience is useful only when it belongs to the author.

### Composition

- State each point once, support it, and move on.
- Use one strong example instead of stacking historical analogies or brand names.
- Drop a metaphor after it has done its job.
- Remove duplicated sections and conclusions that merely replay the document.
- If a sentence could appear unchanged in an unrelated project's documentation, replace it with a project-specific fact or cut it.

## Reference guidance

Read only the references needed for the current task:

- [references/phrases.md](references/phrases.md) for filler, jargon, vague claims, and phrase-level replacements.
- [references/structures.md](references/structures.md) for sentence, paragraph, rhythm, agency, and formatting patterns.
- [references/tropes.md](references/tropes.md) for a broad diagnostic catalog when auditing a long or heavily AI-styled draft.
- [references/examples.md](references/examples.md) for before-and-after transformations, especially scientific and technical prose.

For a short drafting request, this file is usually sufficient. For a full audit or substantial rewrite, read the relevant catalogs before revising.

## Quick audit

Before delivering prose, check:

- Does the opening begin with the point rather than announcing it?
- Are claims specific, sourced where needed, and free of invented significance?
- Did formulaic contrasts, rhetorical setups, forced threes, or repeated sentence shapes accumulate?
- Are actors named where responsibility matters?
- Does the rhythm vary without manufactured fragments?
- Does the formatting fit the document rather than an AI response template?
- Did the revision preserve the author's meaning, register, and actual voice?
- Can any sentence, paragraph, analogy, or conclusion be cut without losing information or character?

## Scored review

When the user requests an audit or score, rate each dimension from 1 to 10:

| Dimension | Question |
| --- | --- |
| Directness | Does the prose state its points rather than announce or stage them? |
| Rhythm | Does it vary naturally without repetitive cadence or fragments? |
| Trust | Does it respect the reader without hand-holding or manufactured emphasis? |
| Authenticity | Does it sound like a specific, credible author? |
| Density | Is every sentence carrying information, argument, or voice? |

A score below 35/50 calls for revision. Explain the highest-impact patterns with short excerpts, then provide a revised version when authorized.
