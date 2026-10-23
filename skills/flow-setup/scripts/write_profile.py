"""Write the flow repository profile from an answers file.

usage: python3 write_profile.py <repo> <answers.json> [--dry-run] [--overwrite <path>]...

<repo> may be any folder inside the repository. The profile goes to its git root.

The AGENTS.md flow block is managed. It is appended, or replaced between its
markers, and no byte outside the markers changes. CLAUDE.md gets an @AGENTS.md
import and .gitignore gets .flow/, each only when missing. A docs/agents/ file
that exists and differs from the template is kept and its diff printed. Pass
--overwrite <path> to replace it. The forge's pull request template is written
only when the repository has none.

A profile path that is a symlink is written through, so the link stays. When
CLAUDE.md and AGENTS.md are one file through a link, CLAUDE.md needs no import.
A path that resolves outside the repository is refused. An existing file keeps
its line endings and mode. A new file gets mode 0666 minus the umask.

Exit status is 2 when the repository, the answers, the markers, or a link are
invalid. Nothing is written in that case. Runs on Python 3.9, the version macOS
ships.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from doctor import (
    BLOCK_BEGIN,
    BLOCK_END,
    CLAUDE_IMPORT,
    FORGES,
    GATES,
    MERGE_STRATEGIES,
    PLACEHOLDER,
    PUBLISH_MODES,
    READY_LABEL,
    SOURCES,
    TEMPLATE,
    TRACKERS,
    git_root,
    template_text,
    template_version,
    valid_branch,
)

PR_TEMPLATE_DEFAULT = {"github": ".github/pull_request_template.md", "gitlab": ".gitlab/merge_request_templates/Default.md"}
CLOSING_REFERENCE = {"github": "Closes #<issue>", "gitlab": "Closes #<issue>", "linear": "Fixes <team>-<number>", "local": "Closes <issue id>"}
FLOW_IGNORES = {".flow", ".flow/", "/.flow", "/.flow/"}
CHOICES = {"forge": FORGES, "tracker": tuple(TRACKERS), "publish_mode": PUBLISH_MODES, "merge_strategy": MERGE_STRATEGIES}
TEXTS = ("base", "linear_team", "ready_label")
DEFAULTS = {"linear_team": "", "ready_label": READY_LABEL, "board": ""}
KEYS = (*CHOICES, *TEXTS, "commands", "sources", "board")
CELL_BREAKERS = ("|", "`", "\n", "\r")
MISSING = object()


class ProfileError(Exception):
    pass


class Target(NamedTuple):
    path: Path
    link: str
    old: str | None


class Change(NamedTuple):
    rel: str
    target: Target | None
    new: str | None
    asks: bool = False
    note: str = ""


def got(value: object) -> str:
    if value is MISSING:
        return "it is missing"
    if isinstance(value, dict):
        return "got an object"
    if isinstance(value, list):
        return "got a list"
    return f"got {json.dumps(value)}"


def breaks_cell(text: str) -> bool:
    return any(c in text for c in CELL_BREAKERS)


def mapping_problems(key: str, value: object, expected: tuple[str, ...]) -> list[str]:
    if not isinstance(value, dict):
        return [f"{key} must be an object with the keys {', '.join(expected)}; {got(value)}"]
    missing, extra = [k for k in expected if k not in value], sorted(set(value) - set(expected))
    if missing or extra:
        return [f"{key} needs exactly the keys {', '.join(expected)}; missing {missing}, extra {extra}"]
    return []


def answer_problems(answers: dict) -> list[str]:
    errors = []
    unknown = sorted(set(answers) - set(KEYS))
    if unknown:
        errors.append(f"unknown keys {', '.join(unknown)}; the answers are {', '.join(KEYS)}")
    for key, allowed in CHOICES.items():
        value = answers.get(key, MISSING)
        if value not in allowed:
            errors.append(f"{key} must be one of {', '.join(allowed)}; {got(value)}")
    for key in TEXTS:
        value = answers.get(key, MISSING)
        if not isinstance(value, str):
            errors.append(f"{key} must be a string; {got(value)}")
        elif breaks_cell(value):
            errors.append(f"{key} may not contain |, a backtick, or a line break, because it fills a table cell")
    if isinstance(answers.get("base"), str) and not valid_branch(answers["base"]):
        errors.append(f"base {json.dumps(answers['base'])} is not a valid branch name")
    if answers.get("ready_label") == "":
        errors.append(f"ready_label must name a label, such as {READY_LABEL}")
    if answers.get("tracker") == "linear" and answers.get("linear_team") == "":
        errors.append("linear_team must name the Linear team key, such as ENG")
    commands = answers.get("commands", MISSING)
    errors += mapping_problems("commands", commands, GATES)
    for gate, command in commands.items() if isinstance(commands, dict) else ():
        if not isinstance(command, str) or not command.strip():
            errors.append(f"commands.{gate} must be a command or n/a; {got(command)}")
        elif breaks_cell(command):
            errors.append(f"commands.{gate} may not contain |, a backtick, or a line break; point the gate at a script instead")
    sources = answers.get("sources", MISSING)
    errors += mapping_problems("sources", sources, SOURCES)
    for concern, paths in sources.items() if isinstance(sources, dict) else ():
        items = [paths] if isinstance(paths, str) else paths
        if not isinstance(items, list) or not all(isinstance(p, str) for p in items):
            errors.append(f"sources.{concern} must be a path, a list of paths, or none; {got(paths)}")
        elif any(breaks_cell(p) for p in items):
            errors.append(f"sources.{concern} may not contain |, a backtick, or a line break")
    board = answers.get("board")
    lines = [board] if isinstance(board, str) else board
    if not isinstance(lines, list) or not all(isinstance(line, str) for line in lines):
        errors.append(f"board must be Markdown text or a list of lines; {got(board)}")
    return errors


def load_answers(path: Path) -> dict:
    try:
        raw = json.loads(path.read_bytes().decode("utf-8"))
    except UnicodeDecodeError:
        raise ProfileError(f"{path} is not UTF-8 text")
    except json.JSONDecodeError as error:
        raise ProfileError(f"{path} is not valid JSON: {error}")
    if not isinstance(raw, dict):
        raise ProfileError(f"{path} must hold a JSON object; {got(raw)}")
    answers = {**DEFAULTS, **raw}
    errors = answer_problems(answers)
    if errors:
        raise ProfileError("\n".join([f"{path} has invalid answers:"] + [f"  {e}" for e in errors]))
    return answers


def existing_pr_template(root: Path, forge: str) -> str | None:
    if forge == "github":
        for folder in (root / ".github", root, root / "docs"):
            for entry in sorted(folder.iterdir()) if folder.is_dir() else []:
                if entry.is_file() and entry.name.lower() == "pull_request_template.md":
                    return entry.relative_to(root).as_posix()
        for entry in sorted((root / ".github").iterdir()) if (root / ".github").is_dir() else []:
            if entry.is_dir() and entry.name.lower() == "pull_request_template":
                found = sorted(entry.glob("*.md"))
                if found:
                    return found[0].relative_to(root).as_posix()
    if forge == "gitlab":
        folder = root / ".gitlab" / "merge_request_templates"
        found = sorted(folder.glob("*.md"), key=lambda p: (p.name != "Default.md", p.name)) if folder.is_dir() else []
        if found:
            return found[0].relative_to(root).as_posix()
    return None


def values(answers: dict, pr_template: str | None) -> dict[str, str]:
    board = answers["board"]
    vals = {key: answers[key] for key in ("base", "publish_mode", "merge_strategy", "forge", "tracker", "ready_label")}
    vals.update(
        version=template_version(),
        pr_template=f"`{pr_template}`" if pr_template else "none",
        closing_reference=CLOSING_REFERENCE[answers["tracker"]].replace("<team>", answers["linear_team"]),
        authorization_gate=template_text(TEMPLATE / "docs" / "agents" / "issue-tracker-gate.md").strip("\n"),
        board=("\n".join(board) if isinstance(board, list) else board).strip(),
    )
    for gate, command in answers["commands"].items():
        command = command.strip()
        vals[f"cmd:{gate}"] = "n/a" if command.lower() == "n/a" else f"`{command}`"
    for concern, paths in answers["sources"].items():
        paths = [paths] if isinstance(paths, str) else paths
        paths = [p.strip() for p in paths if p.strip() and p.strip().lower() != "none"]
        vals[f"src:{concern}"] = ", ".join(f"`{p}`" for p in paths) if paths else "none"
    return vals


def render(name: str, vals: dict[str, str]) -> str:
    text = template_text(TEMPLATE / name)
    unknown = sorted(set(PLACEHOLDER.findall(text)) - set(vals))
    if unknown:
        raise ProfileError(f"template {name} uses unknown placeholders {unknown}")
    return PLACEHOLDER.sub(lambda match: vals[match.group(1)], text)


def eol_of(text: str) -> str:
    crlf = text.count("\r\n")
    return "\r\n" if crlf and crlf * 2 > text.count("\n") else "\n"


def in_eol(text: str, like: str | None) -> str:
    eol = eol_of(like or "")
    return text if eol == "\n" else text.replace("\n", eol)


def appended(text: str, addition: str) -> str:
    eol = eol_of(text)
    addition = in_eol(addition, text)
    if not text:
        return addition + eol
    gap = "" if text.endswith(("\n\n", "\n\r\n")) else eol if text.endswith("\n") else eol * 2
    return text + gap + addition + eol


def splice(current: str | None, block: str) -> str:
    if not current:
        return block + "\n"
    begins, ends = list(BLOCK_BEGIN.finditer(current)), current.count(BLOCK_END)
    if not begins and not ends:
        return appended(current, block)
    if len(begins) == 1 and ends == 1 and begins[0].start() < current.index(BLOCK_END):
        end = current.index(BLOCK_END) + len(BLOCK_END)
        return current[: begins[0].start()] + in_eol(block, current) + current[end:]
    raise ProfileError(f"AGENTS.md has {len(begins)} begin and {ends} end markers; fix them by hand so one block remains")


def ignored(text: str | None) -> str:
    text = text or ""
    if FLOW_IGNORES & {line.strip() for line in text.splitlines()}:
        return text
    eol = eol_of(text)
    return text + ("" if not text or text.endswith("\n") else eol) + ".flow/" + eol


def locate(root: Path, rel: str) -> Target:
    path = root / rel
    real = Path(os.path.realpath(path))
    if not real.is_relative_to(root):
        raise ProfileError(f"{rel} resolves to {real}, outside the repository; point the link inside the repository or replace it with a file")
    if real.exists() and not real.is_file():
        raise ProfileError(f"{rel} is not a regular file")
    try:
        old = real.read_bytes().decode("utf-8") if real.is_file() else None
    except UnicodeDecodeError:
        raise ProfileError(f"{rel} is not UTF-8 text")
    return Target(real, real.relative_to(root).as_posix() if real != path else "", old)


def plan(root: Path, answers: dict) -> list[Change]:
    forge = answers["forge"]
    found = existing_pr_template(root, forge)
    pr_template = found or PR_TEMPLATE_DEFAULT.get(forge)
    vals = values(answers, pr_template)
    block = render("agents-block.md", vals).strip("\n")
    if not (BLOCK_BEGIN.match(block) and block.endswith(BLOCK_END)):
        raise ProfileError("template agents-block.md must start and end with the flow markers")
    agents, claude = locate(root, "AGENTS.md"), locate(root, "CLAUDE.md")
    changes = [Change("AGENTS.md", agents, splice(agents.old, block))]
    if claude.path == agents.path:
        changes.append(Change("CLAUDE.md", claude, None, note="one file with AGENTS.md through a link, so it needs no import"))
    elif claude.old is None:
        changes.append(Change("CLAUDE.md", claude, render("CLAUDE.md", vals)))
    elif CLAUDE_IMPORT.search(claude.old):
        changes.append(Change("CLAUDE.md", claude, claude.old))
    else:
        changes.append(Change("CLAUDE.md", claude, appended(claude.old, "@AGENTS.md"), note="adds the line @AGENTS.md"))
    gitignore = locate(root, ".gitignore")
    changes.append(Change(".gitignore", gitignore, ignored(gitignore.old)))
    for name in ("issue-tracker", "ticket-standard", "pr-standard", "domain"):
        rel = f"docs/agents/{name}.md"
        target = locate(root, rel)
        text = render(f"docs/agents/issue-tracker-{answers['tracker']}.md" if name == "issue-tracker" else rel, vals)
        if name == "issue-tracker" and vals["board"]:
            text += render("docs/agents/issue-tracker-board.md", vals)
        changes.append(Change(rel, target, in_eol(text, target.old), asks=True))
    if forge == "none":
        changes.append(Change("pull request template", None, None, note="no forge"))
    elif found:
        changes.append(Change(found, None, None, note="the repository already has a pull request template"))
    else:
        changes.append(Change(pr_template, locate(root, pr_template), render(".github/pull_request_template.md", vals)))
    written = [c for c in changes if c.new is not None]
    paths = [c.target.path for c in written]
    shared = sorted({c.rel for c in written if paths.count(c.target.path) > 1})
    if shared:
        raise ProfileError(f"{' and '.join(shared)} are one file through a link; the profile needs them apart")
    return changes


def umask() -> int:
    mask = os.umask(0)
    os.umask(mask)
    return mask


def write(path: Path, text: str) -> None:
    mode = path.stat().st_mode & 0o7777 if path.is_file() else 0o666 & ~umask()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def action(change: Change, overwrite: list[str]) -> str:
    if change.new is None:
        return "skip"
    old = change.target.old
    if old == change.new:
        return "same"
    if change.asks and old is not None and change.rel not in overwrite:
        return "keep"
    return "create" if old is None else "update"


def describe(change: Change, verb: str) -> str:
    link = change.target.link if change.target else ""
    notes = [change.note] if change.note else []
    if link and verb in ("create", "update"):
        notes.append(f"writes {link} through the link, which stays")
    if verb == "keep":
        notes.append(f"differs from the template; pass --overwrite {change.rel} to replace it")
    return f"{verb:<7} {change.rel}{' -> ' + link if link else ''}{' (' + '; '.join(notes) + ')' if notes else ''}"


def diff(change: Change) -> str:
    old = change.target.old or ""
    lines = difflib.unified_diff(old.splitlines(True), change.new.splitlines(True), f"a/{change.rel}", f"b/{change.rel}")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the flow repository profile.")
    parser.add_argument("repo", type=Path)
    parser.add_argument("answers", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="append", default=[], metavar="PATH")
    args = parser.parse_args()
    try:
        root, problem = git_root(args.repo)
        if root is None:
            raise ProfileError(f"{args.repo} is not inside a git repository: {problem}")
        changes = plan(root, load_answers(args.answers))
        unknown = set(args.overwrite) - {c.rel for c in changes if c.asks}
        if unknown:
            raise ProfileError(f"--overwrite accepts only docs/agents/ files, got {sorted(unknown)}")
        if args.dry_run:
            print("dry run: nothing written")
        verbs = []
        for change in changes:
            verb = action(change, args.overwrite)
            verbs.append(verb)
            print(describe(change, verb))
            if verb == "keep" or (args.dry_run and verb == "update"):
                print(diff(change), end="")
            if verb in ("create", "update") and not args.dry_run:
                write(change.target.path, change.new)
        if not {"create", "update", "keep"} & set(verbs):
            print("nothing to change")
    except (ProfileError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
