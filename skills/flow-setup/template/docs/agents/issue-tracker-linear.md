# Issue tracker: Linear

Issues for this repository live in Linear, in the team with key `{{linear_team}}`. Issue ids look like `{{linear_team}}-123`. Use the Linear MCP server's tools when the session has them. The tool names below are those of Linear's official MCP server. Another server or version may name them differently, so match each operation by purpose.

These need the user:

- Connecting the Linear MCP server. Its sign-in runs in a browser.
- Any operation the session has no tool for. Give the user the exact change to make in the Linear app, then confirm it with a read.
- Creating teams, workflow states, projects, or cycles.

## Authorization gate

Creating tracker items is deny-by-default. What becomes tracked work is the maintainer's decision, made item by item.

Never create an issue, a parent, a label, or a project without explicit authorization. Authorization is a message from the user that asks for this item, and the test is that you can quote it. An audit finding, deferred work, a standing doc line, or an existing branch is not authorization. `/flow-to-issues` authorizes local drafting only. It publishes after the user approves the exact issue set and hierarchy.

Findings that surface mid-task go to one of two places, and both leave the tracker untouched. Report them in the conversation, proposing a title and a one-line reason, then wait. Or add them to the ticket already in hand, as a Follow-ups section in a body you were asked to write.

The operations below are mechanics for after authorization.

## Operations

- **Create.** `create_issue` with the team `{{linear_team}}`, a title, and a Markdown description.
- **Read.** `get_issue` with the issue id, and `list_comments` for its comments.
- **List.** `list_issues`, filtered by team, state, label, assignee, or a text query. Include completed and canceled issues when checking for duplicates.
- **Comment.** `create_comment` with the issue id and a Markdown body.
- **Label.** `update_issue` with the issue's full label set. `list_issue_labels` shows the labels that exist. Creating a label (`create_issue_label`) is a create and passes the authorization gate first.
- **Close.** Comment with the reason, then use `update_issue` to move the issue to a completed state, or to canceled when dropping work. The closing reference is `Fixes {{linear_team}}-<number>` in the pull request description. With Linear's GitHub or GitLab integration installed, merging that pull request moves the issue to done. Without the integration, close it by hand after the merge.
- **Set parent.** `update_issue` on the child with its parent set to the parent's id. Sub-issues are native in Linear.
- **Add dependency.** Linear has native blocked-by relations. Set the relation with the session's tools when they support relations. Otherwise ask the user to add it in the app, from the child's relations menu. Mirror each edge as a `Blocked by {{linear_team}}-<n>` line at the top of the child description. An issue is unblocked when every blocker is completed.
- **Assign.** `update_issue` with the assignee set to you. `get_user` with `me` returns your user. Never replace another assignee.
- **Set status.** `update_issue` with the target workflow state. `list_issue_statuses` lists the team's states.

## Claiming work

1. Before work starts, the issue exists, sits where `## Hierarchy` in `docs/agents/ticket-standard.md` places it, passes the Definition of Ready, and is assigned to you. The claim is the first write of the session.
2. When work starts, set the status to the team's in-progress state.
3. The pull request carries the closing reference.
4. On merge, the issue moves to done.
5. A feature parent closes only when every child is completed and its aggregate acceptance criteria pass.
6. Deferred work found along the way goes through the authorization gate. Surface its title and reason, and create it only after approval.
