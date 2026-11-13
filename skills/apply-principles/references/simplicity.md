# Simplicity

## Minimize reader load

Reduce the layers readers must trace and the hidden state they must remember to understand behavior. Prefer direct calls, local state, pure functions, and names that expose intent. Preserve differences required by the domain, correctness, or performance.

Keep abstractions that express domain meaning, isolate volatility, enforce contracts, or simplify callers. Each layer should offer a different abstraction from its neighbors; remove forwarding layers and duplicated decisions when they add traversal without reducing complexity elsewhere. File size or a single caller or implementation does not prove a boundary unnecessary.

## Subtract before you add

Look for obsolete paths and redundant machinery before adding more. Inspect callers, exports, and contracts: deletion requires evidence of non-use or redundancy, or user-authorized removal or replacement of live behavior. Preserve required validation, compatibility, and behavior; keep unrelated cleanup out of the change.

Complexity needs a concrete requirement, reachable failure, operational constraint, or material risk. Examine the states, failure modes, and maintenance obligations it adds.

A hypothetical edge case, including one a reviewer raises, is not a reachable failure until you can name the input or state that triggers it. Weigh how likely it is against what it costs when it happens. When both are low, leave the code as it is and say why instead of adding branches.

Keep production code free of flags, parameters, branches, or state that exist only for tests. Test through the public interface, or through a seam that production also uses. If code can't be tested without a test-only hook, treat that as a design problem.

Hold tests to the same bar as code: each must earn its place. Keep a test when it fails because logic this project wrote is wrong, and write it once, at the layer that owns that logic. Don't test that a library, language, or database honors a declaration, don't repeat a check another layer already makes, and don't guard a failure you can't name. When a coverage rule seems to demand such a test, change what the rule measures instead.

Check existing repository, standard-library, platform, and installed capabilities before writing custom code. Prefer a simpler interface over a simpler implementation when the two conflict; neither line count nor reduced product scope is a substitute for a clearer design.

## Prefer deep modules

A module should hide more than it exposes: a small interface over substantial functionality. An interface nearly as complex as its implementation gives callers little; move the complexity inside or merge the module with its neighbor. Many small pieces are not a goal in themselves, because each one adds an interface to learn.

If a change to one design decision forces edits in several modules, that knowledge has leaked; give it one home.

## Prefer general-purpose modules

Build only what today's needs require, behind an interface that is not tied to today's caller. When designing a module or API, ask:

- Is this the simplest interface that will cover my needs?
- In how many situations will this module or function be used? If only one, it is likely too specialized.

Specialization is fine when it is necessary; avoid only the unnecessary kind. Redesign when the result is both more general and simpler. Keep the specialized form when generalizing would add parameters, modes, or speculative features.
