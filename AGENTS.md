# Working on this kit

This repository is a skill kit. `install.sh` symlinks it into Claude Code and Codex, so an edit here changes the live tools on every machine that installed it. Treat every change as a change to running software.

## Layout

| Path | What lives there | Who edits it |
| --- | --- | --- |
| `skills/` | First-party skills: the `flow-*` delivery workflow and the everyday skills | You |
| `vendor/skills/` | Third-party skills, copied verbatim, with upstream recorded in `vendor/skills.lock.json` | Only by re-copying from upstream |
| `agents/roles/` | One source file per `flow-*` role agent | You |
| `agents/claude/`, `agents/codex/` | Agent definitions for each tool | Generated from `agents/roles/` by `tools/build_agents.py`; personal agents such as `js-ts-interview-drill.md` are written by hand |
| `skills/flow-setup/template/` | The files `/flow-setup` writes into other repositories | You |
| `tools/` | The validator, generators, and the usage miner | You |

## Rules

- Run `python3 tools/validate.py` before every commit. It must report 0 errors. It checks frontmatter, unique names, dead links, unknown slash commands and `pstack:` references, rendered agents and the README catalog, company-specific strings, em dashes in workflow prose, and stack-specific words inside `flow-*` skills.
- After editing a file in `agents/roles/`, run `python3 tools/build_agents.py`. After adding, removing, or renaming a skill, run `python3 tools/readme_catalog.py`. Never edit the generated agent files or the catalog block by hand.
- Follow the pstack Authoring a skill playbook for any `SKILL.md`. Write prose by the rules of `pstack:unslop`. Reference pstack skills as `pstack:<name>` and kit skills as `/<name>` or by their backticked name.
- Keep `flow-*` skills free of stack-specific commands. They read gates from the target repository's `AGENTS.md` `## Commands` table. Only `flow-setup` names package managers and build tools, because it detects them.
- Human-invoked skills keep `disable-model-invocation: true` in their frontmatter and `allow_implicit_invocation: false` in `agents/openai.yaml`.
- Never edit a vendored skill in place. To change one, fork it into `skills/` under the same name, delete the vendored copy, and remove its lock entry.
- Before adding or removing a skill, run `python3 tools/skill_usage.py` and decide from measured use.
- Run `./install.sh --dry-run` before `./install.sh`. The installer backs up real files it displaces into `.install-backup/` and never deletes them.
