# Issue tracker: GitLab

Issues for this repository live in GitLab Issues on `{{repo}}`. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI, which infers the project from the git remote. GitLab calls comments notes and pull requests merge requests.

## Authorization gate

Creating tracker items is deny-by-default. What becomes tracked work is the maintainer's decision, made item by item.

Never create an issue, a parent, a label, or a milestone without explicit authorization. Authorization is a message from the user that asks for this item, and the test is that you can quote it. An audit finding, deferred work, a standing doc line, or an existing branch is not authorization. `/flow-to-issues` authorizes local drafting only. It publishes after the user approves the exact issue set and hierarchy.

Findings that surface mid-task go to one of two places, and both leave the tracker untouched. Report them in the conversation, proposing a title and a one-line reason, then wait. Or add them to the ticket already in hand, as a Follow-ups section in a body you were asked to write.

The operations below are mechanics for after authorization.

## Operations

- **Create.** `glab issue create --title "<title>" --description "$(cat <file>)"`. Write the description to a file first so multi-line text survives.
- **Read.** `glab issue view <n> --comments`, or `glab issue view <n> -F json` for parsing.
- **List.** `glab issue list -F json`, narrowed with `--label` and `--search`. Add `--all` to include closed issues when checking for duplicates.
- **Comment.** `glab issue note <n> --message "<text>"`.
- **Label.** `glab issue update <n> --label "<label>"`, or `--unlabel "<label>"`. `glab label list` shows the labels that exist. Creating a label is a create and passes the authorization gate first.
- **Close.** `glab issue close` takes no comment, so post the reason with `glab issue note <n> --message "<reason>"` first, then run `glab issue close <n>`. The closing reference is `Closes #<n>` in a merge request description. Merging it into the default branch closes the issue.
- **Set parent.** Native parent links depend on the GitLab tier. The portable form is a `Part of #<parent>` line at the top of the child description plus a task list entry in the parent. Use a native epic or child link instead only when the project already uses one.
- **Add dependency.** Post the `/blocked_by #<blocker>` quick action as a note, `glab issue note <child> --message "/blocked_by #<blocker>"`. Native blocking links need a paid tier. Always mirror each edge as a `Blocked by #<n>` line at the top of the child description, which records the edge on every tier. `glab api projects/:id/issues/<n>/links` lists the native links. An issue is unblocked when every blocker is closed.
- **Assign.** `glab issue update <n> --assignee <username>`. `glab auth status` shows your username. Never replace another assignee.
- **Set status.** Open and unassigned means to do, open and assigned means in progress, and closed means done. When this file has a `## Board`, also apply the board's status label.

## Claiming work

1. Before work starts, the issue exists, sits where `## Hierarchy` in `docs/agents/ticket-standard.md` places it, passes the Definition of Ready, and is assigned to you. The claim is the first write of the session.
2. When work starts, set the status to in progress.
3. The merge request carries the closing reference.
4. On merge, the issue closes.
5. A feature parent closes only when every child is completed and its aggregate acceptance criteria pass.
6. Deferred work found along the way goes through the authorization gate. Surface its title and reason, and create it only after approval.
