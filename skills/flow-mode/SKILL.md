---
name: flow-mode
description: "Run pstack's poteto-mode with this kit's delivery workflow on top: feature briefs, tracked issues, multi-agent builds, pull requests, and review gates, all driven by the repository's own commands and standards. Use for /flow-mode or a request to work in flow mode."
disable-model-invocation: true
---

# Flow mode

`pstack:poteto-mode` is the engine. It owns the playbooks, the principles, autonomy, subagent rules, and the reply style. Flow mode adds the delivery workflow and the repository's standards, and wins only where this file says so.

## Start

1. Load poteto-mode and follow it in full. Keep the absolute path of its `SKILL.md`, because every Builder dispatch carries it.
   - Claude Code: the pstack folder is the `installPath` recorded for `pstack@cursor-plugins` in `installed_plugins.json`. The session offers the `pstack:poteto-agent` agent type when it is enabled. Prefer the install for this repository over the user install:

     ```bash
     common="$(git rev-parse --path-format=absolute --git-common-dir)"
     if [ "$(basename "$common")" = .git ]; then root="$(dirname "$common")"; else root="$(git rev-parse --show-toplevel)"; fi
     jq -r --arg repo "$root" '.plugins["pstack@cursor-plugins"] // [] | if type == "array" then . else [.] end
       | (map(select(.projectPath == $repo)) + map(select(.scope == "user")))[0].installPath // empty' \
       ~/.claude/plugins/installed_plugins.json
     ```

     Read `skills/poteto-mode/SKILL.md` and the adapter at `docs/harness/claude-code.md` in that folder. The Skill tool refuses poteto-mode, so read the file.
   - Codex: the pstack folder is the highest version under the `pstack-claude` plugin cache. A plain sort would put `0.15.9` after `0.15.28`, so sort by version:

     ```bash
     ls -d ~/.codex/plugins/cache/pstack-claude/pstack/* | sort -V | tail -n 1
     ```

     Run `$poteto-mode`, or read `skills/poteto-mode/SKILL.md` in that folder, and read its `references/codex-tools.md`.
   - When neither resolves, pstack is not installed. Stop and suggest `/flow-setup machine`.
2. Read the repository's `AGENTS.md`. Its flow block opens with `<!-- flow:begin v=<version> -->`, or with a bare `<!-- flow:begin -->` in older profiles. Without the block, the repository is not set up. Work through poteto-mode alone and suggest `/flow-setup` once in the reply.
3. Read [lifecycle.md](references/lifecycle.md). List the shared [`.flow/` folder](references/lifecycle.md#where-ledgers-live) and read any ledger still waiting on its next stage, so in-flight work resumes instead of restarting.

## Route

Match the request here before poteto-mode picks a playbook. Tracked work goes through the pipeline. Everything else goes to the poteto-mode playbook named in the right column.

| Request | Route |
| --- | --- |
| How or why something in this repository works, onboarding | `/flow-help`; `pstack:how`, `pstack:why`, or `pstack:teach` for a deep walkthrough |
| An unsettled feature idea | `/flow-create` |
| Stress-test a plan or a decision | `grilling` |
| A settled plan or a confirmed feature map | `/flow-to-issues` |
| Implement a Ready issue | `/flow-build <issue>`, or the poteto-mode Feature, Bug fix, or Refactoring playbook on the issue's branch, ending at the issue's review boundary |
| Build something that has no issue | the poteto-mode playbook; before publishing, suggest `/flow-to-issues` when the repository tracks work |
| A defect | the poteto-mode Bug fix playbook with `diagnose`; a tracked defect ends at the issue's review boundary |
| Publish a tracked branch | `/flow-to-pr <issue>` |
| Publish untracked work | the poteto-mode Opening a PR playbook |
| Review a branch or a pull request | `/flow-code-check`, plus `/flow-design-check` for UI; `pstack:interrogate` for a contested design |
| A second opinion from another model | `/flow-adv-review`, only when the user asks for it by name |
| Babysit, land, or ship | the poteto-mode Babysit or Shipping playbook |
| What to do next | `/whats-next` |
| Set up a repository or a machine | `/flow-setup` |

The pipeline skills are human-invoked. A request that names a stage counts as the user invoking that stage, so read its `SKILL.md` from this skill's sibling folder (for example `../flow-create/SKILL.md`) and follow it. Never chain into the next stage. End each stage at its handoff and give the nudge from lifecycle.md.

## Overrides

- **Settings.** Read the base branch, publish mode, merge strategy, forge, tracker, pull request template, closing reference, and Ready label from the `## Settings` table of `AGENTS.md`. They replace poteto-mode's defaults.
- **Commands.** Use the gates in the `## Commands` table of `AGENTS.md`. Done means the full gate passed, or each gate that could not pass is reported with its output.
- **Standards.** Tickets follow `docs/agents/ticket-standard.md`. Pull requests follow `docs/agents/pr-standard.md`, and the `Publish mode` setting replaces poteto-mode's rule to open every pull request ready. Tracker writes follow `docs/agents/issue-tracker.md`, where creating anything is denied until the user approves it.
- **Publishing tracked work.** Tracked work implements an issue on the repository's tracker. Many poteto-mode playbooks, such as Feature, Bug fix, Refactoring, Perf issue, and Multi-phase plan, end by running Opening a PR. For tracked work, replace that step in every playbook with "Stop at the issue's review boundary and suggest `/flow-to-pr <issue>`." Opening a PR stays only for untracked work.
- **Delegation.** Dispatch roles per [dispatch.md](references/dispatch.md). Code-writing delegates stay `pstack:poteto-agent`.
- **Domain.** Name things with the vocabulary in `docs/agents/domain.md`. Settle new terms and decisions with `domain-modeling`.
- **Writing.** Every issue body, pull request, report, and reply goes through `pstack:technical-writing` and `pstack:unslop`.

## Always pause

In addition to poteto-mode's list:

- Creating issues, parents, labels, or milestones before the approval that `/flow-to-issues` defines.
- Opening a pull request for a tracked issue outside `/flow-to-pr`.
- Marking a draft pull request ready, merging, or adding an auto-merge label, unless the user asked in that message.
- Adding, upgrading, or removing a dependency, unless the user asked in that message.
