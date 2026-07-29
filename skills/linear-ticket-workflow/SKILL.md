---
name: linear-ticket-workflow
description: >-
  Skill for the full developer workflow: deciding what to work on next, taking Linear
  tickets, creating git branches, implementing fixes/features, and committing with
  conventional commit messages. Use this skill whenever the user provides a Linear ticket
  (URL, ID, or description) and wants Claude to implement the fix or feature, create the
  branch, make commits, and provide testing guidance. Triggers on phrases like "fix this
  ticket", "implement this Linear issue", "work on DEX-123", any Linear URL, or any
  reference to picking up a ticket or issue for development. Also triggers when the user
  pastes ticket details and expects code changes with proper git workflow. Also triggers
  on "what's next", "what should I work on", or any request to prioritize work.
argument-hint: [ticket ID, URL, or "what's next" with optional focus area]
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
  - Grep
  - WebFetch
  - Figma
  - mcp__claude_ai_Linear__get_issue
  - mcp__claude_ai_Linear__list_issues
  - mcp__claude_ai_Linear__create_issue
  - mcp__claude_ai_Linear__update_issue
  - mcp__claude_ai_Linear__list_teams
  - mcp__claude_ai_Linear__list_projects
  - mcp__claude_ai_Linear__list_issue_labels
  - mcp__claude_ai_Linear__list_issue_statuses
  - mcp__claude_ai_Linear__create_comment
  - mcp__claude_ai_Linear__list_comments
---

# Linear Ticket Workflow

This skill handles two modes:

1. **"What's next" mode** — Suggests the 3 most impactful next actions based on full developer context (git state, Linear backlog, PRs, conversation history). Prioritizes blockers, unblocked items, and momentum.
2. **Ticket implementation mode** — Full developer workflow from Linear ticket to committed code with testing guidance. Covers branch creation, implementation, atomic conventional commits, and test case generation.

## Available Integrations

The user has the following MCP integrations available. Use them proactively:

- **Linear MCP** — Fetch tickets, update statuses, list issues, add comments. Use this to pull ticket details, check what's assigned, and update ticket status as work progresses.
- **Figma MCP** — Reference designs when tickets involve UI work. Pull design specs, inspect components, and verify implementation matches designs.
- **GitHub** — Read repo state, branches, PRs, and diffs. **NEVER push to remote** — the user handles all pushes manually. You may read, branch, commit locally, and check PR status, but `git push` is strictly forbidden.

---

## Mode A: "What's Next"

Trigger: user says "what's next", "what should I work on", "prioritize my work", or similar.

### Gather Context

1. **Git state** — Check current branch, uncommitted changes, recent commits. Is there WIP that should be finished first?
2. **Linear backlog** — Use Linear MCP to list issues assigned to the user. Filter by status (In Progress > Todo > Backlog). Check for blockers and dependencies.
3. **PR state** — Check GitHub for open PRs that need review or have review comments to address.
4. **Conversation history** — Consider what was just discussed or completed in the current session.

### Prioritization Logic

Rank by this priority order:
1. **Finish WIP** — If there's uncommitted work or an in-progress branch, suggest completing it first.
2. **Unblock others** — PR reviews requested from the user, or tickets blocking teammates.
3. **Address PR feedback** — Open PRs with unresolved review comments.
4. **In Progress tickets** — Tickets the user already started but hasn't finished.
5. **High priority unblocked tickets** — Urgent/high-priority tickets in Todo status with no blockers.
6. **Momentum plays** — Quick wins or tickets related to what was just completed.

### Output Format

Present exactly 3 suggestions, ranked. For each:

```
### 1. [Type emoji] Short action title
**Ticket:** DEX-1234 — "Ticket title"
**Why now:** One sentence explaining the priority reasoning.
**Effort:** Quick win / Medium / Deep work
**First step:** Concrete next action (e.g. "checkout branch X and pick up where you left off" or "create branch feat/dex-1234-...")
```

Type emojis: 🔥 blocker/urgent, 🔄 PR/review, 🚀 feature, 🐛 bug fix, 🧹 chore/cleanup

If the user provides an optional focus area (e.g. "what's next on mail-merge"), filter suggestions to that area.

After presenting suggestions, wait for the user to pick one. If they pick a ticket, transition into **Mode B** below.

---

## Mode B: Ticket Implementation

### Workflow Overview

1. Parse the ticket(s) — extract ticket number, title, and type (feat/fix)
2. **Create the git branch FIRST** — before any code changes
3. Implement the changes
4. Commit with conventional commits (atomic, grouped by functionality)
5. If multiple tickets: create a PR-ready branch with ticket refs in commits
6. Output a list of manual testing cases

### Step 1: Parse the Ticket(s)

Extract from whatever the user provides (Linear URL, ticket ID, description, or pasted ticket body):

- **Ticket number**: e.g. `DEX-1234`
- **Ticket title**: the human-readable summary
- **Type**: determine if it's a `feat` or `fix` based on the ticket content. Bug reports, error corrections, regressions → `fix`. New functionality, enhancements, additions → `feat`.

