---
name: create-pr
description: Create a GitHub PR for the current branch with a structured body (brief description, testing points, how to test, what's missing) and attach Playwright screenshots of the change as a PR comment. Use when the user asks to create, open, or ship a PR, or says "make a PR" / "PR this branch".
---

# Create PR

Open a GitHub PR for the current branch with a structured body and a screenshots
comment. Screenshots stay local — the user drags them into the comment on GitHub —
so nothing extra is ever pushed to the repo.

## Workflow

1. **Preflight**
   - `gh auth status` must succeed and the repo must have a GitHub remote.
   - If on the default branch, create a feature branch for the pending work first.
   - Confirm there is a diff vs the default branch (committed or pending); abort with
     a clear message if there is nothing to PR.

2. **Commit and push everything**
   - Stage all pending changes and commit with a Conventional Commit message derived
     from the diff (`feat:`, `fix:`, …). Split into atomic commits if the pending work
     clearly mixes concerns.
   - `git push -u origin <branch>`.

3. **Understand what the branch actually did — before opening any browser**
   - Review `git log <default>..HEAD --oneline` and `git diff --stat <default>...HEAD`
     to map the change: which user-facing capabilities, screens, flows, and states
     were added or altered, in the project's domain vocabulary.
   - For large branches (many commits / many files), delegate this to an Explore
     subagent and ask for a summary of user-visible changes, not a file list.
   - This analysis drives both the shot list (next step) and the PR body sections.

4. **Write a prioritized shot list, then capture it with Playwright**
   - Rank candidates before capturing anything:
     1. The headline capability the branch exists for, in its most finished state.
     2. UI that is *new* in this branch, over screens that merely changed.
     3. States that prove behavior a reviewer would question (before/after,
        gated vs published, empty, error).
     4. Secondary touched screens — only if slots remain.
   - Keep 4–6 shots. Write each caption first; if you can't say why a reviewer
     cares, cut the shot. List order = image numbering = the story the comment tells.
   - Start the project's dev server if not already running (check project docs for
     the command, e.g. `bun run dev`); wait until it responds.
   - Use the Playwright MCP tools: `browser_resize` to a desktop viewport
     (e.g. 1440×900), `browser_navigate` to each screen, drive any state needed
     (clicks, forms), then `browser_take_screenshot`.
   - Save images to the session scratchpad with kebab-case names matching the list
     order: `01-<screen>.png`, `02-<state>.png` (no spaces — the names become URLs).
   - If the change has no UI surface (config, scripts, server-only), skip this and
     the comment step, and say so under "How to test".

5. **Create the PR** — `gh pr create` targeting the default branch, with this body:

   ```markdown
   ## Summary
   2–4 sentences: what changed and why.

   ## Testing points
   - Bullet list of the behaviors a reviewer should verify.

   ## How to test
   1. Numbered, copy-pasteable steps (commands, URLs, what to click, what to expect).

   ## What's missing
   - Known gaps, deferred work, follow-ups — or "Nothing".

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   ```

6. **Attach screenshots as a comment (manual image upload)**
   - GitHub hosts comment images only via drag-and-drop in the web UI (no API), and
     nothing extra should be pushed to the repo — so copy the final shot set to
     `~/Downloads/pr-screenshots/<branch-with-dashes>/` where the user can drag from.
   - `gh pr comment <pr-url> --body ...` with a `## Screenshots` section: for each
     image a short bold caption line followed by an italic placeholder naming its
     file, e.g. `*(drag `01-studio-editor.png` here)*`.
   - Tell the user the folder path and that they should edit the comment on GitHub
     and drop each file onto its placeholder — GitHub replaces it with a hosted
     user-attachment image.

7. **Report** — give the user the PR URL and mention the screenshots comment. Report
   honestly anything skipped or failed (e.g. a state you couldn't reach in the
   browser).

## Notes

- Never force-push the feature branch as part of this workflow.
- Never commit or push screenshots to the repo (no branches, tags, or releases for
  image hosting) — local files + drag-and-drop is the whole strategy.
- If `gh pr create` reports a PR already exists for the branch, update it instead:
  `gh pr edit --body ...` and still post/refresh the screenshots comment.
