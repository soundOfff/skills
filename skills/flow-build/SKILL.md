---
name: flow-build
description: Build one Ready issue through its review boundary. Claims the issue, creates one integration worktree, dispatches builder agents over a path-disjoint assignment graph, accepts each diff only with owned paths, reuse proof, and red-green evidence, runs the full gate once, and leaves a committed local branch for /flow-to-pr. Use when a Ready issue benefits from coordinated or parallel builders.
disable-model-invocation: true
---

# Flow build

Turn `/flow-build [issue number or URL]` into a locally committed PR integration
branch ready for `/flow-to-pr`. One invocation owns one work issue. Feature
parents are completion containers, not build targets.

The coordinator is the only writer to `.flow/builds/<issue>.md` and the only
committer. Implementation belongs to dispatched builder agents. The coordinator
and every builder share the future PR's integration worktree. `/flow-to-pr`
continues in that same lane. This skill may claim the existing issue and update
its existing board item. It creates no tracker item, pushes no branch, and
opens no PR.

Always read `docs/agents/ticket-standard.md`, `docs/agents/issue-tracker.md`
`## Claiming work`, the base branch in `docs/agents/pr-standard.md`
`## Lifecycle`, and the dispatch and capability routing in
[`dispatch.md`](../flow-mode/references/dispatch.md). When `AGENTS.md` has no
flow block or one of these files is missing, stop and suggest `/flow-setup`.
Builders follow [`builder.md`](references/builder.md). `dispatch.md` owns
capability routing. The `tdd` and `diagnose` skills own the loops they teach
once routed.

## 1. Resolve the work issue

Use the supplied issue number or URL. Without one, resolve the current branch
or worktree to an issue. If that yields none, list open work issues assigned to
the developer that carry the label `docs/agents/triage-labels.md` maps to the
`ready-for-agent` role. Continue only when exactly one candidate exists.
Otherwise present the candidates and wait for the developer's selection.

Fetch the issue, comments, parent, dependencies, assignee, labels, and any board
fields that `issue-tracker.md` `## Board` names. The newest explicit human
scoping comment is binding. Run `ticket-standard.md` `## Definition of Ready`
against the current issue and repository. A closed issue, feature parent, open
dependency, competing claim, or failed Ready item ends in `blocked` or
`needs-decision` before code changes.

Instantiate [`BUILD-PLAN.md`](templates/BUILD-PLAN.md). Its state machine is:

```text
planning → building → verifying → awaiting-to-pr
    └────────────→ needs-decision | blocked
```

A binding scope correction returns the plan to `planning` and invalidates all
affected assignments.

Completion: one eligible issue and its authoritative snapshot are recorded, a
selection is requested without mutation, or the plan records the exact failed
eligibility condition without a code change.

## 2. Claim and prepare the PR lane

Inspect current worktrees and branches, then fetch `origin/<base>`. Reuse the
current PR integration worktree when its ledger, branch, intended issue, and
changes all agree. Otherwise create the future PR's worktree once on
`issue-<number>-<slug>` from `origin/<base>`. Every implementation assignment
and the later `/flow-to-pr` invocation use this one worktree.

Claim the issue per `issue-tracker.md` `## Claiming work`. When `## Board`
exists, also set the status and dates it names for work start. Record the base
SHA, branch, worktree, actor, and claim evidence in the plan. Keep the branch
local.

Completion: the issue has one verified claim and one PR integration worktree
based on the fetched `origin/<base>`. The ledger points to both and names the
worktree as the lane for every assignment and `/flow-to-pr`.

## 3. Lock the execution graph

Revalidate every issue pointer against the worktree. Map every acceptance
criterion to one or more bounded assignments. Each assignment records:

- one observable completion criterion;
- exact owned paths and prohibited overlaps;
- dependency edges;
- the classification and proof required by the classification contract in the
  `flow-reuse-auditor` agent definition;
