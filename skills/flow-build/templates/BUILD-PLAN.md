---
issue: null
status: planning
branch: null
worktree: null
base_sha: null
head_sha: null
started_at: null
updated_at: null
---

<!-- status: planning | building | verifying | awaiting-to-pr | needs-decision | blocked -->

# Authority snapshot

| Issue | Parent | Binding comment | Assignee | Board status | Review boundary |
| --- | --- | --- | --- | --- | --- |
|  |  | none |  | not-applicable |  |

## Eligibility

| Ready item | Evidence | Result |
| --- | --- | --- |
| `<one row per numbered Definition of Ready item>` |  |  |

## Lane

| Actor | Claim evidence | PR integration worktree | Branch | Base SHA |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Scope lock

| Criterion | Required behavior | Owned paths | Reuse decision and owner | Test seam | Verification |
| --- | --- | --- | --- | --- | --- |
| AC1 |  |  |  |  |  |

## Execution graph

| ID | Completion criterion | Owned paths | Blocked by | Diagnosis and loop | TDD and red command | Capability references | Agent | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B1 |  |  | none | not-applicable | required: `<command>` | `flow-build/references/builder.md`; `tdd` |  | planned |

## Dispatch gate

- [ ] Every acceptance criterion maps to at least one assignment.
- [ ] Every assignment maps to an acceptance criterion.
- [ ] Every assignment has one checkable completion criterion.
- [ ] Every prospective changed path has one owner.
- [ ] Dependency edges are real and acyclic.
- [ ] Every assignment has a `REUSE`, `EXTEND`, `REMOVE`, or evidenced `NEW` destination.
- [ ] Every assignment records `TDD: required` with a public seam and red command, or one permitted exception with pre-change and post-change proof.
- [ ] Every bug or performance branch records its exact symptom and red-capable loop, or depends on a read-only diagnosis assignment.
- [ ] Every capability branch resolves to exact references or `not-applicable` evidence.
- [ ] Targeted verification exists for every assignment.

## Integration log

| Assignment | Changed paths | Diagnosis proof | Red or pre-proof | Green or post-proof | Targeted verification | Commit | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Drift

`none`, or record the assignment, evidence, and required human decision.

## Acceptance proofs

| Criterion | Proof | Result |
| --- | --- | --- |
|  |  |  |

## Repository gates

One row per full-gate id from `AGENTS.md` `## Commands`. A gate that reads `n/a` is recorded as `skipped: n/a`.

| Gate | Command | Result | Evidence |
| --- | --- | --- | --- |
| `lint` |  | pending |  |
| `typecheck` |  | pending |  |
| `test` |  | pending |  |
| `build` |  | pending |  |

## Build gate

- [ ] The issue snapshot and claim remain current.
- [ ] Every assignment is accepted and committed.
- [ ] Every changed path traces to one assignment and criterion.
- [ ] Every behavioral change has recorded red and green evidence. Every exception has its authorized pre-change and post-change proof.
- [ ] Every bug fix has a reproduced symptom, minimal reproduction, confirmed cause, and instrumentation cleanup proof.
- [ ] Reuse decisions match the integrated diff.
- [ ] Documentation and decision-record effects are resolved.
- [ ] Every acceptance criterion has a passing proof.
- [ ] The issue Verification signal passes.
- [ ] Every full-gate command has an honest result.
- [ ] UI proof is recorded or marked `not-applicable` with evidence.
- [ ] HEAD is rebased on the fetched `origin/<base>`.
- [ ] The diff stops at the issue Review boundary.

## Handoff

| Branch | PR integration worktree | Base SHA | HEAD SHA | Commits | Diff summary | UI proof |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
