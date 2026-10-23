# Flow code-check worker contract

## Input

Require one packet containing:

- repository and worktree;
- base SHA, HEAD SHA, diff command, changed files, commits, and diff hash;
- working-tree status;
- issue/spec pointers and review focus;
- applicable repository instructions, ADRs, and capability entrypoints.

Return `BLOCKED` with the missing field when the packet cannot identify one
stable, non-empty target. Treat the packet as a pointer set. Inspect the diff,
changed code, callers, tests, and cited sources directly before deciding.

## Finding bar

A finding is a demonstrated defect in the reviewed change. It includes:

- `BLOCKER`, `HIGH`, or `MEDIUM` severity;
- the smallest useful `path:line` location;
- concrete repository or runtime evidence;
- how the defect manifests, meaning the failure or maintenance cost caused by the change;
- one required outcome that removes the defect.

Severity follows demonstrated impact:

- `BLOCKER` is data loss, security compromise, destructive behavior, or a broken
  core workflow.
- `HIGH` is a user-visible regression, a violated contract, or a structural defect
  that will cause repeated failures.
- `MEDIUM` is a bounded correctness, maintainability, or design defect carrying a
  demonstrated cost.

A solution-quality finding caps at `HIGH`. It reaches `BLOCKER` only by
demonstrating a runtime or security consequence.

Return high-conviction findings only. A preference, cosmetic nit, unsupported
possibility, or optional redesign is not a finding, and neither is a defect you
cannot manifest. Repository instructions override generic guidance. Skip a
violation already reported by a mechanical check unless a distinct consequence
remains.

Report the smallest set of findings that covers the distinct defects. When
several share one root cause, report the cause once at the location that owns
it. One strong finding outranks several weak ones.

## Output

Return exactly:

```markdown
## Verdict
PASS | FAIL | BLOCKED

## Findings
| Severity | Location | Evidence | Impact | Required correction |
| --- | --- | --- | --- | --- |
| ... |

## Verification
- <inspection or command and result>
```

Use `none` as the only Findings row for `PASS`. `FAIL` requires at least one
finding. `BLOCKED` names the unavailable input or proof. Do not include praise,
summary prose, repair patches, or findings owned only by the other review axis.
