# Issue tracker: GitHub

Issues for this repository live in GitHub Issues on the repository the `origin` remote points at. Use the `gh` CLI, which infers the repository from the git remote, and fills `{owner}` and `{repo}` in a `gh api` path. When a command fails on access, `gh auth status` shows which account is active.

{{authorization_gate}}

## Operations

- **Create.** `gh issue create --title "<title>" --body-file <file>`. Write the body to a file first so multi-line text survives.
- **Read.** `gh issue view <n> --comments`, or `gh issue view <n> --json number,title,body,state,labels,assignees,comments` for parsing.
- **List.** `gh issue list --state open --json number,title,labels,assignees --limit 200`, narrowed with `--label` and `--search`. Use `--state all` when checking for duplicates.
- **Comment.** `gh issue comment <n> --body-file <file>`.
- **Label.** `gh issue edit <n> --add-label "<label>"`, or `--remove-label "<label>"`. `gh label list` shows the labels that exist. Creating a label is a create and passes the authorization gate first.
- **Close.** `gh issue close <n> --comment "<reason>"`, adding `--reason "not planned"` when dropping work. The pull request body carries the `Closing reference` setting from `AGENTS.md` `## Settings`. Merging that pull request closes the issue as completed.
- **Set parent.** Native sub-issues, linked by GraphQL node ids: `gh api graphql -f query='mutation { addSubIssue(input: { issueId: "<parent-node-id>", subIssueId: "<child-node-id>" }) { issue { number } } }'`. Read a node id with `gh issue view <n> --json id --jq .id`. Where sub-issues are unavailable, put `Part of #<parent>` at the top of the child body and add the child to a task list in the parent.
- **Add dependency.** Native issue dependencies: `gh api --method POST repos/{owner}/{repo}/issues/<child>/dependencies/blocked_by -F issue_id=<blocker database id>`. Read the database id with `gh api repos/{owner}/{repo}/issues/<blocker> --jq .id`. It is neither the issue number nor the node id. Mirror each edge as a `Blocked by #<n>` line in the child body. Where native dependencies are unavailable, the line alone records the edge. An issue is unblocked when every blocker is closed.
- **Assign.** `gh issue edit <n> --add-assignee @me`. Never replace another assignee.
- **Set status.** GitHub Issues has no status field. Open and unassigned means to do, open and assigned means in progress, and closed means done. When this file has a `## Board`, also set the board's status field.

## Claiming work

1. Before work starts, the issue exists, sits where `## Hierarchy` in `docs/agents/ticket-standard.md` places it, passes the Definition of Ready, and is assigned to you. The claim is the first write of the session.
2. When work starts, set the status to in progress.
3. The pull request carries the closing reference.
4. On merge, the issue closes as completed.
5. A feature parent closes only when every child is completed and its aggregate acceptance criteria pass.
6. Deferred work found along the way goes through the authorization gate. Surface its title and reason, and create it only after approval.
