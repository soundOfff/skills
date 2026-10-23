---
name: whats-next
description: >-
  Suggests the 3 most impactful next actions from the developer's full context: git,
  open pull requests and review requests, the issue tracker, flow ledgers waiting on
  their next stage, and the current conversation. Prioritizes blockers, unblocked items,
  and momentum. Use when deciding what to work on next or after finishing a task.
argument-hint: [optional focus area]
disable-model-invocation: true
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
  - Grep
---

# What's Next

Surface the 3 most impactful things to do right now based on all available context. `$ARGUMENTS` is an optional focus area, such as a path, an issue id, or a word like "cleanup".

## Steps

### 1. Detect session context

Before gathering external context, determine whether this conversation has an **active task in progress**. Session context exists when ANY of these are true:

- There are uncommitted changes in the working tree (`git diff --stat` returns output)
- There are staged but uncommitted changes (`git diff --cached --stat` returns output)
- The current conversation has prior tool calls (files read, edits made, commands run)
- A pull request was recently created or merged in this session
- A flow stage handed control back in this session (see [lifecycle.md](../flow-mode/references/lifecycle.md))
- A skill or process was planned or designed but not yet implemented

**Set `HAS_SESSION_CONTEXT = true`** if any of the above are detected. This flag controls scoring behavior in step 3.

### 2. Gather context (parallel where possible)

Skip any source that fails or does not exist in this repository.

**Git.** Current branch, `git status --short`, `git diff --stat`, `git diff --cached --stat`, `git log --oneline -5`, and ahead or behind upstream.

**Pull requests**, through the forge CLI (`gh` on GitHub, `glab` on GitLab):

- Your open pull requests, with their review state and check status (`gh pr list --author @me --state open --limit 10`)
- Review requests waiting on you (`gh pr list --search "review-requested:@me" --state open --limit 5`)

**Issue tracker**, only when `docs/agents/issue-tracker.md` exists. Use the read and list operations in `issue-tracker.md` `## Operations`, and `issue-tracker.md` `## Board` only when the file has one:

- Issues assigned to you that are in progress, in review, or blocked
- Recently updated issues assigned to you

**Flow ledgers**, only when the shared [`.flow/` folder](../flow-mode/references/lifecycle.md#where-ledgers-live) exists. Read the `status` of each ledger under `features/`, `issues/`, `builds/`, and `prs/`. A ledger is waiting when its status is one of these. Skip a ledger whose work already has a ledger at a later stage.

| Ledger status | Next action |
| --- | --- |
| feature `awaiting-confirmation` | Confirm the feature map in `/flow-create` |
| feature `ready-for-issue` | `/flow-to-issues` |
| issues `awaiting-approval` | Review and approve the issue drafts |
| issues `approved`, `publishing`, or `partial` | Resume `/flow-to-issues` to finish publishing |
| issues `published` | `/flow-build <issue>`, or implement the issue directly |
| build `needs-decision` or `blocked` | Answer the recorded decision or clear the blocker |
| build `planning`, `building`, or `verifying` | Resume `/flow-build <issue>` |
| build `awaiting-to-pr` | `/flow-to-pr <issue>` |
| pr `preflight`, `publication-ready`, `needs-decision`, or `blocked` | Resume `/flow-to-pr <issue>` |
| pr `published` | `/flow-code-check`, plus `/flow-design-check` for UI changes |

**Session context:**

- What was discussed in the current conversation
- Decisions made, actions completed, pending items
- Files modified or investigated

### 3. Score and rank

#### Session-aware scoring

When `HAS_SESSION_CONTEXT = true`, apply these rules BEFORE general scoring. The current session's work should almost always be suggestion #1:

| Session signal | Auto-suggestion | Priority |
|---|---|---|
| Uncommitted changes on current branch | "Commit your changes and open a pull request" (`/flow-to-pr <issue>` for tracked work) | Force #1 |
| A flow stage just handed control back | The nudge that [lifecycle.md](../flow-mode/references/lifecycle.md) gives for that stage | Force #1 |
| Pull request was just created or merged | "Verify the deployment, close the tracked issue, or check staging" | Force #1 |
| A skill, plan, or design was just discussed | "Implement the planned changes" (`/flow-to-issues` first when the repository tracks work) | Force #1 |
| Active file edits in conversation (no uncommitted git changes) | "Continue: [describe the in-progress task from conversation]" | Force #1 |

Only ONE of the above becomes #1 (pick the most specific match). Slots #2 and #3 are filled from general scoring below.

When `HAS_SESSION_CONTEXT = false` (fresh conversation, no prior work), skip this section entirely and use general scoring for all 3 slots.

#### General scoring

For each potential action, score using weighted signals:

| Signal | Weight (no session context) | Weight (with session context) | Examples |
|---|---|---|---|
| Blocking others | 5 | 5 | Approved pull request not merged, review requested from you, issue blocking another |
| Just unblocked | 4 | 4 | Blocker resolved, failing checks now pass, ledger waiting on your decision |
| Active momentum | 3 | **5** | On related branch, uncommitted changes, current task |
| Staleness | 2 | 2 | Pull request open >2 days, issue in progress >3 days, ledger untouched >2 days |
| Approaching deadline | 2 | 2 | Due date within 3 days, iteration ending |
| Recency | 1 | 1 | Recently updated, from current session |

If a focus area is given in `$ARGUMENTS`, boost matching items, but still show high-scoring non-matches such as blockers.

### 4. Present top 3

```
What's next for you:

1. [Action title]
   [Why: one sentence connecting to context]
   → [Concrete next step]

2. [Action title]
   [Why]
   → [Next step]

3. [Action title]
   [Why]
   → [Next step]
```

Each card has an imperative action title, the real signal behind it, and a literal command or action.

When session context was detected, add a note after #1:
`(continuing from this session)`

### 5. Offer interaction

Use **`AskUserQuestion`** (multiSelect: false), or ask in plain text when the harness has no question tool:

- "Execute #1" / "Execute #2" / "Execute #3"
- "Expand details" (full context for all 3)
- "Refresh" (re-gather and re-rank)
- "Skip all"

**If executing.** Announce, execute, report, then offer updated suggestions. A pick that names a human-invoked skill counts as the developer invoking it, so read that skill's `SKILL.md` and follow it.
**If expanding.** Show links, related issues, ledgers, files, and the full reasoning.

## Principles

- **3 items max.** More options cause decision fatigue.
- **Session continuity first.** When there's active work in the conversation, the #1 suggestion MUST relate to finishing or advancing that work.
- **Actionable, not informational.** Every suggestion has a clear next step.
- **Context-first.** Connect signals the developer might miss, such as a merged pull request that unblocks a Ready issue.
- **No repeats.** Don't re-suggest dismissed or completed items in the same session.
- **Show reasoning.** Briefly explain WHY each item is suggested.
- **Be fast.** Gather context in parallel, and don't over-read.
