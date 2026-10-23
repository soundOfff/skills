# Ticket standard

Every issue in this repository is written to be picked up cold, by an agent or a person who was not in the conversation that produced it. Questions mid-build are possible but expensive. A self-contained ticket keeps delegated work moving.

The evidence is direct. A study of 3,180 agent-authored pull requests (arXiv:2512.21426) found that well-scoped issues raised the merge rate by 16.4% and self-contained issues by 16.7%. Named files added 6.4% and step-wise guidance 7.6%. Longer bodies lowered the merge rate by about 9% per length step. Precision wins and volume loses.

Tracker mechanics live in `docs/agents/issue-tracker.md`. This file covers buildable work issues. Feature parents are outcome containers and follow `## Feature parent`.

## Template

Section order is fixed. A section with nothing to say states its zero result in one line, such as "No-gos: none surfaced". An absent section reads as an oversight. An explicit "none" reads as a decision.

- **Title.** Names the action or outcome. An optional routing prefix is fine when it helps scanning, as in `ci: run the e2e gate on pull requests`. Phase numbers and repeated hierarchy are noise. Rewrite a title that does not reveal the work.
- **Problem.** Why the work exists. State the problem, not a restated solution. Quote the user verbatim where their wording sets scope, such as a constraint or a rejected alternative. Rewrite a Problem that only makes sense once you know the fix.
- **Acceptance criteria.** One to three checkboxes, each independently testable and observable. Use Given/When/Then only when behavior branches on state. Include the negative path when one exists, because happy-path-only criteria are the top measured cause of rework. The verbs `improve`, `better`, `faster`, and `cleaner` are banned, as is any verb whose completion nobody can observe.
- **Pointers.** Repository-relative `path:line` pointers to the code the work touches, plus the closest existing pattern to follow. The builder reads. It does not search.
- **Verification.** Exactly one machine-checkable signal, a command and its expected result. Use the `test-file` gate or another gate from the `## Commands` table in `AGENTS.md`. "Manually confirm it looks right" is not verification. When no machine signal can exist, as with visual work, name the human observation that replaces it and why. Browser QA findings count.
- **No-gos.** Three lists. Functionality that is out of scope. Paths and behavior the builder must not modify. Known traps, each with the agreed way around it. Scope boundaries keep a delegated build from wandering.
- **Blocked by.** Native dependencies, added with the add dependency operation in `docs/agents/issue-tracker.md` and mirrored as a `Blocked by` line. With no blockers, write "None. Can start immediately."
- **Review boundary.** The evidenced reason this issue stops here instead of absorbing the next work. Name the shared seam, risk boundary, independently reviewable behavior, or dependency that makes another review cycle cheaper than continuing.
- **New dependencies.** Only when the work is expected to add a direct package. Research the current best choice from an official source and stamp one line per package, ``Predicted direct package: `<name>`; version note: `<researched version>`; source: <url>``. The user approves against this stamp. The dependency rule in `AGENTS.md` `## Golden rules` still applies at install time, and the pinned version comes from the user's request, not from the note.

Copy this skeleton:

```markdown
# <work title>

## Problem
<why this work exists; quote the user verbatim where wording decides scope>

## Acceptance criteria
- [ ] <observable, testable statement>
- [ ] <the negative path, when one exists>

## Pointers
- `<path>:<line>`. <what is there and what changes>
- Follow the pattern in `<path>:<line>`.

## Verification
`<command>` exits 0. <or the expected output>

## No-gos
- Out of scope: <items, or "none">
- Do not touch: <paths or behavior, or "none">
- Traps: <trap and the agreed way around it, or "none">

## Blocked by
<issue references, or "None. Can start immediately.">

## Review boundary
<why work pauses here, with the source or repository evidence>
```

## Hierarchy

Pick exactly one shape for each piece of settled work.

- **Atomic.** One work issue with no parent. Use it when the work fits one review horizon.
- **Feature parent with children.** A feature that needs more than one work issue gets one new feature parent. Every work issue of the feature becomes a native child of that parent through the set parent operation.
- **Existing parent.** Work that extends an open parent attaches to it as a child instead of creating a new parent.

A parent is required only for the children of a feature parent or an existing parent. Atomic work stands alone. Edit this paragraph when the repository keeps every issue under a container parent.

## Sizing

- **Meaningful work only.** Product behavior, backend, frontend, integration, testing, documentation, refactoring, infrastructure, and CI work each earn an issue when they are real units of delivery. Do not create bookkeeping tickets.
- **Review horizon.** End a work item where continuing without independent review would make drift or repair materially more expensive. Shared interfaces, data or permission seams, cross-layer behavior, reviewable UI journeys, and dependencies that unblock later work are natural boundaries. Do not split by phase number, layer, file count, or diff size alone.
- **Independently verifiable.** Prefer a complete vertical behavior. A technical or layer-specific issue is valid when it has a coherent outcome, a verification signal, and a justified review boundary.
- **No embedded setup.** Environment or dependency groundwork inside a feature ticket measurably lowers agent success, by 7 to 9%. Hoist it into a prerequisite ticket and link it as a blocker.
- **400-word budget.** When detail competes with the budget, keep the scope boundaries and the verification, and cut narrative.
- **Wide refactors.** These are the exception to vertical slicing. Sequence them as expand, migrate in batches, and contract, with each batch its own linked ticket.

## Feature parent

A feature parent carries the feature's aggregate Problem, Acceptance criteria, Verification, No-gos, and labels. Nobody claims or builds it directly.

Its children cover every meaningful product and engineering contribution. Do not add a mandatory integration or acceptance child. Either one exists only when it names real work. The parent stays open until every child is closed as completed and the aggregate acceptance criteria pass on the integrated base branch. A slice pull request never closes the parent.

```markdown
# <feature title>

## Problem
<feature-level problem>

## Acceptance criteria
- [ ] <aggregate observable outcome>

## Verification
<feature-level machine signal, or the justified human proof>

## No-gos
- <feature boundary, or "none">

## Completion
- [ ] Every child issue is closed as completed.
- [ ] The aggregate acceptance criteria pass on the integrated base branch.
```

## Hygiene

Write every ticket as if everyone who can read the tracker will read it.

- No secrets, tokens, credentials, customer data, or links that grant access. A pasted transcript or a share link in an issue body is a leak.
- Security terms such as authorization, trust boundary, or injection appear only in a ticket whose scope is security work. Every other ticket describes the same behavior in product words, such as "only the owner sees this page", so the tracker does not advertise a weakness.

## Definition of Ready

Check a ticket before claiming or dispatching it. It is Ready only when:

1. The title names the work, and any prefix helps scanning.
2. The Problem states a problem and quotes the user where their wording decides scope.
3. It has one to three acceptance criteria, each testable, with no banned verbs, and the negative path where one exists.
4. Verification names one machine-checkable signal, or the justified human observation.
5. Pointers name at least one repository path, or say why the work creates a new area.
6. No-gos are present. An explicit "none" is valid. Absence is not.
7. Dependency edges point at real issues and form no cycle. No setup hides inside a feature ticket.
8. The body fits the 400-word budget.
9. Placement follows `## Hierarchy`.
10. The review boundary names the evidence for pausing at this issue.
11. Code-bearing work lands through a branch and a pull request, never as a direct change to the base branch.

A failed check sends the ticket back to its author. Never fix it silently during dispatch.
