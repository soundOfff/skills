---
name: flow-setup
description: Install the flow kit on this machine, or profile a repository so the flow skills run there. In a repository, detect the forge, tracker, docs, and the stack's commands, then write the repository profile the flow skills read (the AGENTS.md flow block, the docs/agents standards, the pull request template, and the .flow/ ignore). With `machine`, link the kit's skills and agents into Claude Code and Codex and check pstack. Use for /flow-setup, when a flow skill reports a missing profile, or when the flow agents are not installed.
disable-model-invocation: true
argument-hint: '[machine]'
---

# Flow setup

`/flow-setup` writes the repository profile. `/flow-setup machine` installs the kit on this machine. Run machine mode when the argument is `machine`, when the working directory is not inside a git repository, or when this harness has no `flow-code-mapper` agent. Otherwise run repo mode. When machine mode ran without the `machine` argument inside a git repository, continue with repo mode afterward.

`<skill>` below is this skill's folder. It holds the templates in `template/`, the writer `scripts/write_profile.py`, and the doctor `scripts/doctor.py`. The doctor checks the profile contract that the flow skills rely on.

## Repo mode

The profile is the managed block in `AGENTS.md`, a `CLAUDE.md` that imports it, the five files in `docs/agents/`, the forge's pull request template, and a `.gitignore` entry for `.flow/`. The writer owns every file write. Never edit these files by hand during setup.

### 1. Explore

Read only. Change nothing. When `.flow/setup.json` exists, it holds the answers of the last run on this clone. Start from it and check each value against the repository again.

| Answer | How to find it |
| --- | --- |
| `forge`, `repo` | `git remote get-url origin`. A `github.com` or GitHub Enterprise host is `github`, and a `gitlab.com` host or one with `gitlab` in its name is `gitlab`. Anything else, or no remote, is `none`. `repo` is the remote path without `.git`, such as `owner/name`. |
| `base` | `git symbolic-ref --short refs/remotes/origin/HEAD` without the `origin/` prefix. Otherwise `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`. Otherwise the current branch. |
| `tracker` | The forge's issues (`github` or `gitlab`). Linear issue ids such as `ABC-123` in branch names, commit subjects, or the pull request template, or `linear.app` links in the docs, suggest `linear`. Without a forge, recommend `local`. |
| `linear_team` | The id prefix in those Linear references. |
| `merge_strategy` | `gh repo view --json squashMergeAllowed,rebaseMergeAllowed,mergeCommitAllowed`, or `merge_method` and `squash_option` from `glab api projects/:id`, where GitLab's `ff` and `rebase_merge` mean `rebase` and a `squash_option` of `always` means `squash`. When exactly one method is allowed, use it. Otherwise read the base branch history. Merge commits mean `merge`, subjects ending in `(#123)` mean `squash`, and a linear history without those suffixes means `rebase`. |
| `commands` | The stack table below. |
| `sources` | The sources table below. Each value is `none` or the repository-relative paths that exist. |
| `labels` | The tracker's label list. Map a triage role to an existing label only when it clearly means the same thing. Otherwise leave the role out and the label equals the role. |

Also read the existing `AGENTS.md` and whether it has a flow block, `CLAUDE.md` and whether it imports `@AGENTS.md`, `docs/agents/`, any pull request template, and `.gitignore`. For GitHub, check for a project board with `gh project list --owner <owner>`. A missing token scope is not a blocker. Note it and move on.

| Concern | Look for |
| --- | --- |
| Domain language | `CONTEXT-MAP.md`, `CONTEXT.md`, `docs/glossary.md`, `GLOSSARY.md`, `UBIQUITOUS_LANGUAGE.md` |
| Decisions | `docs/adr/`, `docs/decisions/`, `doc/adr/`, `docs/architecture/decisions/`, `adr/` |
| Conventions | `CONTRIBUTING.md`, `docs/conventions.md`, `STYLEGUIDE.md`, `docs/style-guide.md` |
| Design system | `DESIGN.md`, token files such as `tokens.json` or `*.tokens.json`, a design-system or UI package folder, `.storybook/` |
| Structure | `PROJECT_STRUCTURE.md`, `ARCHITECTURE.md`, `docs/architecture.md` |

Each gate is the command that does one job:

