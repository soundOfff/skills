---
issue: null
status: preflight
publish_mode: null
branch: null
worktree: null
base_sha: null
head_sha: null
diff_hash: null
pr_number: null
pr_url: null
updated_at: null
---

<!-- status: preflight | publication-ready | published | needs-decision | blocked -->
<!-- publish_mode: draft | ready, from the Publish mode row of AGENTS.md ## Settings, draft when absent -->

# PR publication

## Authority

| Issue | Build handoff or branch evidence | Binding comment | Assignee | Board fields | Review boundary |
| --- | --- | --- | --- | --- | --- |
|  | optional `.flow/builds/<issue>.md`, otherwise current branch evidence | none |  | not-applicable |  |

## Target

| Worktree | Branch | Fetched base | Base SHA | HEAD SHA | Diff hash | Merge commits | Clean |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | none |  |

## Scope map

| Changed path or group | Issue criterion or pointer | Disposition |
| --- | --- | --- |
|  |  | in-scope |

## Reported evidence

| Evidence | Result | Target | Source |
| --- | --- | --- | --- |
| Acceptance criteria | not run |  | none |
| UI proof | not run |  | none |
| `lint` gate | not run |  | none |
| `typecheck` gate | not run |  | none |
| `test` gate | not run |  | none |
| `build` gate | not run |  | none |

## Proposed PR

| Title | Body path or exact text | Diff budget | Risk | Screenshots |
| --- | --- | --- | --- | --- |
|  |  |  |  | not provided |

## Publication gate

- [ ] A tracked open work issue owns the complete diff.
- [ ] The optional build handoff or direct branch evidence matches this lane.
- [ ] The branch is clean, committed, rebased on fetched `origin/<base>`, and contains no merge commits.
- [ ] Every changed hunk maps to the issue and preserves its no-gos.
- [ ] The proposed title and body follow `docs/agents/pr-standard.md` `## Body` and the `Pull request template` setting, and include the `Closing reference` setting.
- [ ] Validation and UI evidence are reported honestly, including `not run`.
- [ ] An immediate pre-push fetch confirms the recorded base equals `origin/<base>`.

## Publication

| Pre-push base SHA | Remote branch | Expected remote SHA | Pushed SHA | PR | Publish mode verified |
| --- | --- | --- | --- | --- | --- |
|  |  | absent or exact SHA |  |  | yes |

## Review recommendations

| Diff signal | Recommended command | Reason | Invoked by this skill |
| --- | --- | --- | --- |
|  | none |  | no |

## Blocking state

`none`, or record the publication-integrity failure and exact human decision or external change required.