- `builder.md` plus every capability reference selected by the routing in
  `dispatch.md`;
- `TDD: required` with one public test seam and first red command, or one
  permitted exception with its pre-change and post-change proof;
- for a bug or performance regression, the exact symptom and red-capable loop
  command, or a preceding read-only diagnosis assignment that must produce it;
- targeted verification.

Apply TDD, bug-diagnosis, and capability routing before dispatch. The routing
rules and their complete exception set live in
[`dispatch.md`](../flow-mode/references/dispatch.md). A dispatch is invalid
until every triggered branch records its exact entry points and proof.

Any pair with a dependency edge or overlapping paths is queued. Disjoint,
unblocked assignments are parallel. A missing decision, stale acceptance
criterion, or unproved `NEW` destination sets `status: needs-decision` and
stops dispatch.

Completion: every item in **Dispatch gate** passes.

## 4. Work the frontier

Set `status: building`. Dispatch every unblocked, path-disjoint assignment
concurrently as the Builder role that `dispatch.md` `## Roles` names for the
current harness (`pstack:poteto-agent` under Claude Code). At least one builder
agent is required. Each prompt contains only the dispatch contract from
`dispatch.md`, the PR integration worktree path, owned paths, dependencies,
completion criterion, and selected capability references. A TDD assignment also
carries its public seam and first red command. An exception carries its
authorized class and required pre-change and post-change proof.

Builders edit the PR integration worktree and leave changes uncommitted. For
every report, inspect the diff directly. Accept it only when the diff stays
within owned paths, meets the assignment criterion, follows its reuse decision
and capability references, preserves repository boundaries, and passes
targeted verification. Required TDD work must show the assigned test failing
for the intended missing behavior before implementation and passing afterward.
Exception work must show its assigned pre-change and post-change proof. Send
failures back to the same builder with file and test evidence.

Bug work must also show the reported symptom in the red-capable loop, its
minimal reproduction, the confirmed cause, and cleanup of temporary
instrumentation. Treat a plausible but unconfirmed cause as a failed
assignment.

After acceptance, run the affected verification, make an atomic commit in the
repository's commit style, and record the commit and changed paths in
**Integration log**. The accepted assignment releases its dependants into the
next frontier. Repeat until the graph is exhausted. Changes outside issue scope
go to **Drift** and set `needs-decision`. Tracker publication remains with
`/flow-to-issues`. A tool or environment failure sets `blocked` with
reproducible evidence.

Completion: every assignment is accepted, every changed path traces to exactly
one assignment and issue criterion, every behavioral change carries red and
green evidence, every bug fix carries confirmed diagnosis evidence, and the
branch contains only recorded atomic commits.

## 5. Prove the review boundary

Set `status: verifying`. Fetch `origin/<base>`, rebase the issue branch, repair
within the locked scope, and refresh recorded commit SHAs. Re-run the issue's
Verification signal, prove every acceptance criterion, and run the full gate
from `AGENTS.md` `## Commands`. UI work also records the browser or human proof
required by the issue. A Browser QA dispatch per
[`browser-qa.md`](references/browser-qa.md) supplies that proof for UX-heavy
work. This is the single full-gate run. Builders used the `test-file` gate
during their cycles.

Stop at the issue's Review boundary. Record the current proof for the later PR
body. `/flow-to-pr` owns publication and may recommend optional review from the
resulting diff. It does not execute review skills. Run every item in
**Build gate**.

Completion: every item in **Build gate** passes, or the plan records the exact
failing proof and ends `blocked`.

## 6. Hand off

Record the branch, PR integration worktree, base and HEAD SHAs, commits, diff
summary, acceptance proofs, gate results, and UI proof under **Handoff**. Set
`status: awaiting-to-pr` and return control to the developer. `/flow-to-pr`
begins only through a new human invocation.

Completion: the plan is `awaiting-to-pr`, the local branch is committed and
unpushed, and the handoff contains every field required to reproduce its
claims.
