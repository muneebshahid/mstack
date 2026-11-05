# Delivery and Migration

## Sequence verifiable units

Choose coherent units and verification points that suit the dependencies and risk. Combine related edits when they are best verified together. Establish shared scaffolding early when it helps later work.

Plan and bound incomplete phases, name unfinished work, and run relevant checks during the transition. Passing those checks does not make the work complete. Run the project's required final checks against the completed result.

Finish coordinated internal migrations by removing obsolete APIs and adapters; retain compatibility only for an actual consumer or deployment requirement.

## Commit in verifiable steps

When commits are authorized, make one commit per step that has its own reason to exist and passes the project's checks, rather than one per task. Put behavior-preserving preparation before the change it enables, keep each test with the code it tests unless the test comes first, regenerate derived files in the commit that changes their source, and leave the record of decisions and status for last. Never leave an intermediate commit failing, so bisecting and reverting a single commit keep working. Fold fix-up commits into the step they belong to before the work merges.