If the user provides a Linear URL or ticket ID, use the **Linear MCP** (`get_issue`) to fetch full details including description, labels, priority, and any linked issues. Don't rely on just the title — the description often has critical context.

If the ticket references a Figma design, use the **Figma MCP** to pull the relevant design details before implementing.

If the user provides multiple tickets, parse all of them. Track each separately — they'll share a branch but get individual commit references.

### Step 2: Create the Git Branch FIRST

**This must happen before any code changes.** Check git status, ensure a clean working tree, then branch.

Branch naming convention:

```
(feat|fix)/dex-<ticket_number>-<kebab-case-title>
```

Rules:
- Use the type (`feat` or `fix`) determined from the ticket
- Ticket number is lowercase: `dex-1234`
- Title is kebab-case, lowercase, concise (drop filler words if the title is very long)
- If multiple tickets, use the primary/first ticket for the branch name

**Examples:**
- Ticket DEX-456 "Add bulk export for contacts" → `feat/dex-456-add-bulk-export-for-contacts`
- Ticket DEX-789 "Fix crash when deleting empty group" → `fix/dex-789-fix-crash-deleting-empty-group`

Commands:
```bash
# Check state first
git status
git branch --show-current

# Branch from the right base (usually main or develop)
git checkout main && git pull  # only if network allows
git checkout -b <branch-name>
```

If the repo is dirty or on an unexpected branch, **stop and notify the user** before proceeding. Do not stash or commit unrelated changes without permission.

### Step 3: Implement the Changes

Read the codebase as needed to understand the architecture before making changes. Focus on:

- Understanding the existing patterns in the codebase
- Making minimal, targeted changes that address the ticket
- Not introducing unrelated refactors unless the ticket calls for it
- If the ticket has a Figma link or involves UI, reference the **Figma MCP** to match design specs

### Step 4: Commit with Conventional Commits

This is critical — follow these rules exactly:

#### Commit message format
```
type(scope): short description
```

Following [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

- **type**: `feat` or `fix` (match what the change actually does, not necessarily the ticket type)
- **scope**: the part of the codebase that changed, e.g. `contacts`, `groups`, `api`, `db`, `auth`, `ui`, `mail-merge`
- **description**: lowercase, imperative mood, one line, no period at the end

#### Commit rules

1. **One line only** — no multi-line commit messages, no body, no footer
2. **No Claude signature** — never add "Generated by Claude", "Co-authored-by: Claude", or any AI attribution in commit messages or code comments
3. **Atomic commits** — each commit should represent one logical unit of work. Separate by functionality:
   - Schema/migration changes get their own commit
   - Backend logic changes get their own commit
   - Frontend/UI changes get their own commit
   - Test changes get their own commit
   - Config changes get their own commit
4. **Multiple tickets** — when working on more than one ticket, include the ticket reference in the commit message: `fix(contacts): handle null email on merge DEX-789` or group commits so it's clear which ticket each one addresses. Aim for at least one commit per ticket.

#### Examples

```
feat(contacts): add bulk export endpoint for contact lists
fix(groups): prevent crash when deleting empty group
feat(mail-merge): expand template variables with company and title
fix(api): validate custom field values before save
feat(db): add categories column to autocomplete custom fields
```

#### How to commit

Stage and commit related files together. Do NOT use `git add .` blindly — be intentional:

```bash
git add <specific-files>
git commit -m "type(scope): description"
```

**NEVER run `git push`.** The user handles all pushes manually.

### Step 5: Multiple Tickets → PR-Ready

When the user passes more than one ticket:

- All work goes on one branch (named after the primary ticket)
- Each ticket's changes should be traceable through commits (include ticket numbers)
- After all commits, give the user a summary suitable for a PR description:
  - List of tickets addressed
  - Brief description of changes per ticket
  - Any notes on architectural decisions

### Step 6: Testing Cases

After all implementation and commits are done, provide a numbered list of **manual testing cases** the user should verify. These should be specific and actionable.

Do NOT run the tests yourself. The user will test manually.

Format:
```
## Testing Cases

1. **[Area] — What to test**
   - Steps to reproduce / verify
   - Expected result

2. **[Area] — What to test**
   - Steps to reproduce / verify
   - Expected result
```

Cover:
- Happy path for each change
- Edge cases mentioned in the ticket
- Regression scenarios (things that should still work after the change)
- If there are multiple tickets, group testing cases by ticket

---

## Important Reminders

- **Branch first, always.** Never start editing files before creating the feature/fix branch.
- **Never `git push`.** All pushes are done by the user manually.
- Always check the current git status and branch before starting work
- Use **Linear MCP** to fetch ticket details and update status as you work
- Use **Figma MCP** when tickets involve UI/design work
- Use **GitHub** (read-only) to check PR status, review comments, and branch state
- If the codebase uses a specific linter or formatter, run it before committing
- Never leave debug logs, console.logs, or TODO comments in committed code
- If you're unsure about an architectural decision, ask the user before proceeding
- The user knows their codebase — if something seems off, flag it rather than guessing
