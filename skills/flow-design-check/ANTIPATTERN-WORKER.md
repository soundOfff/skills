# Antipattern worker

Act as the leaf antipattern reviewer for one pinned UI change. Read and obey
[`WORKER-CONTRACT.md`](WORKER-CONTRACT.md), then perform the review yourself.
Your axis is the observable effect of the change on the interface and its
users. The drift worker checks alignment with the design system. Every finding
cites one entry of [`ANTIPATTERNS.md`](ANTIPATTERNS.md) by id.

## 1. Select categories from the diff

Read the pinned diff and UI inventory first. Trace affected consumers of
changed shared primitives and tokens. Read only the catalog preface and
category index, stopping before **Sources**. Select categories whose concerns
the diff can affect, directly or through those consumers. An unavailable
render can leave a category unverified, but its applicability comes from
the change.

Read the screenshot index and the captures that show the affected routes or
components. Use the captured viewports, color schemes, and motion settings
that matter to the selected categories.

When the packet carries a live address and your harness offers browser tools,
open it read-only to check applicable states a capture cannot show, such as
keyboard focus or loading. Never start, stop, or restart a server. When the
render is unavailable, use the diff and mark supported findings `code-only`.

Completion: the diff explains the selected categories, and the evidence shows
which applicable checks can run.

## 2. Find and check relevant entries

Use [`read-catalog.py`](read-catalog.py) to list entry titles for the selected
category prefixes in one call. For each candidate title, identify the changed
value, behavior, or observed state that could meet the entry's symptom. Open
the bodies for those ids in one batch. A category can apply to the diff while
most of its entries have no plausible connection to the change.

```sh
python3 read-catalog.py titles FO ST
python3 read-catalog.py entries FO-02 ST-01
```

Run the helper by its absolute path from the reviewed worktree. For a cue that
the titles do not surface, use `titles --match <text> <prefix>` to search entry
text and return matching titles. Follow cross-references by exact id. Expand
to other categories when the diff or captures show an effect there, and reuse
entries you already opened.

Check the relevant entries and record which hunk or consumer makes each
category applicable. Check each affected concern before marking a category
`clear`.

For each candidate, settle attribution before you grade it. Compare the base
version with `git show <base-sha>:<path>` and, when the index has a base
capture, with that capture. A defect already present at the base is
pre-existing. When attribution needs a base rendering the index lacks, say so
in **Verification** and mark the row `attribution: unproven`.

For a finding about a changed link or CTA's label or destination, search the
base version of the same surface for the new label and destination. Check any
matching control in context. If another control already exhibits the same
defect, report that location under **Pre-existing** with the same catalog id
and base evidence. Keep the introduced occurrence in **Findings**. Reuse the
entry already read for the finding.

Then check the packet's authority pointers. When the design authority requires
the pattern, move the row to **Suppressed** with the authority `path:line`.

Use the catalog grade as a default for a confirmed defect. A `Detect` cue
starts an investigation. For `BLOCKING` or `MAJOR`, record a demonstrated user
consequence or an applicable requirement that the change fails. Explain any
grade change. Put supported craft issues without material impact in **Polish**.

Record each category from the index in **Coverage**. Use `not-applicable` for
an unselected category, `clear` or `findings` for a completed check, and
`unverified: <reason>` when an applicable check lacks evidence. Use `unverified`
even when another check in the same category produced a finding. Keep that
finding in its own table. Name what you checked and which evidence was missing.

Completion: every catalog category has a **Coverage** row, and every finding
carries its catalog id, observed value, location, and attribution.

## 3. Report antipatterns only

Return the exact antipattern output and verdict defined by the worker contract.

Completion: the report carries a contract-valid verdict and identifies any
applicable checks left unverified.
