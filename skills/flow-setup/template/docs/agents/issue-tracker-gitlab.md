# Issue tracker: GitLab

Issues for this repository live in GitLab Issues on the project the `origin` remote points at. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI, which infers the project from the git remote. GitLab calls comments notes and pull requests merge requests.

{{authorization_gate}}

## Operations

- **Create.** `glab issue create --title "<title>" --description "$(cat <file>)"`. Write the description to a file first so multi-line text survives.
- **Read.** `glab issue view <n> --comments`, or `glab issue view <n> -F json` for parsing.
- **List.** `glab issue list -F json`, narrowed with `--label` and `--search`. Add `--all` to include closed issues when checking for duplicates.
- **Comment.** `glab issue note <n> --message "<text>"`.
- **Label.** `glab issue update <n> --label "<label>"`, or `--unlabel "<label>"`. `glab label list` shows the labels that exist. Creating a label is a create and passes the authorization gate first.
- **Close.** `glab issue close` takes no comment, so post the reason with `glab issue note <n> --message "<reason>"` first, then run `glab issue close <n>`. The merge request description carries the `Closing reference` setting from `AGENTS.md` `## Settings`. Merging it into the default branch closes the issue.
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
