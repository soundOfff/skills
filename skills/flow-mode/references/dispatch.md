# Dispatch

How the flow skills hand work to other agents. Skills own orchestration and gates. Agent definitions and role references own role behavior. Capability skills supply the know-how a role needs.

## Dispatch contract

Every dispatch carries exactly this, and nothing the role does not need:

```text
Role: <role name from the table below>
Agent: <agent type for the current harness, from the table below>
Engine: <absolute path of poteto-mode's SKILL.md, or none when pstack is absent>
Context: <one feature map, issue, or ledger path>
Task: <one bounded question or assignment>
Scope: <paths or concern>
References: <only the capability skills and role references this worker needs>
```

Only a Builder dispatch carries `Engine`. The dispatching agent keeps the coordination state. Read-only workers return reports. They never edit the shared feature map, ledger, or issue. Name a capability reference only for the worker that needs it.

## Roles

| Role | Claude Code agent | Codex agent | Behavior owner |
| --- | --- | --- | --- |
| Code Mapper | `flow-code-mapper` | `flow-code-mapper` | the agent definition |
| Reuse Auditor | `flow-reuse-auditor` | `flow-reuse-auditor` | the agent definition |
| Design Mapper | `flow-design-mapper` | `flow-design-mapper` | the agent definition |
| Researcher | `flow-researcher` | `flow-researcher` | the agent definition |
| Fact lookup | `flow-fact-lookup` | `flow-fact-lookup` | the agent definition |
| Builder | `pstack:poteto-agent`, or `general-purpose` when pstack is absent | a plain spawned worker with workspace write | [builder.md](../../flow-build/references/builder.md) |
| Browser QA | `general-purpose` with browser tools | a spawned worker with browser tools | [browser-qa.md](../../flow-build/references/browser-qa.md) |
| Prototype | `general-purpose` with `isolation: "worktree"` | `codex exec --sandbox workspace-write --cd <worktree>` | the `prototype` skill |

The `flow-*` agent definitions pin their own model and reasoning effort. The pin applies whenever a dispatch names no model. A model or effort override replaces it, so pass none. Builders and prototypes run on the caller's model, or on the pstack role model when one is configured (`feature, refactoring` and `bug-fix` lines in the pstack model rule).

Builders run as `pstack:poteto-agent` under Claude Code so every implementation step reads poteto-mode and applies its principles. That agent finds poteto-mode only through the `Engine` path. Without it, the agent searches Cursor's plugin folders and stops. Resolve the path as [flow-mode](../SKILL.md#start) step 1 does. The Codex pstack port has no `poteto-agent` type, so a Codex Builder is a plain worker whose brief carries the `Engine` path and [builder.md](../../flow-build/references/builder.md).

Read-only is by instruction. The Claude role definitions drop the edit tools, but most keep Bash for inspection, so each brief forbids edits and the coordinator checks `git status` after the worker returns. The Codex role definitions also set `sandbox_mode = "read-only"`, so there the sandbox enforces it.

When a `flow-*` agent type is missing, the kit is not installed for this harness. Agents installed now load only in the next session. Fall back at once to a read-only search agent (`Explore` in Claude Code, `codex exec --ephemeral --sandbox read-only --cd <repo>` in Codex) whose brief includes the role's definition from the kit's `agents/roles/` folder. Say so in the report, and tell the user to run `/flow-setup machine` or the kit's `install.sh` and then restart the session.

## Execution rules

These hold in every harness:

- Read-only investigators run in a fresh, read-only context. Never fork the coordinator. A fork inherits the coordinator's model and its conclusions, which destroys the independence the Reuse Auditor exists for.
- Roles that need the web or a writable worktree run as general-purpose agents. A writable worktree stays isolated from the developer's checkout.
- Investigation runs at the cheapest tier that can still verify an interface. The coordinator's tier is for synthesis and gates.
- The coordinator keeps synthesis, gate enforcement, and every write to the shared artifact. Workers return evidence only.
- Dispatches with scopes that do not overlap go out in one batch.

A harness that offers no fresh, isolated, read-only context still owes these rules. Say so in the report instead of running every role in the coordinating context.

## TDD routing

- Every assignment that adds or corrects executable behavior receives [the `flow-tdd` skill](../../flow-tdd/SKILL.md), one public test seam, and its first red command.
- The complete exception set is documentation or static artifacts, generated refreshes, and behavior-preserving refactors that a named existing test already covers.
- The coordinator records an exception and its before-and-after proof before dispatch. A builder cannot exempt itself after implementation starts.
- The coordinator runs the full gate once at the build boundary. The red-green cycle itself belongs to the `flow-tdd` skill and the builder reference.

## Bug-diagnosis routing

- Every assignment that corrects broken behavior or a performance regression also receives [the `diagnose` skill](../../diagnose/SKILL.md).
- The assignment records the exact symptom and a red-capable loop command. When no loop exists, a read-only diagnosis assignment must produce one before any implementation assignment unblocks.
- Implementation starts only after the loop reproduces the reported symptom, the reproduction is minimized, and probe evidence confirms the cause.

## Capability routing

The coordinator picks capability skills from what the repository uses and the kit has installed. Repository rules and decision records win when a capability skill conflicts with them.

- Work that writes or refactors React components, hooks, client data fetching, or frontend tests receives [`react-best-practices`](../../react-best-practices/SKILL.md).
- Work that designs or changes component APIs, variants, compound components, context providers, or shared state interfaces also receives [`react-composition-patterns`](../../react-composition-patterns/SKILL.md).
- TypeScript work may receive `pstack:typescript-best-practices`.
- A worker reads the skill's entry point and only the rule files that apply to its change.

For other stacks, name the repository's own conventions doc from the `## Sources of truth` table in `AGENTS.md`.
