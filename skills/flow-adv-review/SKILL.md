---
name: flow-adv-review
description: Adversarially challenge a working-tree or branch diff in a fresh reviewer process when a developer explicitly requests it.
disable-model-invocation: true
---

# Flow adversarial review

Run `/flow-adv-review [harness] [--scope auto|working-tree|branch]
[--base <ref>] [focus...]` as a read-only challenge review.
This skill is human-invokable only. No skill, coordinator, reviewer, or inferred
risk may invoke it on the developer's behalf.
The first argument selects `codex` or `claude` only when it exactly
matches one of those names. Otherwise every argument is the focus. No harness
means automatic cross-harness selection. Preserve the focus verbatim.

The review is evidence, not a repair pass. Return its structured result without
editing, committing, pushing, or publishing. The detailed review stance and
output contract live in [`prompts/adversarial-review.md`](prompts/adversarial-review.md)
and [`schemas/review-output.schema.json`](schemas/review-output.schema.json).
The runner supplies both to the reviewer.

## 1. Resolve the target

Determine the current harness as `codex`, `claude`, or `unknown`. Any other
tool, Cursor included, is `unknown`. The runner rejects every other caller value. An `unknown` caller keeps model
independence explicitly `unverified`. It is never reported as same- or
cross-harness evidence.
Accept `--scope auto|working-tree|branch` and `--base <ref>` when supplied.
Otherwise use `auto`. A supplied base selects branch review. Pass the remaining
text as the exact focus.

Automatic routing is fixed:

| Caller | Reviewer order |
| --- | --- |
| Claude | Codex, then fresh Claude |
| Codex | Claude, then fresh Codex |
| Unknown | Codex, then Claude |

An explicit reviewer is tried first, then the caller as fallback when the
caller is supported. Availability requires an installed, authenticated CLI.

Completion: caller, requested reviewer, scope, base, and exact focus are
resolved without changing the repository.

## 2. Start the clean review

Resolve this skill's installed directory, then run its runner from the
repository worktree:

```text
node <skill-directory>/scripts/run-review.mjs start \
  --caller <caller> --harness <auto-or-reviewer> --scope <scope> \
  [--base <ref>] [--focus <exact-focus>]
```

Before launch, the runner collects the complete target diff with expanded
context under fixed file and byte limits. It never asks the reviewer to run Git
or reconstruct the target. If the complete target cannot be represented safely
inside those bounds, the review fails explicitly.

The runner launches a detached CLI process with a fresh session, no resume or
continue state, the shared adversarial prompt, and the shared output schema.
Claude runs with `--safe-mode`, a runner-owned system prompt, and an empty tool
set. User and project `CLAUDE.md`, auto-memory, skills, plugins, hooks, MCP
servers, shell commands, and network-capable tools are unavailable, while normal
OAuth and keychain authentication remains usable. Codex runs ephemerally in its
read-only sandbox and ignores the user's config, its rules, and the reviewed
repository's `AGENTS.md`, so a change under review cannot instruct its own
reviewer. Local job metadata and results live
under the current worktree's `.flow/reviews/`, the one per-worktree exception in
[Where ledgers live](../flow-mode/references/lifecycle.md#where-ledgers-live).
The runner refuses to start until `.flow/` is git-ignored. It refuses another
live job for the same target fingerprint, records a finite deadline, and stores
each executed harness's bounded raw stdout, stderr, and structured output mode
`0600` in its ignored job directory.

Completion: `start` returns one job id and the background worker reaches
`queued` or `running`. A launch error is reported as a failed check.

## 3. Collect the result

Poll without opening the worker log:

```text
node <skill-directory>/scripts/run-review.mjs status <job-id>
```

Keep the developer informed while the job runs. When complete, read the
validated result:

```text
node <skill-directory>/scripts/run-review.mjs result <job-id>
```

The first schema-valid structured review is authoritative. A substantive
`needs-attention` verdict ends selection. It never triggers another harness.
Any parseable review-shaped payload that violates the schema fails closed,
including misspelled verdicts and contradictory verdict and finding
combinations. The runner never shops for an approval after such a response.
Fallback occurs only for unavailable CLIs, process failures, or unparseable or
non-review output.
Inspect every recorded attempt. When the preferred harness is unavailable or
fails, report that harness and its exact failure before presenting the fallback
review. Never make a fallback look like the first choice succeeded. `status`
and `result` reconcile queued or running jobs against their worker and deadline,
transitioning dead or expired work to `failed`. If the reviewed HEAD, index,
tracked working tree, or untracked files changed, the result is stale and this
step starts a new review against the new target, including branch scope.

Completion: one current, schema-valid result exists, or every attempted
harness and its infrastructure failure are reported.

## 4. Return the gate

Return the reviewer harness, whether same-harness fallback occurred, target
metadata, bounded-input mode, reviewer isolation and instruction-source
evidence, every harness attempt and failure, verdict, summary, findings, and
next steps. Preserve every finding's severity, file, lines, confidence, body,
and recommendation. `approve` is a passing adversarial check.
`needs-attention`, failed, and stale are blocking. Same-harness fallback proves
context independence, not model independence.

Completion: the caller receives one explicit passing or blocking result tied
to the reviewed target, with no repository, tracker, or pull request mutation.
