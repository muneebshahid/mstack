# Simplicity

## Minimize reader load

Reduce the layers readers must trace and the hidden state they must remember to understand behavior. Prefer direct calls, local state, pure functions, and names that expose intent. Preserve differences required by the domain, correctness, or performance.

Keep abstractions that express domain meaning, isolate volatility, enforce contracts, or simplify callers. Remove forwarding layers and duplicated decisions when they add traversal without reducing complexity elsewhere. File size or a single caller or implementation does not prove a boundary unnecessary.

## Subtract before you add

Look for obsolete paths and redundant machinery before adding more. Inspect callers, exports, and contracts: deletion requires evidence of non-use or redundancy, or user-authorized removal or replacement of live behavior. Preserve required validation, compatibility, and behavior; keep unrelated cleanup out of the change.

Complexity needs a concrete requirement, reachable failure, operational constraint, or material risk. Examine the states, failure modes, and maintenance obligations it adds.

Check existing repository, standard-library, platform, and installed capabilities before writing custom code. Simplify interfaces before polishing implementation; neither line count nor reduced product scope is a substitute for a clearer design.
