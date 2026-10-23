# skills

My agent workflow, packaged once for Claude Code and Codex. It has three layers:

1. **pstack is the engine.** `poteto-mode`, its principles, playbooks, and review panels stay an installed plugin, so they keep updating upstream.
2. **The flow kit is the delivery workflow.** Brief a feature, turn it into Ready issues, build it with role agents, publish the pull request, and review it. Every step reads the repository's own commands and standards, so the same process runs in any language or framework.
3. **Everyday skills** are the capability, UI, and stack skills I actually use, kept by measured use.

## Install on a machine

```bash
git clone git@github.com:soundOfff/skills.git ~/Tomi/personal-skills
cd ~/Tomi/personal-skills
./install.sh --dry-run
./install.sh
```

`install.sh` fetches the third-party skills pinned in [agents.toml](agents.toml) into `.agents/skills`, then symlinks every skill into `~/.claude/skills` and `~/.codex/skills`, and the role agents into `~/.claude/agents` and `~/.codex/agents`. It moves anything real it would replace into `.install-backup/`, removes links to skills that no longer exist, and changes nothing on a second run. Fetching needs Node 20 or later, and `--no-fetch` links only what is already fetched.

Then install pstack in each tool:

| Tool | Steps |
| --- | --- |
| Claude Code | `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`, then `/pstack:setup-pstack` |
| Codex | `codex plugin marketplace add michael-denyer/pstack-claude`, then `codex plugin add pstack@pstack-claude`, then `$setup-pstack` |

`/flow-setup machine` runs the installer and checks every item above.

## Set up a repository

Run `/flow-setup` inside the repository. It detects the stack, the issue tracker, the domain docs, and the design authority, asks only what it cannot detect, and writes:

- a managed block in `AGENTS.md` with the repository's settings, gates, and sources of truth;
- `docs/agents/` standards for tickets, pull requests, the issue tracker, and domain docs;
- `.flow/` in `.gitignore`, where the workflow keeps its ledgers;
- a pull request template on GitHub and GitLab;
- optionally a first `DESIGN.md` for a repository with a user interface, built from the code or seeded from five questions with the `impeccable` skill, or pasted, for example from Google Stitch.

A doctor script then checks the result. Running `/flow-setup` again rewrites the managed block and asks before it replaces any changed `docs/agents/` file.

## The workflow

```text
idea ──/flow-create──▶ confirmed feature map
settled work ──/flow-to-issues──▶ Ready issues
Ready issue ──/flow-build or direct work──▶ committed branch
committed branch ──/flow-to-pr──▶ pull request
pull request ──▶ /flow-code-check, /flow-design-check, /flow-adv-review
```

You start each stage yourself, as `/flow-create` in Claude Code or `$flow-create` in Codex. A stage keeps its state in a ledger under `.flow/` and stops at its handoff. Work that needs no issue skips the pipeline and runs through `poteto-mode` directly. `/flow-mode` is the single entry point. It loads `poteto-mode`, routes the request to a stage or a playbook, and applies the repository's standards. [lifecycle.md](skills/flow-mode/references/lifecycle.md) has the full state machine.

Read-only role agents do the investigation, each on a model pinned in its definition:

| Agent | Job |
| --- | --- |
| `flow-code-mapper` | Traces how a change meets the code |
| `flow-reuse-auditor` | Finds existing owners before anyone writes new code |
| `flow-design-mapper` | Maps design-system rules and comparable screens |
| `flow-researcher` | Answers external questions from primary sources |
| `flow-fact-lookup` | Answers one narrow fact about the repository |

## Skills

<!-- catalog:begin -->

### Delivery workflow

