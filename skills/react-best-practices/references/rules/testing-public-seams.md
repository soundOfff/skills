---
title: Test Public Behavior Through Repository Seams
impact: MEDIUM-HIGH
impactDescription: catches integration failures without replacing the path under test
tags: testing, public-seams, testing-library, end-to-end
---

## Test Public Behavior Through Repository Seams

Enter through the public surface whose behavior is claimed and keep the real
repository modules between that surface and the boundary the test deliberately
excludes. Assert user- or caller-visible outcomes rather than internal calls.

Follow the repository's decision records on network mocking and test layers.
Use the existing test layer that matches the behavior:

- pure domain logic: call the exported function or store directly, with no DOM;
- React behavior: render the component or hook with its real providers through
  Testing Library in the repository's component test runner;
- feature data behavior: call the feature's real data-access surface, backed by
  the repository's existing fake or local implementation of the excluded
  boundary;
- server adapters: test the exported server operation directly;
- critical browser journeys: use the end-to-end runner against the real dev
  server and data store, intercepting only the external boundary named by the
  journey.

Module mocking (`vi.mock`, `jest.mock`) is a boundary tool, not a blanket
violation or a shortcut around the unit under test. Appropriate boundaries
include an external model or API, time, randomness, irreversible effects,
unavailable browser APIs, or a heavy child with its own behavior test. Mocking
the subject's own hook, query, state owner, or authorization seam replaces the
behavior being claimed and requires a different public test seam.

Keep fixtures beside their owner and type them from the production schema or
contract. A test name states the observable behavior. Use nested `describe`
contexts only when their precondition materially changes that behavior.

When a `renderHook` test starts a React Query mutation outside a user event,
wrap the mutation in `await act(...)` and then wait on the observable settlement.
Awaiting `mutateAsync` alone may finish before React Query observer notifications.

Data hooks return state and errors. User-facing feedback belongs to the
component that invokes the mutation, so the same hook remains usable from other
features and tests can assert the rejection through its public contract.

## Review smells

- The test mocks the exact hook, store, API wrapper, or permission decision it
  claims to verify.
- A fixture duplicates a schema instead of deriving from the owning contract.
- Assertions inspect calls or class strings while the user-visible result is
  available.
- A jsdom test covers behavior that belongs to a fast framework-free seam.
- A local unit test claims confidence in a cross-process journey that only an
  end-to-end test can exercise.
