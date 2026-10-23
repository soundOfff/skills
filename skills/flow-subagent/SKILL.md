---
name: flow-subagent
description: Spawn one flow role subagent and supervise it to completion. Use when the developer asks for a subagent by role, optionally naming a CLI ("researcher subagent with codex").
---

# Spawn a flow role subagent

Roles are `flow-code-mapper`, `flow-reuse-auditor`, `flow-design-mapper`,
`flow-researcher`, and `flow-fact-lookup`. The role table, the dispatch
contract, and the missing-agent rule live in
[dispatch.md](../flow-mode/references/dispatch.md). Each agent definition pins
its model and effort, and the pin applies whenever you pass no model. An
override replaces it. **Never pass a model or reasoning override.** Read-only is
by instruction, as dispatch.md explains, because most Claude definitions keep
Bash. The task forbids edits, and you check `git status` afterward. The Codex
definitions also run in a read-only sandbox. Give the subagent one bounded task.
Role behavior comes from its agent definition, not your prompt.

## Same harness is the default

- **You are Claude.** Dispatch the Agent tool with the `flow-*` agent type.
- **You are Codex.** Spawn the named agent.

If the agent type is missing, follow the missing-agent rule in dispatch.md. An
agent installed now loads only in the next session, so this session spawns the
read-only fallback it names and tells the developer to install and restart.

## The developer names the other CLI

"Use researcher subagent with codex" is the trigger. Cross-CLI dispatch happens
**only on that explicit request**. Run the named CLI as a background process and
capture its output to a file.

**Codex CLI.** Take the model and effort from the role's file in the kit's
`agents/codex/` folder. This skill's directory is a link into the kit, so
resolve its real path first. The kit root is two levels above it.

```bash
kit="$(cd "$(realpath <skill-directory>)/../.." && pwd)"
grep -E '^(model|model_reasoning_effort) =' "$kit/agents/codex/<role>.toml"
codex exec --ephemeral --sandbox read-only --cd <repo> \
  -m <model> -c model_reasoning_effort=<effort> \
  -o /tmp/<role>-report.md \
  "You are <role>. Read $kit/agents/roles/<role>.md first. Task: <task>"
```

**Claude CLI.** The installed agent already carries model and instructions.

```bash
claude -p --agent <role> "<task>" > /tmp/<role>-report.md 2>&1
```

## Supervise to completion

Never fire and forget. Start the subagent, keep working, and wait for its
completion callback (Claude task notification, Codex agent completion, or
process exit for a background CLI). No callback? Poll the output file. Then read
the full result and relay the findings to the developer. A spawned subagent with
an unread report is an unfinished task. If it fails, times out, or returns
empty, report exactly that. Never fabricate its result. The subagent is a
read-only leaf. Any file writes from its findings are yours.