| Skill | What it does | Invoked by |
| --- | --- | --- |
| `flow-setup` | Install the flow kit on this machine, or profile a repository so the flow skills run there. | you type it |
| `flow-mode` | Run pstack's poteto-mode with this kit's delivery workflow on top: feature briefs, tracked issues, multi-agent builds, pull requests, and review gates, all driven by the repository's own commands and standards. | you type it |
| `flow-help` | Navigate and understand the current repository through answer-first guidance, diagnosis, brainstorming, or an explicitly requested lesson. | you type it |
| `flow-create` | Build an evidence-backed feature map and reuse plan from a feature description. | you type it |
| `flow-to-issues` | Convert settled work into an approved issue hierarchy on the repository's issue tracker. | you type it |
| `flow-build` | Build one Ready issue through its review boundary. | you type it |
| `flow-to-pr` | Publish one implemented, tracked issue as a correctly formatted pull request. | you type it |
| `flow-code-check` | Produce an optional consolidated correctness and solution-quality review for a pinned change. | you or the agent |
| `flow-code-review` | Correctness-review a pinned change (behavior, spec, regressions, security) as flow-code-check's correctness worker. | you or the agent |
| `flow-code-quality-review` | Quality-review a pinned change (reuse, decomposition, maintainability) as flow-code-check's quality worker. | you or the agent |
| `flow-design-check` | Produce an optional design-drift review for a pinned UI change. | you or the agent |
| `flow-adv-review` | Adversarially challenge a working-tree or branch diff in a fresh reviewer process when a developer explicitly requests it. | you type it |
| `flow-subagent` | Spawn one flow role subagent and supervise it to completion. | you or the agent |
| `flow-tdd` | Test-drive executable behavior through public seams with a red, green, refactor loop. | you or the agent |

### Everyday skills

| Skill | What it does | Invoked by |
| --- | --- | --- |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. | you or the agent |
| `domain-modeling` | Build and sharpen a project's domain model. | you or the agent |
| `grilling` | Interview the user relentlessly about a plan, decision, or idea, asking every question that can be settled now in one numbered round at a time. | you or the agent |
| `prototype` | Build a throwaway prototype to answer a design question. | you or the agent |
| `react-best-practices` | React and Next.js performance and code-quality rules, built on Vercel Engineering's performance set and extended with component structure, testing, and type-safety rules. | you or the agent |
| `react-composition-patterns` | Design React 19 component APIs with composition, explicit variants, and compound components. | you or the agent |
| `research` | Investigate a question against high-trust primary sources and write the cited findings to a Markdown note in the repository. | you or the agent |
| `test-audit` | Invoke whenever writing, changing, reviewing, or sweeping tests. | you or the agent |
| `whats-next` | Suggests the 3 most impactful next actions from the developer's full context: git, open pull requests and review requests, the issue tracker, flow ledgers waiting on their next stage, and the current conversation. | you type it |

### Third-party

Pinned in [agents.toml](agents.toml) and fetched by `install.sh`.

