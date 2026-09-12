# Testing

- Add or improve tests for consequential behavior that existing checks do not protect. Prefer observable outcomes over mocks, implementation details, or duplicated assertions. Coverage percentage alone does not justify more tests.
- Use test-first when requested or useful: demonstrate the intended failure, make the change, then rerun the test. A regression test should catch the original bug.
- Choose the level that exercises the real behavior. When a new test costs more than the protection it adds, use a focused reproduction, script, or direct check and report material gaps.
- Preserve useful regression protection. Change existing expectations only when the intended behavior changes; remove redundant or obsolete tests when their value is gone.
