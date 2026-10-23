---
name: flow-to-issues
description: Convert settled work into an approved issue hierarchy on the repository's issue tracker. Drafts locally, reconciles duplicates, proves coverage, cuts work at review horizons, and publishes only after the developer approves the exact hierarchy. Use when a confirmed feature map, a named plan, an existing issue, or the current conversation should become Ready issues.
disable-model-invocation: true
---

# Flow to issues

Convert the input after `/flow-to-issues` into build-ready issues on the
repository's tracker. Accept a confirmed feature map, another named document, an
existing issue, or the current conversation. Keep drafts at
`.flow/issues/<slug>.md` in the shared
[ledger folder](../flow-mode/references/lifecycle.md#where-ledgers-live).
Tracker publication requires approval of the exact hierarchy.

The repository standards are authoritative:

- Always read `docs/agents/ticket-standard.md`,
  `docs/agents/issue-tracker.md`, and the `Ready label` setting in `AGENTS.md`
  `## Settings`.
- Read `docs/agents/pr-standard.md` for code-bearing work.

When `AGENTS.md` has no flow block or `ticket-standard.md` or `issue-tracker.md`
is missing, stop and suggest `/flow-setup`.

Publication is deny-by-default under `issue-tracker.md`
`## Authorization gate`. Invoking this skill authorizes local drafting only.
Every tracker write waits for approval of the exact issue set and hierarchy.

This skill owns only source conversion, sequencing, gates, and local state. The
standards own ticket content, tracker mechanics, hierarchy, board fields,
titles, and PR rules.

## 1. Resolve the source

An explicit path or issue wins. Otherwise use the current conversation. A
feature map is authoritative only with `status: ready-for-issue`. Preserve its
confirmed requirements, exclusions, reuse decisions, decision records, and
binding human language.

Instantiate [`ISSUE-PLAN.md`](templates/ISSUE-PLAN.md). A plan already in
`publishing` or `partial` resumes at step 7. Its state machine is:

```text
draft → awaiting-approval → approved → publishing → published
                         ↘ rejected                ↘ partial
```

Edits to an approved plan return it to `draft` and clear its approval. When a
feature still has unresolved decisions, record those gaps in the draft and end
with a recommendation that the developer invoke `/flow-create`. Atomic work and
already-settled inputs proceed directly.

Completion: the local plan exists and either records every authoritative source
and conflict, or records the exact missing decisions and ends in `draft`.

## 2. Preflight read-only

Resolve the repository, tracker account, write access, destinations, labels,
native parent support, and native dependency support with the operations in
`issue-tracker.md` `## Operations`. When `issue-tracker.md` has a `## Board`,
also resolve the board and every field and value it names. Search open and
closed issues for the same work. Record each query, match, and proposed
disposition in **Duplicate reconciliation**.

Keep the tracker unchanged. A missing label, including the `Ready label`, a
missing write scope, or a board value or container named by `issue-tracker.md`
`## Board` is a separate approval item in the plan. Native
parentage is required for every published issue that `ticket-standard.md`
`## Hierarchy` places under a parent.

Completion: every destination is existing or explicitly proposed for separate
approval, and every duplicate match has a non-mutating disposition.

## 3. Prove coverage and choose the hierarchy

Normalize the source into explicit and repository-required outcomes. In
**Source coverage**, map every owned slice of each outcome to a work item and
map every work item back to at least one outcome or repository requirement.

Choose exactly one of the atomic, feature parent, or existing-parent hierarchy
shapes defined by `ticket-standard.md` `## Hierarchy`.

The coverage map authorizes integration, acceptance, review, and coordination
work items when they are delivery work. Native dependencies express sequence.
Issue titles describe outcomes.

Completion: the coverage map has no uncovered outcome, overlapping slice, or
orphan work item, and the local hierarchy has one valid shape.

## 4. Cut at review horizons

Apply the review horizon rule in `ticket-standard.md` `## Sizing` to every work
item, including an atomic item. Record the observable outcome and the reason
work must pause there. If an atomic item crosses a review horizon, split it and
use the feature hierarchy.

The issue boundary is the pause. After implementation, the builder stops and
the developer invokes `/flow-to-pr` to publish the correctly formatted pull
request. Review recommendations are derived from the actual PR diff after
publication, not prescribed as issue gates.

Completion: every work item has one verifiable outcome, one evidenced review
boundary, and no issue embeds an automatic review gate.

## 5. Draft and gate

Draft every work-item body to `ticket-standard.md` `## Template`. For feature
work, also draft the parent to `ticket-standard.md` `## Feature parent`. End
every body with its draft marker, `<!-- flow-draft: <plan-slug>/<Draft ID> -->`,
so a resumed publication can find what it already created. Every work item's labels
include the `Ready label` setting. Store the exact bodies in the local plan.
Resolve dependency edges to draft IDs and keep the graph acyclic.

Run `ticket-standard.md` `## Definition of Ready` over every work item and run
every item in the plan's **Draft gate**. A failure returns to its owning step.
Set `status: awaiting-approval` only when all drafts and gates pass.

Completion: every item in **Draft gate** passes and the plan is
`awaiting-approval`.

## 6. Approval gate

Present one compact row per proposed issue: title, parent, labels, blockers,
review boundary, verification, and any board fields that `issue-tracker.md`
`## Board` requires. Show existing issues to update and every separately
controlled label, board value, or container creation.

Record the response verbatim:

- exact approval sets `approved_at` and `status: approved`;
- edits set `status: draft`, clear approval, and return to the owning step;
- rejection sets `status: rejected`;
- an unanswered gate keeps `status: awaiting-approval` and the tracker
  unchanged.

Creation of a new label, board value, or container requires its own explicit
approval in addition to approval of the issue hierarchy.

Completion: the plan is `approved` with the exact approved bodies and
mutations, or it terminates as `rejected` or `awaiting-approval` without a
tracker write.

## 7. Publish and verify

Require `status: approved`, or `publishing` or `partial` when resuming.
Reconcile before any tracker write, on the first run and on every resume:

- Re-read every item already recorded in **Published issues**.
- List the items the authenticated actor created since `approved_at`, read
  their bodies, and match this plan's draft markers. A tracker search for the
  markers can find them faster, but an empty search result proves nothing,
  because search indexes lag behind writes. Record each found item that has no
  row yet.
- Repeat duplicate reconciliation. An item that carries this plan's marker is
  this plan's own, not a duplicate.
- Two items with the same marker are an unrepaired result. Record both under
  **Partial publication** for the developer.

Run every item in **Publish gate**, then set `status: publishing`. Create and
verify any separately approved label, board value, or container before the
issues that depend on it. Then create only the drafts that reconciliation did
not find. Take exactly one issue
branch:

- **Atomic.** Create the work issue. Attach it natively to its approved parent
  when `ticket-standard.md` `## Hierarchy` requires one.
- **Feature.** Create or verify the feature parent under its approved parent,
  if any. Then create child issues in dependency order and attach each to that
  parent. Update an existing parent's body only when that update was approved.

Each create sends the exact approved body, marker included. A work item's
create also applies its approved labels, the `Ready label` among them. Record
the draft ID, item id, and URL in **Published issues** immediately after each
create call returns, before the next tracker write.

Apply the approved dependency edges, any labels the create could not set, and,
when `issue-tracker.md` `## Board` exists, the approved board placement and
fields, using `issue-tracker.md` `## Operations`. Skip each one that a re-read
shows already in place. Re-read every issue and record verification of
parentage, labels, dependencies, board placement and fields, and exact body
content.

Successful verification sets `status: published` and records every URL. A
failed mutation is repaired within the approved scope. An unrepaired result
sets `status: partial` and records every successful mutation plus the exact
missing repair. Only a published plan is dispatchable.

Completion: the plan is `published` with every approved issue verified, or
`partial` with an exhaustive repair record. Report the dependency-ordered
frontier and return control to the developer. Downstream work begins only
through a subsequent human invocation.
