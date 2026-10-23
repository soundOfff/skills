---
plan: "<plan name>"
slug: "<plan-slug>"
status: draft
created_at: "<ISO-8601>"
updated_at: "<ISO-8601>"
approved_at: null
approval: null
---

<!-- status: draft | awaiting-approval | approved | rejected | publishing | published | partial -->

# Sources

| Source | Authority | Conflict or missing decision |
| --- | --- | --- |
| `<path, issue URL, or current conversation>` |  | none |

## Destination

| Repository | Tracker | Parent destination | Existing feature parent | Board |
| --- | --- | --- | --- | --- |
| `<owner/repo>` | `<GitHub, GitLab, Linear, or Local>` | none | none | none |

## Duplicate reconciliation

| Query | States searched | Match | Proposed disposition | Evidence |
| --- | --- | --- | --- | --- |
|  | open and closed | none | distinct |  |

## Source coverage

| Source ID | Required outcome or repository requirement | Owned slice | Work-item draft ID |
| --- | --- | --- | --- |
| S1 |  |  | W1 |

## Hierarchy

| Draft ID | Type | Title | Parent | Labels | Board fields |
| --- | --- | --- | --- | --- | --- |
| W1 | `feature-parent \| work-item` |  |  |  | none |

## Review horizons

| Work-item ID | Verifiable outcome | Review boundary and evidence | Code-bearing |
| --- | --- | --- | --- |
| W1 |  |  | yes |

## Dependencies

| Work-item ID | Blocked by | Acyclic proof |
| --- | --- | --- |
| W1 | none | root |

## Feature acceptance

- [ ] <aggregate observable outcome, or `not-applicable: atomic work`>
- [ ] <every child issue is closed as completed, or `not-applicable: atomic work`>

## Draft bodies

### <Draft ID> <title>

<exact feature-parent or work-item body>

## Draft gate

- [ ] Sources are authoritative and conflicts or missing decisions are explicit.
- [ ] Duplicate queries cover open and closed issues and record evidence.
- [ ] Every owned slice of every source outcome maps to one work item.
- [ ] No outcome slice has overlapping owners.
- [ ] Every work item maps to a source outcome or repository requirement.
- [ ] Work has exactly one shape from `ticket-standard.md` `## Hierarchy`.
- [ ] Every item has the parent `## Hierarchy` requires, existing or proposed for separate approval.
- [ ] When `issue-tracker.md` has a `## Board`, every item has the placement and fields it requires, and every new board value is proposed for separate approval.
- [ ] Every work item passes the Definition of Ready.
- [ ] Every work item has an evidenced review boundary.
- [ ] Dependency edges are real, native, and acyclic.
- [ ] No unadopted issue owns the same work.

## Approval

<verbatim approval, rejection, or `awaiting`>

### Separately controlled mutations

| Label, board value, or container | Required action | Approval |
| --- | --- | --- |
| none | none | not-applicable |

## Publish gate

- [ ] `status: approved` and `approved_at` is set.
- [ ] Exact bodies and mutations still match the recorded approval.
- [ ] Duplicate reconciliation was refreshed immediately before publication.
- [ ] Every separately controlled mutation has explicit approval.

## Published issues

| Draft ID | Issue | Parent verified | Board verified | Metadata verified | Body verified |
| --- | --- | --- | --- | --- | --- |
|  |  |  | not-applicable |  |  |

## Partial publication

`none`, or list every successful mutation and exact missing repair.
