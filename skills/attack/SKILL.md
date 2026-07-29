---
name: attack
description: Grab a ready issue and drive it to a merged PR — one vertical slice, TDD-style. Use when the user wants to "attack" an issue, "grab"/"pick up"/"take" the next ticket, "implement issue #N", or just says "attack" / "go" with an issue reference.
---

# Attack

Pick up a triaged issue and take it to an open PR.

## 1. Pick the issue

If the user named one, use it. If not, grab the oldest issue with the ready label:

```bash
gh issue list --label "<ready-label>" --state open \
  --json number,title,createdAt --limit 20
```

Tell the user which issue you picked before starting.

## 2. Branch

```bash
git switch -c <feat|fix|chore>/<issue-number>-<short-kebab-summary>
```

## 3. Build it

Read the issue body and any comments, then implement. Work test-first:

1. **Red** — write a failing test.
2. **Green** — write the minimum code to pass.
3. **Refactor** — clean up with tests green.

Commit at each green → refactor boundary.

## 4. Verify

Run the repo's full check suite (tests, typecheck, lint, build) before opening a PR.

## 5. Open the PR

```bash
git push -u origin HEAD
gh pr create \
  --title "<concise title>" \
  --body "Closes #<n>.

## What
<one paragraph>

## Verification
<commands run + result>"
```

## Stop conditions

Ask the user (don't guess) if:

- The issue is ambiguous or contradicts the codebase.
- It's blocked by an unfinished dependency.
- A check fails for a reason you can't attribute to your own change.
- You'd need a destructive git op (`--force`, `reset --hard`, etc.).
