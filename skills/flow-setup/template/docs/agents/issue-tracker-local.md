# Issue tracker: Local

Issues for this repository live as Markdown files under `.scratch/`. There is no remote tracker. Whether `.scratch/` is committed is this repository's choice.

- One folder per feature or group of work, `.scratch/<group>/`. Standalone work uses the group `standalone`.
- A feature parent is `.scratch/<group>/parent.md`.
- Each work issue is its own file, `.scratch/<group>/issues/<NN>-<slug>.md`, numbered from `01`. Never combine tickets in one file.
- An issue's id is its path under `.scratch/` without the extension, as in `checkout/issues/03-retry-payment`.
- Header lines at the top of each file record its state: `Status: open`, `in-progress`, or `closed`, then `Assignee:`, `Parent:`, `Blocked by:`, and `Labels:`.
- Comments append under a `## Comments` heading at the bottom, oldest first, each with a date and an author.

## Authorization gate

Creating tracker items is deny-by-default. What becomes tracked work is the maintainer's decision, made item by item. Writing a new file under `.scratch/` creates a tracker item.

Never create an issue, a parent, or a label without explicit authorization. Authorization is a message from the user that asks for this item, and the test is that you can quote it. An audit finding, deferred work, a standing doc line, or an existing branch is not authorization. `/flow-to-issues` authorizes local drafting only. It publishes after the user approves the exact issue set and hierarchy.

Findings that surface mid-task go to one of two places, and both leave the tracker untouched. Report them in the conversation, proposing a title and a one-line reason, then wait. Or add them to the ticket already in hand, as a Follow-ups section in a body you were asked to write.

The operations below are mechanics for after authorization.

## Operations

- **Create.** Write a new file in the layout above with the next free number in its group, creating the folders as needed. Start it with `Status: open`.
- **Read.** Read the file.
- **List.** List the files under `.scratch/*/issues/` and read their header lines. `rg -l '^Status: open' .scratch` finds open issues.
- **Comment.** Append under `## Comments`.
- **Label.** Edit the `Labels:` line.
- **Close.** Add a comment with the reason, then set `Status: closed`. The closing reference is `Closes <issue id>` in the pull request body. Nothing closes the file automatically, so set the status after the merge.
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
