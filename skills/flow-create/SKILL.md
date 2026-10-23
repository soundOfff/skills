---
name: flow-create
description: Build an evidence-backed feature map and reuse plan from a feature description. Dispatches code mapping, reuse auditing, design, and research roles, works the open decisions with the developer, and ends in an explicitly confirmed shared understanding. Use when a feature idea needs briefing before it becomes tracked issues.
disable-model-invocation: true
---

# Flow create

Turn the text after `/flow-create` into a build-ready feature map at
`.flow/features/<slug>.md`. If the input names an existing map, resume it. If no
description or map is supplied, ask for one and stop.

The feature map is the single source of briefing state. The main agent is its
only writer. Tracker mutation belongs to `/flow-to-issues`. Production code
belongs to `/flow-build`. Work in this skill is limited to the feature map,
settled domain docs and decision records, and a developer-requested isolated
prototype.

## 1. Open the map

Read `AGENTS.md` and `docs/agents/domain.md`. When `AGENTS.md` has no flow block
or `docs/agents/domain.md` is missing, stop and suggest `/flow-setup`. Derive a
stable kebab-case slug, create `.flow/features/`, and instantiate
[`FEATURE-MAP.md`](templates/FEATURE-MAP.md) when no matching map exists.
Preserve the user's feature description verbatim under **Request**.

Allowed states are `briefing`, `awaiting-confirmation`, and `ready-for-issue`.
Only an explicit human confirmation permits `ready-for-issue`.

Completion: one map exists, carries the original request, and has
`status: briefing` unless it was already confirmed.

## 2. Dispatch the baseline

Dispatch the Code Mapper and Reuse Auditor concurrently in isolated contexts
using the dispatch contract in
[`dispatch.md`](../flow-mode/references/dispatch.md).

Both roles are read-only and return evidence to the main agent. The Reuse
Auditor performs its search before seeing the Code Mapper's conclusions. Both
independent reports are prerequisites for `ready-for-issue`.

The coordinating context never searches the codebase itself. Every role in this
skill is dispatched as the agent type that
[`dispatch.md`](../flow-mode/references/dispatch.md) `## Roles` names for the
current harness.

The coordinator keeps synthesis, the Reuse Gate, the frontier, and every write
to the map.

Completion: both reports cover every requirement currently visible in the map,
or name the precise evidence still missing.

## 3. Route required investigations

After consolidating the baseline, dispatch the applicable roles:

- Any rendered interface, interaction, copy, responsive behavior, focus, or
  motion change requires the Design Mapper.
- Any load-bearing external library, API, standard, license, compatibility, or
  current-practice question requires the Researcher.
- A UI prototype runs only after the developer explicitly requests options.
  Dispatch it in an isolated worktree using the `prototype` skill and the
  Design Mapper's constraints. Record the options, developer verdict, and
  artifact pointer in the map.

Dispatch each role as step 2 does.

The main agent validates returned file pointers and sources, then writes only
validated conclusions and evidence pointers into the map.

Completion: every applicable role has returned. Non-applicable roles are marked
`not-applicable` with the observable reason.

## 4. Enforce the Reuse Gate

Every required behavior has at least one **Change surface** row and one **Reuse
map** row classified and proved by the classification contract in the
`flow-reuse-auditor` agent definition. Resolve Code Mapper and Reuse Auditor
disagreements with additional evidence. An unresolved disagreement fails the
gate.

Completion: every behavior is classified with `path:line` evidence and every
`NEW` row has a complete new-code proof.

## 5. Work the frontier

Maintain a decision tree in the map. Facts go to bounded AFK investigations,
which an agent settles without the developer. Decisions stay HITL, with the
developer. The **frontier** is every fact or decision whose prerequisites are
settled.

Run AFK frontier items concurrently when their scopes do not overlap. Each runs
as a dispatched Fact lookup or Researcher, never as a search in the
coordinating context. Ask the whole HITL frontier in one numbered round. For
each question include the recommendation, evidence, and meaningful consequence.
Wait for the developer, record the answers, recompute the tree, and repeat.

Apply `docs/agents/domain.md` and the `domain-modeling` skill's discipline as
terms settle. Update the domain language named in the `Domain language` row of
`## Sources of truth` in `AGENTS.md` inline. Add a decision record only when the ADR threshold
in `docs/agents/domain.md` is met.

Use this process at every feature size. Persist the map when the runtime ends.
The developer decides whether to pause or continue.

Completion: the frontier is empty, blocking unknowns are zero, and deliberate
deferrals and exclusions are explicit.

## 6. Confirm shared understanding

Run every item in **Ready-for-confirmation gate**. A failed item returns to its
owning step. When all items pass, write the compact outcome, scope, change
surface, reuse plan, decisions, edge cases, and verification under **Shared
understanding**. Set `status: awaiting-confirmation` and present that statement.

Ask the developer to confirm or correct it. A correction sets `status:
briefing`, clears any previous confirmation, and returns to the owning step.
Explicit confirmation records the exact response and timestamp, checks both
items in **Confirmation gate**, and sets `status: ready-for-issue`. Report the
map path, suggest `/flow-to-issues`, and return control to the developer. The
next human-only skill begins only through a new human invocation.

Completion: the map is either back in `briefing` with every correction routed,
or it contains the exact human confirmation and has `status: ready-for-issue`.
