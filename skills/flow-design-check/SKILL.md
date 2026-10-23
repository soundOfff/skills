---
name: flow-design-check
description: Produce an optional two-axis design review for a pinned UI change, design drift against the repository's design authority and universal visual antipatterns in the rendered result. Use after a pull request that changes UI is published, or when the developer asks whether UI code still matches the repository's design system or whether a screen looks right.
---

# Flow design check

Run `/flow-design-check [--base <ref>] [--focus <text>] [--url <address>]` as a
read-only advisory review. One coordinator dispatches exactly two fresh workers.
The drift worker judges whether the UI code still matches the repository's
design authority. The antipattern worker judges whether the rendered UI shows
visual antipatterns that no design authority would want. The workers receive
the same packet but cannot read each other's report or delegate further.
Behavioral correctness belongs to `flow-code-review`. General structure and
maintainability belong to `flow-code-quality-review`.

Before dispatch, read and enforce [`WORKER-CONTRACT.md`](WORKER-CONTRACT.md).
The coordinator validates that contract. It does not replace a missing worker
with its own review. This check may inspect files, run non-mutating commands,
start the repository's dev server on a dedicated port, and take screenshots.
It edits no code, tracker item, commit, branch, or pull request. Its verdict
informs the developer. It never blocks draft publication or starts an
automatic repair or rereview cycle.

This check reads the repository profile. When `AGENTS.md` has no flow block,
return `BLOCKED` and suggest `/flow-setup`.

## 1. Pin the UI target

Use a supplied base SHA, HEAD SHA, diff hash, issue, and focus when present.
Otherwise fetch `origin/<base>`, with the `Base branch` setting from
`AGENTS.md` `## Settings`, use its merge-base with `HEAD`,
require a clean working tree, and compute:

```text
git diff --binary <base-sha>...<head-sha> | git hash-object --stdin
```

Record the commit list, changed files, and diff command. Inventory every
UI-affecting hunk, including UI code, styles, assets, shared primitives, design
documents, token sources or outputs, and configuration that changes rendered
design. An empty UI inventory is `BLOCKED`, not a design approval.

Completion: one non-empty UI target is identified by base SHA, HEAD SHA, diff
hash, and clean working-tree status, and every UI-affecting hunk is inventoried.

## 2. Collect authority pointers and render the target

Collect the authority pointers without judging them: the files named by the
`Design system` and `Conventions` rows of `## Sources of truth` in
`AGENTS.md`, the applicable accepted ADRs from the `Decisions` row, any
feature-local design document, the issue's binding design decisions, and the
base and target versions of every changed design-authority file. Record a row
that reads `none` as `none`. The drift worker reads and interprets them.

Render the target once, so both workers see the same pixels. Use the first
source that works:

1. The `--url` address, when the developer supplied one.
2. The `dev` gate from the `## Commands` table in `AGENTS.md`, run in this
   worktree on a dedicated port. Verify which checkout the port serves before
   capturing anything, for example with `lsof -p <pid> | grep cwd`. Several
   dev servers can split localhost across IPv4 and IPv6 on one port.

Drive the page with the browser tools your harness provides, or with the
repository's own browser automation named by the `e2e` gate. Capture every
changed route, or a page that mounts every changed component, at a 375px and
a 1280px viewport, in each color scheme the repository supports, and once with
reduced motion when the change touches motion. Capture the base version of the
same screens when the diff makes attribution unclear, such as a change to a
shared primitive or a token. Save the captures under
`<.flow>/design-check/<diff-hash>/`, resolving `.flow` as
[lifecycle.md](../flow-mode/references/lifecycle.md#where-ledgers-live)
describes, with an index that names each capture's route or component,
viewport, color scheme, motion setting, checkout SHA, and port. Stop every
process you started.

When no source works, because the `dev` gate reads `n/a`, the server fails, or
the harness has no browser tools and the `e2e` gate reads `n/a`, record
`render: unavailable` with the reason and continue code-only. Say so in the
final report. An unavailable render narrows the antipattern axis. It does not
block the check.

Build the packet exactly from the **Input** section of
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md).

Completion: every authority pointer resolves to a path or `none`, and either a
capture index exists for the pinned target or `render: unavailable` names its
reason.

## 3. Start the independent pair

In one parallel dispatch, start exactly two fresh read-only workers:

