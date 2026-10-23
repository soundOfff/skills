# Issue tracker: Local

Issues for this repository live as Markdown files under `.scratch/`. There is no remote tracker. Whether `.scratch/` is committed is this repository's choice.

- One folder per feature or group of work, `.scratch/<group>/`. Standalone work uses the group `standalone`.
- A feature parent is `.scratch/<group>/parent.md`.
- Each work issue is its own file, `.scratch/<group>/issues/<NN>-<slug>.md`, numbered from `01`. Never combine tickets in one file.
- An issue's id is its path under `.scratch/` without the extension, as in `checkout/issues/03-retry-payment`.
- Header lines at the top of each file record its state: `Status: open`, `in-progress`, or `closed`, then `Assignee:`, `Parent:`, `Blocked by:`, and `Labels:`.
- Comments append under a `## Comments` heading at the bottom, oldest first, each with a date and an author.
- Writing a new file under `.scratch/` creates a tracker item, so it passes the authorization gate first.

{{authorization_gate}}

## Operations

- **Create.** Write a new file in the layout above with the next free number in its group, creating the folders as needed. Start it with `Status: open`.
- **Read.** Read the file.
- **List.** List the files under `.scratch/*/issues/` and read their header lines. `rg -l '^Status: open' .scratch` finds open issues.
- **Comment.** Append under `## Comments`.
- **Label.** Edit the `Labels:` line.
- **Close.** Add a comment with the reason, then set `Status: closed`. The pull request body carries the `Closing reference` setting from `AGENTS.md` `## Settings`. Nothing closes the file automatically, so set the status after the merge.
- **Set parent.** Set the child's `Parent:` line to the parent's id, and list the child under a `## Children` heading in the parent.
- **Add dependency.** Add the blocker's id to the child's `Blocked by:` line. An issue is unblocked when every listed issue is closed.
- **Assign.** Set the `Assignee:` line. Never replace another assignee.
- **Set status.** Set the `Status:` line.

## Claiming work

1. Before work starts, the issue exists, sits where `## Hierarchy` in `docs/agents/ticket-standard.md` places it, passes the Definition of Ready, and is assigned to you. The claim is the first write of the session.
2. When work starts, set `Status: in-progress`.
3. The pull request carries the closing reference.
4. After the merge, set `Status: closed`.
5. A feature parent closes only when every child is closed and its aggregate acceptance criteria pass.
6. Deferred work found along the way goes through the authorization gate. Surface its title and reason, and create it only after approval.
