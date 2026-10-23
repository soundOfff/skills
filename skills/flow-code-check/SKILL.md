---
name: flow-code-check
description: Produce an optional consolidated correctness and solution-quality review for a pinned change. Use after a pull request is published, or when the developer asks to check a branch's code.
---

# Flow code check

Run `/flow-code-check [--base <ref>] [--focus <text>]` as a read-only advisory review.
One coordinator dispatches exactly two fresh workers. `flow-code-review` judges
behavior. `flow-code-quality-review` judges the solution. The workers receive the
same target but cannot read each other's report or delegate further.

Before dispatch, read and enforce [`WORKER-CONTRACT.md`](WORKER-CONTRACT.md).
The coordinator validates that contract. It does not replace a missing worker
with its own review. This check may inspect files and run non-mutating commands.
It edits no code, tracker item, commit, branch, or PR.
Its verdict informs the developer. It never blocks draft publication or starts
an automatic repair or rereview cycle.

## 1. Pin the review packet

Resolve the repository root, current `HEAD`, and base. Use the supplied base.
Otherwise use the merge-base with `origin/<base>`, with the `Base branch`
setting from `AGENTS.md` `## Settings`, or the remote's default branch when
`AGENTS.md` has no flow block. Include working-tree changes when present. Reject
an unresolved base or empty change before dispatch.

Resolve the binding issue/spec from the supplied focus, the shared
[`.flow/builds/`](../flow-mode/references/lifecycle.md#where-ledgers-live),
branch commits, or issue references. Collect only the repository instructions
and ADRs applicable to changed paths. The `Conventions` and `Decisions` rows of
`## Sources of truth` in `AGENTS.md` say where they live. Pick capability
entrypoints by the capability routing in
[`dispatch.md`](../flow-mode/references/dispatch.md#capability-routing). Build
the packet exactly from the authoritative **Input** section of
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md), using those resolved pointers as its
issue, instruction, ADR, and capability inputs.

Completion: every **Input** item in `WORKER-CONTRACT.md` is present and the
packet identifies one stable, non-empty target.

## 2. Start the independent pair

In one parallel dispatch, start exactly two fresh read-only workers:

1. **Correctness.** Require
   [`flow-code-review/SKILL.md`](../flow-code-review/SKILL.md).
2. **Quality.** Require
   [`flow-code-quality-review/SKILL.md`](../flow-code-quality-review/SKILL.md).

Give both the complete review packet and
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md). State that each worker is a leaf. It
performs its own repository legwork and returns one report without spawning or
consulting another agent. Use a fresh generic worker process that loads the
named leaf skill, under the execution rules in
[`dispatch.md`](../flow-mode/references/dispatch.md#execution-rules). Do not
select a harness-provided reviewer role whose own output schema can override the
leaf contract. `WORKER-CONTRACT.md` remains authoritative. Do not substitute an
unnamed review axis or collapse both axes into one worker.

Completion: two workers with different named axes are running concurrently
against the identical base, HEAD, diff hash, and scope.

## 3. Run the mechanical gate

While the pair runs, execute the repository checks required by the packet. Read
the commands from the `## Commands` table in the `AGENTS.md` flow block. At
minimum run the `health` gate when it is configured, and the full gate (`lint`,
`typecheck`, `test`, and `build`, skipping any that read `n/a`). Record a
`health` gate that reads `n/a` as skipped.

When the repository has no `AGENTS.md` flow block, find the full-gate commands in
the repository's own manifests, such as its package scripts, task runner, or CI
workflow. Say so in the report, mark each found command `inferred`, and suggest
`/flow-setup`. A missing profile is not a pass. A full-gate step that neither
the profile nor a manifest defines is unavailable.

Reuse current, target-matching results for `typecheck`, `test`, and `build` when
the caller's ledger or an optional `/flow-build` handoff records them. Otherwise
run the missing gates. Record commands, exit status, and concise failure
evidence. A bypassed or unavailable command is blocking, not a pass.

Completion: every mechanical result is tied to the packet's target and none is
reported from memory or another SHA.

## 4. Validate the reports

Wait for both workers. Check every report against `WORKER-CONTRACT.md`. Verify
each finding's file and lines exist, the cited evidence is in scope, and the
impact follows from that evidence. Remove unsupported findings and record the
reason. Preserve supported findings under their original axis. Cross-reference
exact overlap instead of letting one axis hide the other.

Recompute `HEAD`, working-tree status, and the diff hash. Any change makes both
reports and mechanical results stale. Restart the check against the new target.

Completion: two contract-valid reports and all mechanical results describe one
unchanged target, or the exact missing, malformed, or stale evidence is known.

## 5. Return the gate

Return:

```markdown
## Flow code check · PASS | FAIL | BLOCKED
Target: <base-sha>..<head-sha> · <diff-hash>

### Mechanical
<command results>

### Correctness
<validated flow-code-review report>

### Solution quality
<validated flow-code-quality-review report>
```

`PASS` requires both workers to return `PASS`, every mechanical check to pass,
and the target to remain current. Any supported finding returns `FAIL`. Missing
workers, invalid reports, unavailable checks, or stale evidence return
`BLOCKED`. A failing result returns to the developer for repair. This skill
never repairs the change.

Completion: one explicit verdict accounts for both independent axes, every
mechanical check, and target freshness.
