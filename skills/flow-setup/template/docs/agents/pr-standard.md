# Pull request standard

A pull request is the unit of shipped proof. Reviewers, human or agent, judge it cold, and its merge closes the linked issue. The precision rule from `docs/agents/ticket-standard.md` holds here too. Reviewer defect-finding drops by about half beyond about 400 changed lines (SmartBear, 10 million review sessions). Median time to review roughly doubles with each extra 100 lines (Google's code review guidance). A description that answers what, why, and how up front cuts review time.

## Scope and size

- **One concern per pull request.** It maps to one buildable work issue, or one coherent slice of one. A feature parent is never the work issue. "And" in the title is the same smell as in a ticket title.
- **One worktree per pull request.** When `/flow-build` runs, its builders and `/flow-to-pr` share the pull request's worktree from the first change through publication. Direct work follows the same rule.
- **Soft budget of about 400 changed lines** of hand-written diff. Lockfiles, generated files, and content moved verbatim do not count. Over budget, split along vertical slices or the expand, migrate, and contract sequence. Never split arbitrarily to hit the number.
- **Atomic commits.** Follow the commit style the history already uses. Without one, use Conventional Commits (`feat:`, `fix:`, `docs:`). The pull request title follows the same style.

## Body

Pull request template: {{pr_template}}. These rules apply with or without one.

- **Lead with what and why in one or two sentences.** The reviewer knows the shape of the change before the first file. Then surface the decisions a reviewer would otherwise reverse-engineer from the diff, such as tradeoffs and rejected alternatives.
- **Link the issue.** Tracked work carries its closing reference, `{{closing_reference}}`, as the close operation in `docs/agents/issue-tracker.md` describes. Reference related issues, pull requests, and decision records by id.
- **Report validation honestly.** List each full-gate command from the `## Commands` table in `AGENTS.md` with its actual result. Disclose a flaky failure, a skipped gate, or a hook bypass with its evidence: what failed, why it looks unrelated, and what passed in isolation. Never claim it as a pass and never leave it out.
- **Screenshots for UI changes,** with the same hygiene as tickets. No secrets, customer data, or access-granting links in images or text.
- **Review guidance for multi-file changes.** Name the entry-point file and the reading order when the diff order misleads, as in "start with the schema change; the rest follows from it".
- **Write for people and tools.** Prose for the reviewer, exact issue ids and gate names for automation.

## Lifecycle

| Setting | Value |
| --- | --- |
| Base branch | `{{base}}` |
| Publish mode | `{{publish_mode}}` |
| Merge strategy | `{{merge_strategy}}` |

1. Branch from the latest `origin/{{base}}`. Never commit or push to the base branch.
2. The author runs the full gate before asking for review. In `draft` mode, `/flow-to-pr` opens a draft, and the pull request leaves draft only after the developer has verified the code and the gates. In `ready` mode, it opens the pull request ready for review.
3. Address review feedback with new commits.
4. Sync by rebase only. Run `git fetch origin {{base}}` and `git rebase origin/{{base}}`, then push with `git push --force-with-lease`. Never merge the base branch into the feature branch.
5. The developer merges with the merge strategy above. Agents never merge unless the user asks in that message. On merge, the closing reference closes the linked issue as completed.

## Ready-for-review checklist

A pull request is ready for review only when:

1. The title follows the commit style and names one concern.
2. The body leads with what and why, and surfaces the decisions worth surfacing.
3. Tracked work carries its closing reference, and the issue's acceptance criteria are met. A slice pull request closes its work issue, never an incomplete feature parent.
4. Every full-gate command ran, and its result is reported honestly.
5. The diff is within budget, or the body justifies the exception.
6. UI changes carry clean screenshots. No secret or customer data appears anywhere in the pull request.
7. Docs and decision records changed in the same pull request when a decision, dependency, or command changed.
8. Every hunk traces to the one concern. There are no unexplained drive-by changes.
9. Any optional review or validation that did not run is disclosed as not run, never shown as passing.
