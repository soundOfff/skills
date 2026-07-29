# personal-skills

My agent skills and workflow for **Claude Code** and **Codex**, in one place.

This repo is the source of truth. `install.sh` symlinks each skill into
`~/.claude/skills` and `~/.codex/skills`, so editing a file here takes effect in
both tools immediately — no copying, no drift between the two.

```bash
./install.sh              # link everything into Claude + the Codex subset
./install.sh --dry-run    # show what would change, touch nothing
./install.sh --claude-only
./install.sh --codex-only
./install.sh --all-codex  # give Codex every skill, not just the subset
```

Anything real that `install.sh` would displace is moved to
`.install-backup/<timestamp>/` first. The script never deletes a real file, and
re-running it is a no-op.

## Layout

```
skills/            my own skills — the ones I wrote or maintain by hand
vendor/skills/     third-party skills, vendored verbatim
vendor/skills.lock.json   upstream + commit hash for every vendored skill
agents/            subagent definitions
config/claude/     settings.json, settings.local.json   (reference copies)
config/codex/      config.toml, default.rules           (reference copies)
reference/         docs and upstream material that are not skills
codex-skills.txt   which skills Codex gets by default
install.sh
```

Files under `config/` are **reference copies only** — `install.sh` does not link
or apply them, because they hold machine-specific paths. Diff them by hand.

## Skills

### Your own skills

| Skill | What it does |
|---|---|
| `attack` | Grab a ready issue and drive it to a merged PR — one vertical slice, TDD-style. Use when the user wants to "attack" an issue, "grab"/"pick… |
| `create-pr` | Create a GitHub PR for the current branch with a structured body (brief description, testing points, how to test, what's missing) and attach… |
| `figma` | Use the Figma MCP server to fetch design context, screenshots, variables, and assets from Figma, and to translate Figma nodes into production… |
| `figma-implement-design` | Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and… |
| `frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components,… |
| `hunter` | Repo-wide adversarial audit across six specialty tracks (correctness, memory, performance, security, reliability, supply chain), each run… |
| `implement-figma` | Translates Figma designs into production-ready application code with 1:1 visual fidelity. Use when implementing UI code from Figma files, when… |
| `linear-ticket-workflow` | Skill for the full developer workflow: deciding what to work on next, taking Linear tickets, creating git branches, implementing fixes/features,… |
| `react-best-practices` | React and Next.js performance optimization guidelines from Vercel Engineering. This skill should be used when writing, reviewing, or refactoring… |
| `test-master` | Generates test files, creates mocking strategies, analyzes code coverage, designs test architectures, and produces test plans and defect reports… |
| `whats-next` | Suggests the 3 most impactful next actions based on full developer context — git, Linear, PRs, and current conversation. Prioritizes blockers,… |

### Vendored skills (third-party, by upstream)

**[mattpocock/skills](https://github.com/mattpocock/skills)** — 42  
`ask-matt` · `caveman` · `code-review` · `codebase-design` · `design-an-interface` · `diagnose` · `diagnosing-bugs` · `domain-modeling` · `edit-article` · `git-guardrails-claude-code` · `grill-me` · `grill-with-docs` · `grilling` · `handoff` · `implement` · `improve-codebase-architecture` · `migrate-to-shoehorn` · `obsidian-vault` · `prototype` · `qa` · `request-refactor-plan` · `research` · `resolving-merge-conflicts` · `review` · `scaffold-exercises` · `setup-matt-pocock-skills` · `setup-pre-commit` · `tdd` · `teach` · `to-issues` · `to-prd` · `to-spec` · `to-tickets` · `triage` · `ubiquitous-language` · `wayfinder` · `write-a-skill` · `writing-beats` · `writing-fragments` · `writing-great-skills` · `writing-shape` · `zoom-out`

**[better-auth/skills](https://github.com/better-auth/skills)** — 6  
`better-auth-best-practices` · `better-auth-security-best-practices` · `create-auth-skill` · `email-and-password-best-practices` · `organization-best-practices` · `two-factor-authentication-best-practices`

**[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)** — 5  
`design-taste-frontend` · `gpt-taste` · `imagegen-frontend-web` · `minimalist-ui` · `redesign-existing-projects`

**[blader/humanizer](https://github.com/blader/humanizer)** — 1  
`humanizer`

**[jakubkrehel/make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better)** — 1  
`make-interfaces-feel-better`

**[pbakaus/impeccable](https://github.com/pbakaus/impeccable)** — 1  
`impeccable`

**[twostraws/swiftui-agent-skill](https://github.com/twostraws/swiftui-agent-skill)** — 1  
`swiftui-pro`

**[vercel-labs/skills](https://github.com/vercel-labs/skills)** — 1  
`find-skills`


## How the live setup was wired before this repo

Worth recording, because it explains the layout:

- `~/.agents/skills/` held all 58 third-party skills as real directories,
  managed by a skill installer with `.skill-lock.json`. These are now
  `vendor/skills/`.
- `~/.claude/skills/` was a mix: 11 real directories (my own) plus 47 relative
  symlinks into `~/.agents/skills`, plus one absolute symlink for `hunter`.
- `~/.codex/skills/` held 10 skills as **byte-identical copies** of Claude's,
  kept in sync by hand. The symlink approach in `install.sh` removes that
  duplication — both tools now read the same files.

## Validation

All 69 skills parse as valid YAML frontmatter and declare both `name` and
`description`, checked with a real YAML parser rather than a regex:

```bash
python3 -m venv /tmp/v && /tmp/v/bin/pip install -q pyyaml
/tmp/v/bin/python tools/validate.py
```    

## hunter

`skills/hunter` ships a self-test. It stubs the model CLIs and exercises the
whole fan-out, so it is safe and cheap to run:

```bash
bash skills/hunter/scripts/selftest.sh   # 42 assertions
```
