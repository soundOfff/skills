# Antipattern worker

Act as the leaf antipattern reviewer for one pinned UI change. Read and obey
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md), then perform the review yourself.
Your axis is universal visual quality, meaning whether the rendered change
shows antipatterns a trained designer would flag in any product, whatever its
design system says. Whether the change matches that design system belongs to
the drift worker. Never invent a repository rule. Every finding cites one entry
of [`ANTIPATTERNS.md`](ANTIPATTERNS.md) by id.

## 1. Load the catalog and the evidence

Read the catalog in full before looking at the change. It is long, so read
it in chunks and skip no category. It groups entries by category and gives
each an id, a symptom, a detection cue, a fix, and a grade.
Then read the screenshot index and every capture that shows a changed route or
component, at every viewport, color scheme, and motion setting captured. Read
the diff for every UI-affecting hunk and the shared primitives it touches.

When the packet carries a live address and your harness offers browser tools,
open it read-only to check what a static capture cannot show: hover, focus,
active, disabled, loading, empty, and error states, keyboard order, reduced
motion, text at 200% zoom, and the narrowest width before overflow. Never
start, stop, or restart a server. When the render is unavailable, work from the
diff and the catalog's code cues, and treat every finding as `code-only`.

Completion: the catalog, the captures, and the UI inventory are read, and the
list of states you could and could not observe is written down.

## 2. Walk every category

For each catalog category, check every changed element against the entries that
apply. Look at the whole screen, not only the changed pixels. A change can break
hierarchy, alignment, rhythm, or contrast elsewhere on the same screen, and
that consequence belongs to the change.

For each candidate, settle attribution before you grade it. Compare the base
version with `git show <base-sha>:<path>` and, when the index has a base
capture, with that capture. A defect already present at the base is
pre-existing. When attribution needs a base rendering the index lacks, say so
in **Verification** and mark the row `attribution: unproven`.

Then check the packet's authority pointers. When the design authority requires
the pattern, move the row to **Suppressed** with the authority `path:line`.

Grade each remaining finding with the catalog entry's grade. Demote or promote
only when the observed consequence demonstrates it, and say why in the row.
`POLISH` rows go to the **Polish** table.

Record each category in **Coverage** with one result: `clear`, `findings`,
`not-applicable` when the change touches nothing in the category, or
`unverified: <reason>` when the category needs a render or a state the
evidence lacks. Name what you checked against, such as the captures, the live
page, or the diff alone.

Completion: every catalog category has a **Coverage** row, and every finding
carries its catalog id, observed value, location, and attribution.

## 3. Report antipatterns only

Return the exact antipattern output of the worker contract. `FAIL` requires at
least one `BLOCKING` or `MAJOR` finding attributed to the change. `PASS` means
every applicable category is `clear` or `not-applicable`, or carries only
`POLISH` rows. A missing catalog, an unreadable capture set with no diff to
fall back on, or a stale target returns `BLOCKED`.

Completion: the report contains only catalog-backed findings with observed
evidence, or an explicit contract-valid `PASS` or `BLOCKED`.
