---
name: flow-to-pr
description: Publish one implemented, tracked issue as a correctly formatted pull request. Rebases on the base branch, pins the diff, writes the title and body from the repository's PR standard, pushes with a pinned lease, publishes in the repository's publish mode, and recommends review without running it. Use when a tracked issue's implementation reaches its review boundary, with or without a /flow-build handoff.
disable-model-invocation: true
argument-hint: '[issue number or URL]'
---

# Flow to PR

Run `/flow-to-pr [issue number or URL]` when implementation is ready to publish.
A `/flow-build` handoff is optional. This skill rebases, formats, pushes, and
creates one pull request in the repository's publish mode. It does not execute
review skills, run repair loops, mark a draft ready, merge the PR, or add an
auto-merge label.

The published pull request is the successful outcome. Review and validation
results may be missing without blocking publication. Report them honestly as
`not run`. Always read `docs/agents/pr-standard.md`,
`docs/agents/issue-tracker.md`, and the delivery lifecycle in
[`lifecycle.md`](../flow-mode/references/lifecycle.md). When `AGENTS.md` has no
flow block or either standard is missing, stop and suggest `/flow-setup`.

This skill publishes tracked work only. Untracked work ships through
`pstack:poteto-mode` and its Opening a PR playbook.

## 1. Resolve the publication lane

Resolve the supplied issue. Without one, select the only
`.flow/builds/<issue>.md` in `status: awaiting-to-pr` whose recorded worktree is
the current worktree. Any ambiguity requires the developer to select.

Fetch the issue, comments, parent, dependencies, assignee, and any board fields
that `issue-tracker.md` `## Board` names. Require an open work issue, not a
feature parent, with binding scope and a Review boundary.

- With a matching build handoff, require its branch and worktree to match the
  current lane. Treat its test, acceptance, and repository proof as reported
  evidence, not a publication gate.
- Without a handoff, use the current branch. Require a clean, committed branch
  other than the base branch from `pr-standard.md` `## Lifecycle`, and map the
  complete `origin/<base>...HEAD` diff to the issue. Do not create or backfill
  `.flow/builds/`.
- If the issue is unassigned, claim it for the authenticated actor per
  `issue-tracker.md` `## Claiming work`. Never replace another assignee. When
  `## Board` names a work status and a start date, set the status to its
  in-progress value and set the start date only when it is empty. Record the
  before and after values.

An unexplained hunk, conflicting owner, incompatible existing PR, scope change,
or missing product decision is `needs-decision`. Instantiate
[`PR-READINESS.md`](templates/PR-READINESS.md) and keep it under
`.flow/prs/<issue>.md`.

```text
preflight → publication-ready → published
        needs-decision | blocked
```

Completion: the issue, branch, worktree, scope, and ledger agree, or the exact
publication ambiguity is recorded without pushing.

## 2. Rebase and pin the target

Fetch `origin/<base>` and rebase the branch onto it. Resolve a conflict only
when the issue and integrated diff prove the result. A semantic choice is
`needs-decision`. Never merge the base branch into the branch.

Require `git rev-list --merges <base-sha>..HEAD` to return no commits. Record
the fetched base SHA, HEAD SHA, changed paths, and
`git diff --binary <base-sha>...<head-sha> | git hash-object --stdin`.

Inspect the pinned diff for scope and PR presentation. Do not run
`/flow-code-check`, `/flow-design-check`, `/flow-adv-review`, repository
validation, or repair agents. Record existing exact-target evidence when it is
available. Otherwise record `not run`.

Completion: the clean linear branch is rebased on the recorded base and every
hunk maps to the issue, or the exact conflict or scope decision is recorded.

## 3. Prepare the pull request

Build the title and body from the forge's pull request template that
`pr-standard.md` `## Body` names, when it exists, and from the rules in that
section. Write the prose per
`pstack:technical-writing` and `pstack:unslop`. The body must:

- lead with what changed and why;
- contain the closing reference in the tracker's syntax from
  `issue-tracker.md`, which for GitHub is `Closes #<issue>`;
- report known validation results without converting `not run` into success;
- disclose risk, diff-budget exceptions, and available UI evidence;
- leave review or validation items incomplete when they were not performed.

Run every item in **Publication gate** in the ledger. Missing review results,
test results, screenshots, or personal verification do not block publication.
A malformed title or body, missing issue link, dirty branch, scope mismatch,
nonlinear history, or stale base does.

Completion: the proposed title and body truthfully represent the pinned target
and every publication-integrity item passes.

## 4. Push and publish

Set `status: publication-ready`. Immediately before pushing, fetch
`origin/<base>` and compare it with the recorded base. If it changed, rebase and
return to step 2.

For a new remote branch, use a normal upstream push. For an existing remote
branch, read its exact SHA with
`git ls-remote --heads origin refs/heads/<branch>` and push with:

```text
git push --force-with-lease=refs/heads/<branch>:<expected-remote-sha> -u origin <branch>
```

Never retry with an unpinned lease. Create or update one pull request against
`<base>` in the publish mode from `pr-standard.md` `## Lifecycle`, which is
`draft` or `ready`, and `draft` when the section names none. An existing draft
stays a draft. Then verify its remote head SHA, base, draft state, title, body,
and closing reference. Record the PR number and URL and set
`status: published`.

Completion: the remote branch equals the pinned HEAD and one verified pull
request in the publish mode is recorded with `status: published`, or the exact
push or publication failure is recorded as `blocked`.

## 5. Recommend optional review

After the pull request exists, classify the actual diff and present
recommendations. Do not invoke them:

- recommend `/flow-code-check --base <base-sha>` when code, configuration,
  scripts, or executable tests changed;
- also recommend `/flow-design-check --base <base-sha>` when UI components,
  styles, design authority, or user-facing UI behavior changed;
- a documentation-only change gets no automatic review recommendation.

`/flow-adv-review` is human-invokable only. Never invoke it, add it to the
automatic recommendation set, or imply that it is required.

Optional review findings are advisory. This skill does not repair them,
rereview automatically, or block publication. The developer decides whether to
run a recommendation and what to do with its result.

Return:

```markdown
## Flow to PR: PUBLISHED | NEEDS DECISION | BLOCKED
Issue: <issue> · Target: <base>..<head> · PR: <url-or-not-created>
Publication: <draft, ready, or local-only>
Reported validation: <results or not run>
Recommended review: <commands or none>
Human next step: <review recommendation, personal verification, or merge decision>
```

Completion: one correctly formatted pull request in the repository's publish
mode represents the unchanged remote target, recommendations are reported
without execution, and no agent has marked a draft ready, merged it, or added an
auto-merge label.
