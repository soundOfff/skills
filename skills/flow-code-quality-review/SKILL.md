---
name: flow-code-quality-review
description: Quality-review a pinned change (reuse, decomposition, maintainability) as flow-code-check's quality worker.
---

# Code quality review

Act as the leaf solution-quality reviewer for one pinned change. Read and obey
[`flow-code-check/WORKER-CONTRACT.md`](../flow-code-check/WORKER-CONTRACT.md), then
perform the review yourself. Your axis is codebase health. Requirement coverage
and runtime correctness belong to `flow-code-review` unless they establish the
maintenance impact of a structural defect.

## 1. Establish the local design

Read the repository instructions, conventions, relevant ADRs, and capability
entrypoints supplied in the packet. Search beyond the diff for existing owners,
interfaces, helpers, types, and tests that implement the same semantics. The
repository wins over generic patterns.

Completion: every changed responsibility has a known canonical owner and every
applicable repository rule has been identified.

## 2. Demand structural simplification

Inspect every meaningful change for:

- duplicated behavior or a new helper that an existing owner should absorb;
- feature logic in a shared path or logic placed outside its canonical layer;
- files, functions, components, or tests accumulating unrelated duties;
- scattered conditionals, repeated switches, nullable modes, flags, or fallbacks
  that reveal a missing state model or policy boundary;
- thin wrappers, pass-through layers, speculative generality, casts, untyped
  escape hatches, or optionality that hide the actual contract;
- data clumps, primitive domain concepts, feature envy, message chains,
  shotgun surgery, and divergent reasons to change;
- sequential orchestration or partial updates where a clearer atomic boundary
  already exists;
- comments that restate code, narrate edit history or agent activity, preserve a
  prompt, overclaim guarantees, or excuse temporary structure;
- tests coupled to implementation details, oversized mixed-purpose suites,
  duplicated fixtures, dead code, and stale documentation.

Prefer a required outcome that deletes concepts, branches, duplication, or
indirection. Splitting a file is valid only when the extracted module has a
coherent owner and interface. A smaller rearrangement of the same complexity
does not resolve the finding.

When the repository defines one, the size limit the `health` gate enforces is the
numeric floor, not an approval target. A shorter file can still mix
responsibilities. A grandfathered large file can still require decomposition
when this change makes its design worse. Cite the distinct structural
consequence instead of repeating the mechanical failure.

Completion: every changed responsibility has been tested for reuse, ownership,
decomposition, control-flow growth, boundary clarity, and maintainability.

## 3. Report solution quality only

Return the exact worker contract. Each finding identifies the structural debt
introduced or enlarged by this change and the required design outcome. Generic
cleanups, naming preferences, and alternate designs without a demonstrated
maintenance cost do not meet the finding bar.

`PASS` means the change reuses the canonical owners, adds no evidenced
duplication or architectural drift, and keeps its responsibilities direct and
cohesive. Missing repository context needed to make that judgment returns
`BLOCKED`.

Completion: the report contains only solution-quality findings with repository
evidence, or an explicit contract-valid `PASS` or `BLOCKED`.