| Gate | Job |
| --- | --- |
| `install` | Install dependencies from the lockfile without changing it. |
| `dev` | Start the app or dev server locally. |
| `format` | Rewrite files into the repository's format. |
| `lint` | Run static checks and fail on violations. |
| `typecheck` | Type-check without emitting output. |
| `test` | Run the whole unit and integration suite. |
| `test-file` | Run one test file, with `<path>` where the path goes. |
| `e2e` | Run the end-to-end or browser suite. |
| `build` | Produce the production build or compile. |
| `design` | Check design-system rules such as token use or contrast. |
| `health` | Check code health such as size limits or dead code. |

Read the commands from the manifests:

| Signal | Install | Other gates |
| --- | --- | --- |
| `package.json` with `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` | `pnpm run <script>` |
| `package.json` with `yarn.lock` | `yarn install --immutable`, or `--frozen-lockfile` for Yarn 1 | `yarn <script>` |
| `package.json` with `bun.lock` or `bun.lockb` | `bun install --frozen-lockfile` | `bun run <script>` |
| `package.json` with `package-lock.json` | `npm ci` | `npm run <script>` |
| `pyproject.toml` with `uv.lock` | `uv sync` | `uv run <tool>` |
| `pyproject.toml` with `poetry.lock` | `poetry install` | `poetry run <tool>` |
| `requirements*.txt`, or a bare `pyproject.toml` | `pip install -r requirements.txt`, or `pip install -e .` | `python -m <tool>` |
| `Cargo.toml` | `cargo fetch` | `cargo fmt`, `cargo clippy -- -D warnings`, `cargo test`, `cargo build --release` |
| `go.mod` | `go mod download` | `gofmt -w .`, `go vet ./...`, `go test ./...`, `go build ./...` |
| `Gemfile` | `bundle install` | `bundle exec rubocop`, `bundle exec rspec` or `bundle exec rake test` |
| `mix.exs` | `mix deps.get` | `mix format`, `mix credo`, `mix test`, `mix compile --warnings-as-errors` |
| `gradlew` or `build.gradle(.kts)` | `./gradlew dependencies` | `./gradlew check`, `./gradlew test`, `./gradlew build` |
| `mvnw` or `pom.xml` | `./mvnw dependency:resolve` | `./mvnw test`, `./mvnw verify` |
| `Makefile`, `justfile`, `Taskfile.yml` | a target named for the job | `make <target>`, `just <recipe>`, `task <name>` |

- A script, target, or recipe the repository declares wins over a raw tool, because it carries the repository's flags. Match `package.json` scripts by name, such as `typecheck`, `type-check`, or `tsc` for `typecheck`, and `e2e` or `test:e2e` for `e2e`.
- For Python, the `[tool.*]` sections of `pyproject.toml` name the tools, such as `ruff check .` for `lint`, `ruff format .` for `format`, `mypy` or `pyright` for `typecheck`, and `pytest` for `test` with `pytest <path>` for `test-file`.
- CI config (`.github/workflows/`, `.gitlab-ci.yml`) shows which commands the team gates on. When CI and a script disagree, prefer what CI runs.
- A gate the repository has no command for reads `n/a`. Never invent a command or add a tool to fill a gate.
- A command may not contain `|` or a backtick. Point the gate at a script or a target instead.

Completion: every answer has a value with its evidence, or it is on the question list for step 2.

### 2. Ask

Present the findings as one table of answer, value, and evidence. Then ask, in one numbered round, only what exploration could not settle. Lead each question with the recommended answer so the user can accept it in a word.

- The tracker, when the remote does not decide it: GitHub, GitLab, Linear, or Local.
- The Linear team key, when the tracker is Linear and no reference revealed it.
- The publish mode, `draft` or `ready`. Recommend `draft`, which keeps a pull request out of review until the developer has verified it.
- Each gate with no inferable command. Recommend the closest command found, or `n/a`.
- Whether flow skills should maintain a project board, only when exploration found one. Recommend no.

Completion: the user answered the round, and every answer has a value.

### 3. Write

Create `.flow/` when it is missing and write the answers to `.flow/setup.json`:

```json
{
  "forge": "github",
  "repo": "owner/name",
  "tracker": "github",
  "linear_team": "",
  "base": "main",
  "publish_mode": "draft",
  "merge_strategy": "squash",
  "commands": {"install": "...", "dev": "...", "format": "...", "lint": "...", "typecheck": "...", "test": "...", "test-file": "... <path>", "e2e": "n/a", "build": "...", "design": "n/a", "health": "n/a"},
  "sources": {"Domain language": "none", "Decisions": "none", "Conventions": "none", "Design system": "none", "Structure": "none"},
  "labels": {},
  "board": ""
}
```

