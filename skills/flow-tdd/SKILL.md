---
name: flow-tdd
description: Test-drive executable behavior through public seams with a red, green, refactor loop. Use for behavior-changing work, when the user wants to build a feature or fix a bug test-first, mentions red-green-refactor, or wants integration tests.
---

# Test-driven development

TDD is a vertical red, green, refactor loop. Each cycle proves one observable
behavior through a public seam, adds only enough implementation to make it pass,
then simplifies while it remains green.

Read the repository's domain language and the decision records governing the
change, so test names, interfaces, and expected behavior use its vocabulary.
`docs/agents/domain.md` says where they live. Without it, read `CONTEXT.md` and
`docs/adr/` when they exist.

## Agree the seam

A **seam** is the public interface where behavior is exercised and observed.
Tests enter through that seam and assert its result rather than private methods,
internal calls, or storage side channels.

`/flow-build` supplies a seam already agreed through the Ready issue and build
plan. Use it without asking again. When invoked outside `/flow-build`, record the
proposed seam and obtain human confirmation before writing the first test.

When selecting the seam or assertion, consult [`tests.md`](tests.md). When a
test double is required, consult [`mocking.md`](mocking.md) before adding it.

## Run one vertical cycle

1. **Red.** Write the narrowest behavior test for the current slice. Run it and
   record evidence that it fails for the missing or defective behavior.
2. **Green.** Add the minimum behavior needed for that test. Run it and record
   the passing result. Preserve previous green tests.
3. **Refactor.** Simplify names, ownership, duplication, and control flow while
   the same tests stay green. Add no behavior during refactoring.

Repeat with the next behavior only after the current cycle is green.

## Keep tests durable

- Assert behavior a user or caller observes through a public interface.
- Derive expected values from the issue, a worked example, or another
  independent source of truth.
- Keep one logical behavior per test and name that behavior directly.
- Apply the boundary policy in [`mocking.md`](mocking.md) when a double is
  required.
- Prefer integration-style coverage when it stays deterministic and local.

Implementation-coupled, tautological, and horizontal test batches do not prove
the assignment. A horizontal batch writes every test first and the
implementation afterwards, so its tests check an imagined shape instead of real
behavior. A test that passed before the implementation is not red evidence
unless it reproduces the defect before the fix.

Completion: every changed behavior has its own recorded red and green evidence,
all retained tests pass after refactoring, and no test depends on an internal
implementation detail.
