# Source Style

## No comments

Owned source must contain no comments or docstrings unless the user explicitly asks. This includes tests, scripts, configuration, temporary sketches, and scaffolds. TODOs and comment-based suppressions have no automatic exception.

Express intent and enforce constraints through names, types, structure, and executable checks. Put rationale in [Logbook](../../logbook/SKILL.md) or separate prose documentation.

## Remove comments without losing constraints

When cleanup would make code unclear, reshape it to carry the meaning. Do not weaken safety rules or checks to reach zero comments. If safe removal requires an out-of-scope reshape, leave the existing comment and report it and the constraint as unresolved. Do not claim zero-comment cleanup or treat this as permission to add comments.

Preserve shebangs as executable interpreter directives and retain required legal and license headers. Generated, vendored, and third-party files are outside this cleanup. If a tool requires a comment directive and has no comment-free solution, report the concrete conflict rather than adding an exception. Check owned source for remaining comments and docstrings, accounting for these exclusions and explicit user requests.
