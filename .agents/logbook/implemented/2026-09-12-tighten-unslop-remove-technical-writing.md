# Logbook: Tighten Unslop and Remove Technical Writing

Status: implemented
Kind: simplification

## Problem

Unslop repeats guidance across its entry point, phrase list, structure list, trope catalog, and audit checklists. Some references ban every adverb or passive construction despite the entry point's contextual guidance. Several worked rewrites add numbers, sources, or personal experiences absent from their originals.

The user requested a repetition and wording pass, removal of Technical Writing, and no changes to Bro.

## Decision

Remove Technical Writing and its README entry without merging its document modes or style rules elsewhere. Leave Bro unchanged.

Shorten Unslop's entry point to editing guidance and meaning preservation. Consolidate the overlapping trope catalog into the phrase and structure references. Keep representative patterns, plain replacements, and contextual judgment; remove blanket word bans, repeated audits, and the arbitrary scoring threshold.

Replace the expansive worked examples with short invented examples whose rewrites preserve the original facts, uncertainty, and voice. Keep the upstream license unchanged and preserve the trope catalog's attribution in Third-Party notices.

## Alternatives considered

- Merge Technical Writing into Unslop. Rejected because the user explicitly asked to remove it for now.
- Keep four overlapping references with shorter wording. Rejected because the trope catalog repeats the other guides.
- Keep examples that add plausible specifics. Rejected because they contradict the instruction to preserve meaning and evidence.
- Treat listed words and constructions as forbidden. Rejected because technical terms, uncertainty, passive voice, and useful formatting can carry necessary meaning.

## Evidence

The parent inspected all Unslop files, Technical Writing, Bro, source notices, and caller references. It edited the prose directly, repaired the README and reference links, and retained the license. No consultant or behavioral trial was run for the initial wording pass.

Repository validation passed with 14 skills, packaged profiles and manifests, 118 relative links, hygiene checks, unit tests, and Logbook records. Unslop passed the skill validator. Bro and the Unslop license match their committed versions. Unslop's Markdown falls from 8,100 words to roughly 1,630.

The user then requested paired trials on clichéd text using Luna Max. The parent staged complete committed and revised skill copies outside the repository and ran three identical source drafts per version: a release announcement, incident explanation, and design recommendation. Six fresh native agents used `gpt-5.6-luna` at `max`; local execution records identified that model and effort and showed reads of the exact staged entry points. All snapshots passed structural validation, and disposable file hashes remained unchanged. Original/revised output word counts were 138/141, 146/155, and 187/161. Length was descriptive rather than a quality score.

Both versions removed obvious filler. Release outputs were effectively tied. The original incident rewrite changed a planned log request into a completed action; the revised version preserved the future action. The original design rewrite also changed current behavior into recommendations and asserted that requirements were met without supporting evidence. The revised version preserved more of the source, but both added threshold-setting advice and both altered punctuation inside a literal incident log quote.

A separate Luna Max assessor compared neutral outputs. This used the user's model preference instead of the configured Fable quality judge, without changing model defaults. After decoding labels, its pairwise findings favored the revised incident and design outputs and tied the release pair. The parent agreed with those substantive findings, rejected minor release-format objections, and caught the shared quote change missed by the assessor. The small sample remains inconclusive for a general winner; the parent kept the revised skill available for user review without changing its instructions in response to the trials.

Only the revised release run read optional references; the other five used their entry points. Reference behavior and automatic activation therefore remain largely unexercised. Full inputs, outputs, skill snapshots, hashes, prompts, agent IDs, material tool-call excerpts, and the independent assessment were retained outside the repository for the user's inspection. The browser URL policy blocked the HTML preview; a Markdown comparison was provided, and the HTML output blocks were checked against the raw text without claiming visual inspection.

## Consequences

The public catalog falls from 15 skills to 14. Unslop retains phrase-level guidance, structural guidance, and worked examples with less repeated instruction. Documentation-specific rules from Technical Writing are no longer active.

## Revisit when

Actual use reveals a recurring writing failure not covered by the shortened guidance, or the user wants a separate documentation standard again.