1. **Drift.** Require [`DRIFT-WORKER.md`](DRIFT-WORKER.md).
2. **Antipatterns.** Require [`ANTIPATTERN-WORKER.md`](ANTIPATTERN-WORKER.md)
   and [`ANTIPATTERNS.md`](ANTIPATTERNS.md).

Give both the complete packet and [`WORKER-CONTRACT.md`](WORKER-CONTRACT.md).
State that each worker is a leaf. It performs its own repository legwork and
returns one report without spawning or consulting another agent. Use a fresh
generic worker process that loads the named worker file, under the execution
rules in [`dispatch.md`](../flow-mode/references/dispatch.md#execution-rules).
Give the antipattern worker the harness's browser tools when it has them, so it
can inspect states a static capture cannot show. Do not select a
harness-provided reviewer role whose own output schema can override the
worker contract. Do not collapse both axes into one worker, let the drift
worker cite the catalog, or let the antipattern worker infer a repository
rule.

Completion: two workers with different named axes are running concurrently
against the identical base, HEAD, diff hash, UI inventory, and capture index.

## 4. Run the mechanical design gate

While the pair runs, run the `design` gate from the `## Commands` table in
`AGENTS.md` against the pinned target. Preserve the command, exit status, and
each reported violation. When the gate reads `n/a`, record `not-configured`. A
command that runs and finds a violation is failing design evidence. A
configured command that cannot run is `BLOCKED`. Attribute every violation
before verdict. A violation introduced by the target is failing evidence. One
proven present at the base is a pre-existing `BLOCKED` gate. An unresolved
attribution is also `BLOCKED`.

Completion: one current mechanical result or `not-configured` record exists for
the pinned target, or its unavailable or stale evidence is recorded.

## 5. Validate the reports

Wait for both workers. Check every report against `WORKER-CONTRACT.md`. Verify
that each changed `path:line` exists in the diff, each authority `path:line`
says what the row claims, each cited capture exists in the index, each catalog
id exists in [`ANTIPATTERNS.md`](ANTIPATTERNS.md), and each finding's
attribution to the target holds. Remove unsupported findings and record the
reason. Preserve supported findings under their original axis.

When both axes flag the same hunk, keep both rows and mark the overlap. A drift
row and an antipattern row describe different defects. When the drift report
shows that the authority requires a pattern the antipattern report flags, the
authority wins: move the antipattern row to its **Suppressed** table with the
authority `path:line`. When the antipattern report flags a pattern the
authority is silent on, the row stands, and the drift axis may still carry a
decision about whether the authority should settle it.

Recompute `HEAD`, working-tree status, and the diff hash. Any change makes both
reports, the captures, and the mechanical result stale. Restart the check
against the new target.

Completion: two contract-valid reports and the mechanical result describe one
unchanged target, or the exact missing, malformed, or stale evidence is known.

## 6. Return the gate

Return:

```markdown
## Flow design check · PASS | FAIL | NEEDS DECISION | BLOCKED
Target: <base-sha>..<head-sha> · <diff-hash>
Render: <n> captures in <path> · <checkout sha> · port <n> | unavailable: <reason>

### Mechanical
<command, exit status, violations, or not-configured>

### Drift
<validated drift report: Coverage, Findings, Decisions, Verification>

### Antipatterns
<validated antipattern report: Findings, Polish, Suppressed, Pre-existing, Coverage, Verification>
```

Verdict precedence is fixed. `BLOCKED` outranks every other verdict when a
worker is missing, a report is invalid, a configured gate cannot run, or the
target is stale. `FAIL` outranks `NEEDS DECISION` when any target-attributed
mechanical violation, any `DRIFT` row, or any `BLOCKING` or `MAJOR` antipattern
exists. `NEEDS DECISION` requires no `FAIL` cause and at least one unresolved
authority question. `PASS` requires a passing or `not-configured` mechanical
gate, only `CONFORMS` or `INTENTIONAL CHANGE` drift rows, and no antipattern
above `POLISH`. An unavailable render never lowers a verdict on its own. The
report states which categories went unverified. A failing result returns to
the developer for repair. This skill never repairs the change.

Completion: one current verdict accounts for the mechanical result, both axes,
every UI-affecting hunk, and target freshness, with no repository, tracker, or
pull request mutation beyond the captures under `.flow/`.
