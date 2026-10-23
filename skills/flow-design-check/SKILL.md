---
name: flow-design-check
description: Produce an optional design-drift review for a pinned UI change. Use after a pull request that changes UI is published, or when the developer asks whether UI code still matches the repository's design system.
---

# Flow design check

Run `/flow-design-check [--base <ref>] [--focus <text>]` as one fresh, read-only
advisory review. Its axis is **design drift**, meaning whether the UI code being
proposed still matches the repository's design authority. Behavioral correctness
belongs to `flow-code-review`. General structure and maintainability belong to
`flow-code-quality-review`.

Its verdict informs the developer. It never blocks draft publication or starts
an automatic repair or rereview cycle.

This check reads the repository profile. When `AGENTS.md` has no flow block,
return `BLOCKED` and suggest `/flow-setup`.

## 1. Pin the PR target

Use a supplied base SHA, HEAD SHA, diff hash, issue, and focus when present.
Otherwise fetch `origin/<base>`, with the base branch from
`docs/agents/pr-standard.md` `## Lifecycle`, use its merge-base with `HEAD`,
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

## 2. Resolve design authority

Read the files named by the `Design system` and `Conventions` rows of
`## Sources of truth` in `AGENTS.md`, the applicable accepted ADRs from the
`Decisions` row, any feature-local design document, and the issue's
binding design decisions. A row that reads `none` supplies no written authority.
Read the base and target versions of every changed design-authority file. A
current written rule outranks precedent. The nearest comparable UI supplies
precedent only where written authority is silent.

Map every UI-affecting hunk to the exact authority or precedent that establishes
its expected result. A change to design authority is intentional only when the
issue authorizes it, the same PR updates every required source and generated
artifact, and a changed decision has its ADR effect resolved. An
absent or conflicting answer is a design decision, not permission to infer a new
rule.

Completion: every UI-affecting hunk has an authority `path:line`, an evidenced
precedent, or one explicit unresolved design question. Every changed authority
file has its downstream effects accounted for.

## 3. Run the mechanical design gate

Run the `design` gate from the `## Commands` table in `AGENTS.md` against the
pinned target. Preserve the command, exit status, and each reported violation.
When the gate reads `n/a`, record `not-configured` and classify hunks by
authority and precedent alone. A command that runs and finds a violation is
failing design evidence. A configured command that cannot run is `BLOCKED`.
Attribute every violation before verdict. A violation introduced by the target
is `DRIFT`. One proven present at the base is a pre-existing `BLOCKED` gate. An
unresolved attribution is also `BLOCKED`.

Recompute HEAD, working-tree status, and the diff hash after the command. Any
change makes the target stale and restarts the check from step 1.

Completion: one current mechanical result or `not-configured` record exists for
the pinned target, or its unavailable or stale evidence is recorded.

## 4. Classify design drift

Assign every UI-affecting hunk exactly one classification:

- `CONFORMS` means current authority or evidenced precedent requires the target
  implementation.
- `INTENTIONAL CHANGE` means the issue authorizes a design-system change and the
  PR updates its authority, resolves its decision record and generated effects,
  and accounts for every affected consumer.
- `DRIFT` means the target diverges from an established rule or precedent
  without an authorized design change.
- `NEEDS DECISION` means authority is absent or conflicting, so human judgment
  must settle one named question.

Split a mixed hunk into the smallest independently assessable rows before
classification. One row carries one classification.

Audit the complete drift taxonomy:

- **Token drift.** Color, type, spacing, density, radius, shadow, or motion
  escapes the declared system.
- **Primitive drift.** PR code bypasses or duplicates the shared component that
  owns the visual structure.
- **Pattern drift.** Hierarchy, layout, variants, status language, or motion
  diverges from the applicable product or document pattern.
- **State drift.** Loading, empty, error, disabled, selected, or read-only UI
  diverges from its established representation.
- **Responsive drift.** Widths, wrapping, overflow, or breakpoint behavior
  diverges from the applicable rule or precedent.
- **Authority drift.** Code and design documents, ADRs, token sources,
  generated artifacts, or consumers no longer describe the same system.
- **Scope drift.** A UI change has no trace to the issue's accepted concern.

Each `DRIFT` finding cites the smallest useful changed `path:line`, the authority
`path:line`, the concrete UI consequence, and the required correction. Each
`NEEDS DECISION` item cites the conflicting or missing evidence and asks one
bounded question. Preferences without repository authority are decisions, not
findings.

Completion: every UI-affecting hunk is classified, all seven drift axes are
accounted for, and every finding or decision satisfies its evidence contract.

## 5. Return the gate

Recompute base, HEAD, working-tree status, and diff hash. Return:

```markdown
## Flow design check · PASS | FAIL | NEEDS DECISION | BLOCKED
Target: <base-sha>..<head-sha> · <diff-hash>

### Mechanical
<command, exit status, violations, or not-configured>

### Coverage
| Changed path:line | Classification | Drift axis | Authority or precedent | Evidence |

### Findings
| Changed path:line | Authority path:line | UI consequence | Required correction |

### Decisions
| Question | Missing or conflicting evidence | Owner |
```

Verdict precedence is fixed. `BLOCKED` outranks every other verdict when the
review cannot complete or its target is stale. `FAIL` outranks `NEEDS DECISION`
when any target-attributed mechanical violation or `DRIFT` exists. `NEEDS
DECISION` requires no proven drift and at least one unresolved authority
question. `PASS` requires a passing or `not-configured` mechanical gate and only
`CONFORMS` or `INTENTIONAL CHANGE` rows.

Completion: one current verdict accounts for the mechanical result and every
UI-affecting hunk, with no repository, tracker, or pull request mutation.
