# claude-code-workflows (external)

Upstream: <https://github.com/OneRedOak/claude-code-workflows>
Pinned at: `6a653445125da828f31af473fcdd3cf29f99be82`

An unmodified clone of this repo was sitting inside `~/.claude/skills/` as
`claude-code-workflows/`. It is **not a skill** — it has no `SKILL.md` and is
never loaded as one. It holds three workflow templates: `code-review`,
`design-review`, and `security-review`.

It is referenced rather than vendored, since it was a clean checkout with no
local changes. To get it back:

```bash
git clone https://github.com/OneRedOak/claude-code-workflows
git -C claude-code-workflows checkout 6a653445125da828f31af473fcdd3cf29f99be82
```

The `design-review/` material overlaps with
`reference/design-review-workflow/`, which holds the loose `design-*.md`
templates that were also loose in the skills directory.
