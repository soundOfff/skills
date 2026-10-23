# Flow design-check worker contract

## Input

Require one packet containing:

- repository and worktree;
- base SHA, HEAD SHA, diff command, changed files, commits, and diff hash;
- working-tree status;
- the UI inventory: every UI-affecting hunk with its changed `path:line`;
- authority pointers: the files named by the `Design system` and `Conventions`
  rows of `## Sources of truth` in `AGENTS.md`, the applicable accepted ADRs,
  any feature-local design document, the issue's binding design decisions, and
  the base and target versions of every changed authority file, or `none` for a
  row that has no source;
- render evidence: a screenshot index naming each capture's route or
  component, viewport, color scheme, motion setting, checkout SHA, and port, or
  `render: unavailable` with its reason, plus the live address when one exists;
- review focus;
- the worker file for this axis, and for the antipattern axis the catalog path.

Return `BLOCKED` with the missing field when the packet cannot identify one
stable, non-empty UI target. Treat the packet as a pointer set. Inspect the
diff, the changed code, the authority files, and the captures directly before
deciding.

## Finding bar

A finding is a demonstrated design defect that this change introduces or makes
worse. It includes:

- the axis's classification or severity;
- the smallest useful changed `path:line`, plus the capture that shows the
  defect when it is visible;
- concrete evidence: the authority `path:line` on the drift axis, or the
  catalog id and the observed value on the antipattern axis;
- the UI consequence, meaning what a user sees, misreads, or cannot do;
- one required correction.

The drift axis classifies every UI-affecting hunk as `CONFORMS`,
`INTENTIONAL CHANGE`, `DRIFT`, or `NEEDS DECISION`. A `DRIFT` row is a finding.
The antipattern axis grades each finding `BLOCKING`, `MAJOR`, or `POLISH`. The
grade comes from the catalog entry unless the observed consequence demonstrates
a different one, and then the row says why.

Attribution comes before verdict. A defect proven present at the base is
pre-existing and is not a finding. The antipattern worker lists at most five
pre-existing defects on the changed screens under **Pre-existing**, without a
grade, so the developer can decide. A finding whose attribution the evidence
cannot settle carries `attribution: unproven`, and the coordinator decides.

Authority wins over the catalog. When a design authority in the packet requires
the pattern, the row is not a finding. The antipattern worker records it under
**Suppressed** with the authority `path:line`. A preference without repository
authority is a decision on the drift axis, and on the antipattern axis it is a
finding only when a catalog entry names it.

Return high-conviction findings only. A guess from code about how something
renders, when a capture could have settled it, is not evidence. When the render
is unavailable, a code-only antipattern finding cites the exact value or
structure in the diff that produces it and carries `code-only`. Skip a
violation the mechanical gate already reported unless a distinct consequence
remains.

Report the smallest set of findings that covers the distinct defects. When
several share one root cause, such as one token or one shared primitive,
report the cause once at the location that owns it. One strong finding
outranks several weak ones.

## Output

The drift worker returns exactly:

```markdown
## Verdict
PASS | FAIL | NEEDS DECISION | BLOCKED

## Coverage
| Changed path:line | Classification | Drift axis | Authority or precedent | Evidence |
| --- | --- | --- | --- | --- |
| ... |

## Findings
| Changed path:line | Authority path:line | Capture | UI consequence | Required correction |
| --- | --- | --- | --- | --- |
| ... |

## Decisions
| Question | Missing or conflicting evidence | Owner |
| --- | --- | --- |
| ... |

## Verification
- <inspection, command, or capture and result>
```

The antipattern worker returns exactly:

```markdown
## Verdict
PASS | FAIL | BLOCKED

## Findings
| Grade | Catalog id | Changed path:line | Capture | Evidence | UI consequence | Required correction |
| --- | --- | --- | --- | --- | --- | --- |
| ... |

## Polish
| Catalog id | Changed path:line | Capture | Evidence | Suggested correction |
| --- | --- | --- | --- | --- |
| ... |

## Suppressed
| Catalog id | Authority path:line | Why the authority requires it |
| --- | --- | --- |
| ... |

## Pre-existing
| Catalog id | Location | Evidence |
| --- | --- | --- |
| ... |

## Coverage
| Category | Checked against | Result |
| --- | --- | --- |
| ... |

## Verification
- <inspection, command, or capture and result>
```

Use `none` as the only row of an empty table. On the drift axis, `FAIL`
requires at least one `DRIFT` row, `NEEDS DECISION` requires no `DRIFT` row and
at least one decision, and `PASS` requires only `CONFORMS` or
`INTENTIONAL CHANGE` rows. On the antipattern axis, `FAIL` requires at least
one `BLOCKING` or `MAJOR` finding, and `POLISH` rows never change the verdict.
`BLOCKED` names the unavailable input or proof. Do not include praise, summary
prose, repair patches, or findings owned by the other axis.