Leave `board` empty unless the user asked flow skills to maintain a board. Then fill it with the Markdown body of the `## Board` section in `docs/agents/issue-tracker.md`. It names the board and its link, the command that adds an issue, the status field with its values for to do, in progress, and done, and every other field a skill must set, with its allowed values and the command that sets it. Skills read the section's presence as a requirement, so an empty `board` leaves it out.

Run `python3 <skill>/scripts/write_profile.py <repo> <repo>/.flow/setup.json --dry-run`. It prints one line per file. `create` and `update` will be written. `same` needs nothing. `keep` means an existing `docs/agents/` file differs from the template, and the writer prints its diff. Show each `keep` diff to the user and ask yes or no for each file in one round.

Then run the same command without `--dry-run`, adding `--overwrite <path>` for each yes. The writer replaces only the text between `<!-- flow:begin -->` and `<!-- flow:end -->` in an existing `AGENTS.md`, or appends the block when there is none. It creates `CLAUDE.md` only when missing and otherwise adds an `@AGENTS.md` line when the import is absent. Tell the user when it added that line. It writes the pull request template only when the forge has none: `.github/pull_request_template.md` for GitHub and `.gitlab/merge_request_templates/Default.md` for GitLab. It appends `.flow/` to `.gitignore` once.

Completion: the writer exited 0, and every `keep` file has the user's answer.

### 4. Check and hand off

Run `python3 <skill>/scripts/doctor.py repo <repo>` and paste its output in the reply.

- A FAIL that comes from an answer, such as a missing source path, means a wrong answer. Fix the answer and return to step 3.
- A FAIL for a gate whose tool is not on PATH stays in the report. Name the tool and leave installing it to the user, because the golden rules forbid adding tools unasked.
- Text outside the managed block that repeats or contradicts it, such as an older commands list, goes in the report. Never edit it.

Leave every change uncommitted. Tell the user how to review and commit it on a branch:

```bash
git status --short && git diff
git switch -c chore/flow-setup
git add AGENTS.md CLAUDE.md .gitignore docs/agents <pull request template path>
git commit -m "chore: add the flow repository profile"
```

Completion: the reply holds the doctor output, each remaining FAIL or WARN with its cause, and the review and commit commands.

## Machine mode

### 1. Find the kit

The installed skill is a symlink into the kit. Resolve this skill's real path with `realpath <skill>`. The kit root is two folders above it and holds `install.sh`. When `install.sh` is not there, this copy is not linked from a kit clone. Stop and ask the user for the path of their kit clone.

Completion: the kit root is known and holds `install.sh`.

### 2. Install

From the kit root, run `./install.sh --dry-run` and show its output. Then run `./install.sh`. It links every kit skill into `~/.claude/skills` and `~/.codex/skills`, and every agent into `~/.claude/agents` and `~/.codex/agents`. It moves any real file it would displace into the kit's `.install-backup/` folder, and it prunes links into the kit whose source is gone. Report the backup folder when it names one.

Completion: `./install.sh` exited 0 and its summary line is in the reply.

### 3. Check

Run `python3 <kit>/skills/flow-setup/scripts/doctor.py machine` and paste its output. Every FAIL and WARN line comes with its fix. Print those fixes for the user and do not run them, because plugin installs are interactive and the skills CLI owns `~/.agents/skills`.

- Claude Code without pstack: run `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`, inside a Claude Code session.
- Codex without pstack: run `codex plugin marketplace add michael-denyer/pstack-claude`, then `codex plugin add pstack@pstack-claude`, in a terminal.
- Missing model rules: run `/pstack:setup-pstack` in Claude Code or `$setup-pstack` in Codex, in each harness that lacks them.
- A skill in both the kit and `~/.agents/skills`: Codex reads both folders and sees two copies. Run `npx skills remove -g <names>` with the names the doctor lists, then `./install.sh` from the kit root, because the skills CLI also removes agent links that share those names.

New skills and agents load in the next session of each harness.

Completion: the reply holds the doctor output and the exact command for every FAIL and WARN.
