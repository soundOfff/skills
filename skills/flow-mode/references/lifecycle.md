# Delivery lifecycle

Tracked work moves through four human-invoked stages. Each stage owns one ledger under [`.flow/`](#where-ledgers-live) and ends by handing control back to the developer. A stage never starts the next one on its own.

```text
idea ──/flow-create (optional)──▶ confirmed feature map
settled work ──/flow-to-issues (required)──▶ Ready issue
Ready issue ──/flow-build (optional) or direct work──▶ committed branch
committed branch ──/flow-to-pr (required)──▶ published pull request
published pull request ──▶ recommended: /flow-code-check (code), /flow-design-check (UI)
```

`/flow-code-check` and `/flow-design-check` are recommended after publication. They are not stages. `/flow-adv-review` runs only when the developer asks for it. No skill or agent invokes it on their behalf. Review results are advice. They never block publication and never start a repair loop by themselves. The developer owns the fix, defer, and merge decisions.

## Stages and their states

| Stage | Ledger | States |
| --- | --- | --- |
| `/flow-create` | `.flow/features/<slug>.md` | `briefing` → `awaiting-confirmation` → `ready-for-issue` |
| `/flow-to-issues` | `.flow/issues/<slug>.md` | `draft` → `awaiting-approval` → `approved` → `publishing` → `published`, or `rejected`, or `partial` |
| `/flow-build` | `.flow/builds/<issue>.md` | `planning` → `building` → `verifying` → `awaiting-to-pr`, or `needs-decision`, or `blocked` |
| `/flow-to-pr` | `.flow/prs/<issue>.md` | `preflight` → `publication-ready` → `published`, or `needs-decision`, or `blocked` |
| `/flow-help` | `.flow/help/<slug>.md`, only when the developer asks to save | `active` until the developer stops it |
| `/flow-adv-review` | `.flow/reviews/` in the current worktree | managed by its runner |

Only the coordinating skill writes its ledger. Dispatched workers return evidence to it.

## Where ledgers live

`.flow/` means one folder that every worktree of the repository shares: the git-ignored `.flow/` folder at the root of the main worktree. Resolve it from any worktree with:

```bash
echo "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")/.flow"
```

Every stage reads and writes its ledgers there, whichever worktree it runs in. `/flow-adv-review` is the exception. It keeps its jobs in the current worktree's `.flow/reviews/`, because a job reviews one working tree.

## Untracked work

Not every change needs an issue. A quick fix, a spike, or a repository without an issue tracker runs through `pstack:poteto-mode` directly. Its Bug fix, Feature, and Refactoring playbooks hold the engineering rigor, and its Opening a PR playbook ships the result. The pipeline adds tracking, approval gates, and a reviewable paper trail on top. It does not replace that rigor.

## Nudges

Suggest these skills at the right moment instead of running them. The stages are human-invoked, and the review checks are recommendations the developer chooses to run:

- An unbriefed feature idea: suggest `/flow-create`.
- A settled plan, a confirmed feature map, or a grilling session that ends in "let's build it": suggest `/flow-to-issues` before any code, so the plan becomes Ready issues instead of a mental note.
- A Ready issue that would benefit from parallel builders: offer `/flow-build <issue>`.
- Implementation of a tracked issue reaches its review boundary: suggest `/flow-to-pr <issue>`.
- A published pull request that changed code or UI: suggest `/flow-code-check`, plus `/flow-design-check` for UI.
- The developer is unsure what to do next: suggest `/whats-next`.
- The repository has no `docs/agents/` folder or no flow block in `AGENTS.md`: suggest `/flow-setup`.
