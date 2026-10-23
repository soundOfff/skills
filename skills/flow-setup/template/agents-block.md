<!-- flow:begin v={{version}} -->
<!-- Managed by /flow-setup. A re-run rewrites everything between these markers. Keep repository notes outside them. -->

## Settings

| Setting | Value |
| --- | --- |
| Base branch | `{{base}}` |
| Publish mode | `{{publish_mode}}` |
| Merge strategy | `{{merge_strategy}}` |
| Forge | `{{forge}}` |
| Tracker | `{{tracker}}` |
| Pull request template | {{pr_template}} |
| Closing reference | `{{closing_reference}}` |
| Ready label | `{{ready_label}}` |

Flow skills read these values from this table and nowhere else. Files in `docs/agents/` name a row instead of repeating its value. To change a value, re-run `/flow-setup`.

## Commands

| Gate | Command |
| --- | --- |
| install | {{cmd:install}} |
| dev | {{cmd:dev}} |
| format | {{cmd:format}} |
| lint | {{cmd:lint}} |
| typecheck | {{cmd:typecheck}} |
| test | {{cmd:test}} |
| test-file | {{cmd:test-file}} |
| e2e | {{cmd:e2e}} |
| build | {{cmd:build}} |
| design | {{cmd:design}} |
| health | {{cmd:health}} |

The full gate is `lint`, `typecheck`, `test`, and `build`, skipping any that read `n/a`. `test-file` runs one test file, with `<path>` replaced by its path. A gate that reads `n/a` is not configured.

## Sources of truth

| Concern | Path |
| --- | --- |
| Domain language | {{src:Domain language}} |
| Decisions | {{src:Decisions}} |
| Conventions | {{src:Conventions}} |
| Design system | {{src:Design system}} |
| Structure | {{src:Structure}} |

A source that reads `none` does not exist yet. Tracker, ticket, and pull request rules live in `docs/agents/`: `issue-tracker.md`, `ticket-standard.md`, `pr-standard.md`, and `domain.md`.

## Delivery workflow

Tracked work moves through four stages. Each stage is human-invoked, keeps one ledger under the git-ignored `.flow/` folder, and hands control back. No stage starts the next one.

1. `/flow-create`, optional. Turns an idea into a confirmed feature map.
2. `/flow-to-issues`, required for tracked work. Turns settled work into issues that carry the `Ready label`, after the user approves the exact set.
3. `/flow-build <issue>`, optional. Builds one Ready issue up to its review boundary with parallel agents. Direct work on the issue's branch is fine too.
4. `/flow-to-pr <issue>`, required. Rebases, pushes, and opens the pull request in the `Publish mode`.

After publication, `/flow-code-check` reviews code and `/flow-design-check` reviews UI. Their results are advice and never block. Untracked work, such as a quick fix or a spike, runs through `pstack:poteto-mode` directly.

| Skill | Use it to |
| --- | --- |
| `/flow-mode` | Work here with poteto-mode plus this workflow. |
| `/flow-help` | Get a grounded answer, an orientation, or a bug explanation. |
| `/flow-create` | Map a feature and its reuse plan before building it. |
| `/flow-to-issues` | Turn settled work into an approved issue hierarchy. |
| `/flow-build` | Build one Ready issue with focused agents. |
| `/flow-to-pr` | Publish one implemented issue as a pull request. |
| `/flow-code-check` | Review a change for correctness and solution quality. |
| `/flow-design-check` | Review a UI change for design drift. |
| `/flow-adv-review` | Challenge a change with a second model, only when asked. |
| `/flow-setup` | Rewrite this block and refresh `docs/agents/`. |

In Codex, type `$flow-help` instead of `/flow-help`, and the same for every skill above.

## Golden rules

- Never add, upgrade, or remove a dependency unless the user asks for it in that message. Always pin the exact version.
- Work on a feature branch. Never commit or push to the `Base branch`.
- Sync with the `Base branch` on `origin` by rebase. Never merge the base branch into a feature branch.
- Force-push only after a rebase, and only with `--force-with-lease`.
- Never merge a pull request unless the user asks for it in that message.
- Never create an issue, parent, or label without a user message you can quote that asks for it. See `## Authorization gate` in `docs/agents/issue-tracker.md`.
- Never put secrets, credentials, or customer data in code, logs, issues, or pull requests.
- Run the full gate before handing off. When a gate cannot run, report why and never claim it passed.
<!-- flow:end -->
