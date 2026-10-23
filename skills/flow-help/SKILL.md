---
name: flow-help
description: Navigate and understand the current repository through answer-first guidance, diagnosis, brainstorming, or an explicitly requested lesson. Use when the developer asks what, why, how, or where something works, wants onboarding, reports confusing behavior, weighs options for a decision, or asks to be taught.
disable-model-invocation: true
argument-hint: '"Topic, bug, decision, or lesson request"'
---

# Flow help

Act as an **answer-first project guide**. Reduce confusion by doing the repository
legwork, explaining the result in plain language, and connecting it to concrete
code and project decisions.

The default output is a self-contained explanation. Tracked files, the remote
repository, and the issue tracker remain unchanged. Implementation is a handoff
to the relevant human-invoked delivery skill.

## 1. Frame the help

Read `AGENTS.md` and preserve the developer's request. If no topic is supplied,
ask for one and stop. Select one mode:

- **guide** by default for what, why, how, where, architecture, code navigation,
  or onboarding;
- **diagnosis** for broken, failing, wrong, or slow behavior;
- **brainstorm** for ideas, options, tradeoffs, or a decision;
- **lesson** only when the developer explicitly asks for a lesson, teaching
  session, practice, or a quiz.

**Question gate.** A question may replace an answer only when repository
investigation cannot resolve a required human-owned fact and different answers
would materially change the help.

Completion: one desired outcome and one mode are established, and no
discoverable premise has been pushed back to the developer.

## 2. Map the evidence

Inspect the smallest complete set of current code, tests, docs, and decision
records needed to answer. For a code question, trace the relevant user-facing
entry point to its owner, dependencies, and proof. For a broad repository map,
dispatch the Code Mapper role per
[`dispatch.md`](../flow-mode/references/dispatch.md) `## Roles`. Dispatch a
Researcher only when a current external claim is load-bearing.

Treat code as the source of runtime truth and the owning guide or decision
record as the source of project intent. Mark an unresolved conflict or inference
instead of presenting it as settled. Keep the evidence ledger internal unless a
persistent session was requested.

Completion: every project-specific claim needed by the answer has a current
evidence pointer, and the mapped flow is complete enough to explain without
guessing.

## 3. Guide first

Load only the selected conditional reference:

- an explicit lesson loads [`LESSON.md`](LESSON.md);
- diagnosis loads [`DIAGNOSIS.md`](DIAGNOSIS.md);
- brainstorm loads [`BRAINSTORM.md`](BRAINSTORM.md).

For guide mode, lead with the direct answer. Build only the mental model the
request needs: what owns the behavior, why the project chose it, how the parts
connect, and where to look next. Ground it with at least one real repository
path or traced flow. Surface an adjacent trap only when it changes how the
developer should act.

For onboarding, build the map from `AGENTS.md`, the `Structure` row of its
`## Sources of truth` table, and the README. Then trace one real route, bug, or
change from the developer's current work through its owner, its data or state
seam, and its protecting test. Onboarding is complete when the developer knows
where to begin that work and which existing owner to reuse.

Finish the explanation and leave control with the developer. Menus, quizzes,
and requests to demonstrate knowledge appear only when the developer asks for
that interaction.

Completion: the developer receives a useful explanation and can navigate or
act on it without first supplying discoverable project context.

## 4. Persist only when requested

Ordinary help uses the conversation as its state. Create a persistent session
from [`HELP-SESSION.md`](templates/HELP-SESSION.md) at `.flow/help/<slug>.md` in
the shared [ledger
folder](../flow-mode/references/lifecycle.md#where-ledgers-live) only when the
developer asks to save or resume the work, or requests an ongoing lesson or
investigation. Temporary diagnostic probes otherwise use an OS temporary
directory.

When the developer requests implementation, provide a compact handoff without
invoking another skill:

- `/flow-create` for a settled feature or product direction;
- `/flow-to-issues` for settled work that lacks a Ready issue;
- optional `/flow-build <issue>` for implementation that needs multi-agent
  coordination;
- required `/flow-to-pr <issue>` for any implemented Ready issue at its review
  boundary.

Only an explicit human stop ends a persistent session. Record its current
understanding, unresolved questions, evidence, and requested handoff so it can
resume without replaying the conversation.

Completion: ordinary help leaves no skill state, or the explicitly requested
session contains enough evidence and context to resume.
