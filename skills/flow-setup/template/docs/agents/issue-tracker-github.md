# Issue tracker: GitHub

Issues for this repository live in GitHub Issues on `{{repo}}`. Use the `gh` CLI, which infers the repository from the git remote. When a command fails on access, `gh auth status` shows which account is active.

## Authorization gate

Creating tracker items is deny-by-default. What becomes tracked work is the maintainer's decision, made item by item.

Never create an issue, a parent, a label, or a milestone without explicit authorization. Authorization is a message from the user that asks for this item, and the test is that you can quote it. An audit finding, deferred work, a standing doc line, or an existing branch is not authorization. `/flow-to-issues` authorizes local drafting only. It publishes after the user approves the exact issue set and hierarchy.

Findings that surface mid-task go to one of two places, and both leave the tracker untouched. Report them in the conversation, proposing a title and a one-line reason, then wait. Or add them to the ticket already in hand, as a Follow-ups section in a body you were asked to write.

The operations below are mechanics for after authorization.

## Operations

- **Create.** `gh issue create --title "<title>" --body-file <file>`. Write the body to a file first so multi-line text survives.
- **Read.** `gh issue view <n> --comments`, or `gh issue view <n> --json number,title,body,state,labels,assignees,comments` for parsing.
- **List.** `gh issue list --state open --json number,title,labels,assignees --limit 200`, narrowed with `--label` and `--search`. Use `--state all` when checking for duplicates.
- **Comment.** `gh issue comment <n> --body-file <file>`.
- **Label.** `gh issue edit <n> --add-label "<label>"`, or `--remove-label "<label>"`. `gh label list` shows the labels that exist. Creating a label is a create and passes the authorization gate first.
- **Close.** `gh issue close <n> --comment "<reason>"`, adding `--reason "not planned"` when dropping work. The closing reference is `Closes #<n>` in a pull request body. Merging that pull request closes the issue as completed.
- **Set parent.** Native sub-issues, linked by GraphQL node ids: `gh api graphql -f query='mutation { addSubIssue(input: { issueId: "<parent-node-id>", subIssueId: "<child-node-id>" }) { issue { number } } }'`. Read a node id with `gh issue view <n> --json id --jq .id`. Where sub-issues are unavailable, put `Part of #<parent>` at the top of the child body and add the child to a task list in the parent.
- **Add dependency.** Native issue dependencies: `gh api --method POST repos/{{repo}}/issues/<child>/dependencies/blocked_by -F issue_id=<blocker database id>`. Read the database id with `gh api repos/{{repo}}/issues/<blocker> --jq .id`. It is neither the issue number nor the node id. Mirror each edge as a `Blocked by #<n>` line in the child body. Where native dependencies are unavailable, the line alone records the edge. An issue is unblocked when every blocker is closed.
- **Assign.** `gh issue edit <n> --add-assignee @me`. Never replace another assignee.
- **Set status.** GitHub Issues has no status field. Open and unassigned means to do, open and assigned means in progress, and closed means done. When this file has a `## Board`, also set the board's status field.

## Claiming work

1. Before work starts, the issue exists, sits where `## Hierarchy` in `docs/agents/ticket-standard.md` places it, passes the Definition of Ready, and is assigned to you. The claim is the first write of the session.
2. When work starts, set the status to in progress.
3. The pull request carries the closing reference.
4. On merge, the issue closes as completed.
5. A feature parent closes only when every child is completed and its aggregate acceptance criteria pass.
6. Deferred work found along the way goes through the authorization gate. Surface its title and reason, and create it only after approval.
