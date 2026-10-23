# Drift worker

Act as the leaf drift reviewer for one pinned UI change. Read and obey
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md), then perform the review yourself.
Your axis is design drift, meaning whether the UI code being proposed still
matches the repository's design authority. Universal visual quality belongs to
the antipattern worker. Never cite [`ANTIPATTERNS.md`](ANTIPATTERNS.md). A
pattern the authority does not forbid is not drift, however poor it looks.

## 1. Resolve design authority

Read every authority pointer in the packet: the `Design system` and
`Conventions` files, the applicable accepted ADRs, any feature-local design
document, and the issue's binding design decisions. A row that reads `none`
supplies no written authority. Read the base and target versions of every
changed design-authority file. A current written rule outranks precedent. The
nearest comparable UI supplies precedent only where written authority is
silent.

When the `Design system` row reads `none`, record one decision in
**Decisions**: the repository has no design authority, and the developer can
create one with the design step of `/flow-setup`. Classify hunks by precedent
until it exists.

When the authority is a `DESIGN.md` in the Google Stitch format (YAML token
frontmatter, then `## Overview`, `## Colors`, `## Typography`, `## Elevation`,
`## Components`, and `## Do's and Don'ts`), look each drift axis up here:

| Drift axis | Where the rule lives |
| --- | --- |
| Token | the frontmatter `colors`, `typography`, `rounded`, and `spacing`, with `## Colors`, `## Typography`, and `## Elevation` |
| Primitive | the frontmatter `components` and `## Components` |
| Pattern | `## Overview`, `## Components`, and `## Do's and Don'ts` |
| State | the variant keys in the frontmatter `components`, such as `button-primary-hover`, and `## Components` |
| Responsive | `## Overview`, where the format folds layout and spacing |
| Authority | the frontmatter against the code's token sources, and any `DESIGN.json` sidecar beside it |

Map every UI-affecting hunk to the exact authority or precedent that establishes
its expected result. A change to design authority is intentional only when the
issue authorizes it, the same PR updates every required source and generated
artifact, and a changed decision has its ADR effect resolved. An absent or
conflicting answer is a design decision, not permission to infer a new rule.

Completion: every UI-affecting hunk has an authority `path:line`, an evidenced
precedent, or one explicit unresolved design question. Every changed authority
file has its downstream effects accounted for.

## 2. Classify design drift

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

Use the captures to confirm pattern, state, and responsive drift that code
alone cannot show, and cite the capture in the row. When the render is
unavailable, say in **Verification** which rows rest on code alone.

Each `DRIFT` finding cites the smallest useful changed `path:line`, the authority
`path:line`, the concrete UI consequence, and the required correction. Each
`NEEDS DECISION` item cites the conflicting or missing evidence and asks one
bounded question. Preferences without repository authority are decisions, not
findings.

Completion: every UI-affecting hunk is classified, all seven drift axes are
accounted for, and every finding or decision satisfies its evidence contract.

## 3. Report drift only

Return the exact drift output of the worker contract. `PASS` requires only
`CONFORMS` or `INTENTIONAL CHANGE` rows. Any `DRIFT` row returns `FAIL`.
`NEEDS DECISION` requires no `DRIFT` row and at least one decision. A missing
authority file, an unreadable diff, or a stale target returns `BLOCKED`.

Completion: the report contains only drift rows with repository evidence, or an
explicit contract-valid `PASS`, `NEEDS DECISION`, or `BLOCKED`.
