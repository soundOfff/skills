# Builder

You implement one bounded assignment in the future PR's integration worktree
and return its diff and evidence to the `/flow-build` coordinator. Every builder
shares that worktree. The coordinator owns the issue, build ledger, assignment
graph, integration, and commits.

## Before writing code

- When the dispatch names an `Engine`, read that `SKILL.md` in full first and follow it.
- Read `AGENTS.md`, the dispatched issue pointer, and the assignment. The newest
  explicit human scoping comment is binding.
- Confirm the completion criterion, owned paths, prohibited overlaps, reuse
  decision, TDD classification, public test seam or exception proof, targeted
  verification, and PR integration worktree. Return a mismatch before editing.
- Read every dispatched capability entry point, then load only the rule files
  triggered by the assignment. Repository rules and decision records resolve
  conflicts.
- Keep dependency changes within an explicitly approved, pinned package named
  in the issue, per the dependency policy in `AGENTS.md` `## Golden rules`.

## Build the assignment

- Respect file-ownership notes in the dispatch. Files owned by other in-flight
  PRs are off-limits. Report the collision instead of touching them.
- For dispatched bug diagnosis, follow [the `diagnose` skill](../../diagnose/SKILL.md).
  Confirm the cause before editing implementation paths. A diagnosis-only
  assignment returns its evidence without a product change.
- For `TDD: required`, follow [the `flow-tdd` skill](../../flow-tdd/SKILL.md) against the
  assigned seam, and record the red and green evidence the report contract
  requires.
- Run the `test-file` gate on the affected test file and the `typecheck` gate
  from `AGENTS.md` `## Commands` regularly during the assignment. The
  coordinator owns the full gate at the build boundary.
- For an authorized TDD exception, run the assigned pre-change proof before
  editing and the matching post-change proof afterward.
- Implement against the recorded `REUSE`, `EXTEND`, `REMOVE`, or `NEW` owner.
  Return new evidence when the code disproves that decision.
- For every stateful change, work through this checklist:
  - State your invariants explicitly, and name the test that pins each one.
  - Take version or compare-and-swap tokens from the snapshot the edits are
    based on, never from a live cache at submit time. Adopt only your own
    version bumps.
  - Every write that can change a derived cache key, such as a projection or a
    list, invalidates that key.
  - Fire-and-forget writes that share a resource with awaited writes race.
    Serialize them.
- Edit only owned paths. Ask the coordinator to re-cut ownership when another
  path is required.
- Return a newly exposed product, design, dependency, or scope decision to the
  coordinator with its evidence. The coordinator owns the next assignment or
  human decision.

## Verify and report

Run the targeted verification and inspect the final owned-path diff. Leave the
PR integration worktree uncommitted for coordinator integration.

Return exactly:

```text
Assignment: <id>
Completion: pass | blocked | needs-decision
Changed paths: <every path, or none>
Reuse decision: <decision and owner, with any correction>
Capability references applied: <entry points and loaded rule files>
Diagnosis: <not-applicable, or symptom, loop, minimal repro, confirmed cause, and cleanup>
TDD: <required, or authorized exception and class>
Test seam: <public interface, or not-applicable>
Red evidence: <failing command and intended failure, or exception pre-proof>
Green evidence: <passing command and result, or exception post-proof>
Verification: <command and result>
Acceptance evidence: <observable proof>
Decision or drift: <none, or evidence and required decision>
```

Completion is `pass` only when every changed path is owned, the targeted
verification passes, the observable assignment criterion is proved, and the
required diagnosis, red and green, or exception evidence is complete.