| Skill | Upstream | Pinned commit |
| --- | --- | --- |
| [`better-accessibility`](https://github.com/jakubkrehel/skills/tree/4650b9c0300852b59be163649926424fe990df9a/skills/better-accessibility) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `4650b9c03008` |
| [`better-colors`](https://github.com/jakubkrehel/skills/tree/9b03828ccb64a1093334c0e4a5c1aa1c86d7241f/skills/better-colors) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `9b03828ccb64` |
| [`better-interface`](https://github.com/jakubkrehel/skills/tree/267330e1adfc66a718fb65fa6918c1f06d0a689e/skills/better-interface) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `267330e1adfc` |
| [`better-layout`](https://github.com/jakubkrehel/skills/tree/da5f6d59741e93cf9d36a67179f42d33f2cbb452/skills/better-layout) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `da5f6d59741e` |
| [`better-typography`](https://github.com/jakubkrehel/skills/tree/4650b9c0300852b59be163649926424fe990df9a/skills/better-typography) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `4650b9c03008` |
| [`better-ui`](https://github.com/jakubkrehel/skills/tree/267330e1adfc66a718fb65fa6918c1f06d0a689e/skills/better-ui) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `267330e1adfc` |
| [`better-writing`](https://github.com/jakubkrehel/skills/tree/da5f6d59741e93cf9d36a67179f42d33f2cbb452/skills/better-writing) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | `da5f6d59741e` |
| [`frontend-design`](https://github.com/anthropics/claude-plugins-official/tree/44490cccaf6d9f82fdeec9416fbf7c9bd72575dc/plugins/frontend-design/skills/frontend-design) | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | `44490cccaf6d` |
| [`grill-me`](https://github.com/mattpocock/skills/tree/697d4ce9742da558fd1ba6697c8e9775e2e302dd/skills/productivity/grill-me) | [mattpocock/skills](https://github.com/mattpocock/skills) | `697d4ce9742d` |
| [`grill-with-docs`](https://github.com/mattpocock/skills/tree/697d4ce9742da558fd1ba6697c8e9775e2e302dd/skills/engineering/grill-with-docs) | [mattpocock/skills](https://github.com/mattpocock/skills) | `697d4ce9742d` |
| [`handoff`](https://github.com/mattpocock/skills/tree/697d4ce9742da558fd1ba6697c8e9775e2e302dd/skills/productivity/handoff) | [mattpocock/skills](https://github.com/mattpocock/skills) | `697d4ce9742d` |
| [`impeccable`](https://github.com/pbakaus/impeccable/tree/0760cdf3e907e7c96bb6524ac58933f5ffca4782/.agents/skills/impeccable) | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | `0760cdf3e907` |
| [`make-interfaces-feel-better`](https://github.com/jakubkrehel/make-interfaces-feel-better/tree/384562064fcdd99778fcbafd8729626fe6aab02f/skills/make-interfaces-feel-better) | [jakubkrehel/make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better) | `384562064fcd` |
| [`resolving-merge-conflicts`](https://github.com/mattpocock/skills/tree/697d4ce9742da558fd1ba6697c8e9775e2e302dd/skills/engineering/resolving-merge-conflicts) | [mattpocock/skills](https://github.com/mattpocock/skills) | `697d4ce9742d` |
| [`test-master`](https://github.com/Jeffallan/claude-skills/tree/3ba746ec95b30aba3c43ff4180f5146405ba253c/skills/test-master) | [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | `3ba746ec95b3` |

<!-- catalog:end -->

## Guides

- [Build a pull request review bot](docs/pr-review-bot.md) runs the kit's adversarial review on any pull request you comment on, with one GitHub Actions workflow or a small cloud setup.

## Maintain the kit

- `python3 tools/validate.py` checks every skill and agent. Run it before each commit.
- `python3 tools/skill_usage.py` counts how often each skill ran in Claude Code, Codex, and Cursor. Run it before you add or remove a skill.
- `python3 tools/build_agents.py` renders `agents/roles/` into the Claude Code and Codex agent formats.
- `python3 tools/readme_catalog.py` rebuilds the skill tables above.

[AGENTS.md](AGENTS.md) has the rules for editing the kit. [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) lists the projects the kit's own skills adapt, and their licenses. Skills removed in the October 2026 cleanup are still in git history, for example `git show 4da67ef:vendor/skills/<name>/SKILL.md`.

### Third-party skills

[agents.toml](agents.toml) is the kit's `package.json` for skills. Each entry pins one upstream skill to a commit:

```toml
[[skills]]
name = "impeccable"
source = "pbakaus/impeccable"
ref = "0760cdf3e907e7c96bb6524ac58933f5ffca4782"
path = ".agents/skills/impeccable"
```

`./install.sh` fetches every entry with [dotagents](https://github.com/getsentry/dotagents) and links it next to the kit's own skills. The fetched folders and dotagents' `agents.lock` stay out of git, so `agents.toml` is the only record. `python3 tools/validate.py` rejects a `ref` that is not a full commit SHA, because dotagents fetches a branch or tag fresh on every install.

- **Add a skill.** Append an entry with the skill's folder as `path` and a full commit SHA as `ref`, then run `./install.sh`.
- **Update a skill.** Set `ref` to a newer commit and run `./install.sh`. `gh api 'repos/<source>/commits?path=<path>&per_page=1' --jq '.[0].sha'` prints the newest commit that changed the skill.
- **Remove a skill.** Delete its entry and run `./install.sh`, which removes its links.
- **Change a skill.** Copy it into `skills/` under the same name and delete its entry. The kit owns the copy from then on.
