---
name: diagnose
description: Disciplined diagnosis loop for hard bugs and performance regressions. Build a tight feedback loop, then reproduce, minimise, hypothesise, instrument, fix, and add a regression test. Use when the user says "diagnose this" or "debug this", reports a bug, says something is broken, throwing, failing, or slow, or describes a performance regression.
---

# Diagnose

A discipline for hard bugs. Skip phases only when explicitly justified.

The caller sets the mutation boundary. `/flow-help` leaves tracked paths
unchanged and uses the final phases to name the regression seam and clean
scratch artifacts. A `/flow-build` bug assignment runs every phase through fix
and regression proof.

When exploring the codebase, read the domain language and check the decision
records in the area being investigated. `docs/agents/domain.md` says where they
live. Without it, read `CONTEXT.md` and `docs/adr/` when they exist.

## Phase 1. Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug, one that goes red on _this_ bug, you will find the cause. Bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one, roughly in this order

1. **Failing test** at whatever seam reaches the bug, whether unit, integration, or end-to-end.
2. **Curl or HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright, Puppeteer) that drives the UI and asserts on the DOM, console, or network.
5. **Replay a captured trace.** Save a real network request, payload, or event log to disk. Replay it through the code path in isolation.
6. **Throwaway harness.** Spin up a minimal subset of the system (one service, mocked deps) that exercises the bug code path with a single function call.
7. **Property or fuzz loop.** If the bug is "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through the old version and the new version (or two configs) and diff the outputs.
10. **HITL bash script.** Last resort. If a human must click, drive _them_ with [`scripts/hitl-loop.template.sh`](scripts/hitl-loop.template.sh) so the loop is still structured. Captured output feeds back to you.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can I make it faster? (Cache setup, skip unrelated init, narrow the test scope.)
- Can I make the signal sharper? (Assert on the specific symptom, not "didn't crash".)
- Can I make it more deterministic? (Pin time, seed RNG, isolate filesystem, freeze network.)

A 30-second flaky loop is barely better than no loop. A 2-second deterministic one is tight, and it makes the rest of the diagnosis fast.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger 100×, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable. A 1% one is not, so keep raising the rate until it is.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for one of these:

- access to whatever environment reproduces it;
- a captured artifact (HAR file, log dump, core dump, screen recording with timestamps);
- permission to add temporary production instrumentation.

Do **not** proceed to hypothesise without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**. You can name **one command** (a script path, a test invocation, a curl) that you have **already run at least once**, with the invocation and its output pasted, and that is:

- [ ] **Red-capable.** It drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. "Runs without erroring" is not enough. It must be able to _catch this specific bug_.
- [ ] **Deterministic.** It gives the same verdict every run. For a flaky bug, that means a pinned, high reproduction rate, per above.
- [ ] **Fast.** Seconds, not minutes.
- [ ] **Agent-runnable.** You can run it unattended. A human joins the loop only through `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, **stop. Jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2. Reproduce and minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. The wrong bug leads to the wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps **one at a time**, re-running the loop after each cut. Keep only what the failure depends on.

A minimal repro shrinks the hypothesis space in Phase 3, because fewer moving parts are left to suspect. It also becomes the clean regression test in Phase 5.

Done when **every remaining element is load-bearing**, so removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3. Hypothesise

Generate **3 to 5 ranked hypotheses** before testing any of them. Generating a single hypothesis anchors on the first plausible idea.

Each hypothesis must be **falsifiable**. State the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is a vibe. Discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks it instantly ("we just deployed a change to #3"), or know hypotheses they've already ruled out. Don't block on it. Proceed with your ranking if the user is away.

## Phase 4. Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger or REPL inspection** if the environment supports it. One breakpoint beats ten logs.
2. **Targeted logs** at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, for example `[DEBUG-a4f2]`. Cleanup at the end becomes a single grep. Untagged logs survive. Tagged logs get removed.

**Perf branch.** For performance regressions, logs are usually wrong. Instead, establish a baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5. Fix and regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam is one where the test exercises the **real bug pattern** as it occurs at the call site. If the only available seam is too shallow (a single-caller test when the bug needs multiple callers, a unit test that can't replicate the chain that triggered the bug), a regression test there gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original, un-minimised scenario.

## Phase 6. Cleanup and post-mortem

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The hypothesis that turned out correct is stated in the commit or PR message, so the next debugger learns

**Then ask what would have prevented this bug.** If the answer involves architectural change (no good test seam, tangled callers, hidden coupling), record a scoped architecture finding in the caller's ledger or issue, and suggest `pstack:architect` for the redesign. Make the recommendation **after** the fix is in, not before. You have more information now than when you started.
