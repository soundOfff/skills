---
name: flow-code-review
description: Correctness-review a pinned change (behavior, spec, regressions, security) as flow-code-check's correctness worker.
---

# Code review

Act as the leaf correctness reviewer for one pinned change. Read and obey
[`flow-code-check/WORKER-CONTRACT.md`](../flow-code-check/WORKER-CONTRACT.md), then
perform the review yourself. Your axis is behavioral correctness. Solution
shape, elegance, file size, and maintainability belong to
`flow-code-quality-review` unless they cause a concrete behavioral failure.

## 1. Reconstruct the required behavior

Read the supplied issue/spec and its newest binding human decisions. Map every
acceptance criterion and explicit no-go to the changed entrypoints and tests.
Inspect adjacent callers and contracts needed to understand behavior. The diff
alone is insufficient evidence.

Completion: every stated requirement and prohibition maps to an implementation
path or an evidenced missing path.

## 2. Try to falsify the change

Trace every changed behavior through success, empty, invalid, unauthorized,
retry, cancellation, and failure paths that apply. Challenge:

- missing, partial, or incorrectly interpreted requirements;
- behavior outside the requested scope or behind incomplete gating;
- regressions in callers, consumers, wire contracts, persistence, and errors;
- stale state, races, non-atomic updates, retries, and duplicate effects;
- authentication, authorization, information exposure, and trust boundaries;
- data loss, irreversible state, unsafe fallback, and weak input variants;
- tests that miss the claimed behavior or use an easier case than production.

Run the smallest safe proof that can confirm or refute each suspected defect.
Treat a failing proof as evidence. Treat an unread test as unverified.

Completion: every changed behavior has been followed through its applicable
failure paths and every finding has a reproducible consequence.

## 3. Report correctness only

Return the exact worker contract. Quote the requirement for specification
findings and identify the violated invariant for runtime findings. Scope creep
is a defect when the change exposes behavior the issue did not authorize.

`PASS` means every requirement is implemented, no unauthorized behavior was
added, applicable failure paths hold, and the available proofs support those
claims. Unavailable binding requirements or necessary runtime evidence return
`BLOCKED`.

Completion: the report contains only correctness findings with repository
evidence, or an explicit contract-valid `PASS` or `BLOCKED`.
