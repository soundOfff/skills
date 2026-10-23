"""Write the flow repository profile from an answers file.

usage: python3 write_profile.py <repo> <answers.json> [--dry-run] [--overwrite <path>]...

The AGENTS.md flow block is managed: it is created, or replaced between its
markers, and text outside the markers is never changed. CLAUDE.md gets an
@AGENTS.md import and .gitignore gets .flow/, each only when missing. A
docs/agents/ file that already exists and differs from the template is kept and
its diff printed; pass --overwrite <path> to replace it. The forge's pull
request template is written only when the repository has none.

Exit status is 2 when the answers or the existing markers are invalid. Nothing
is written in that case.
"""

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
    SOURCES,
    TRACKERS,
    TRIAGE_ROLES,
)

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
PR_TEMPLATE_DEFAULT = {"github": ".github/pull_request_template.md", "gitlab": ".gitlab/merge_request_templates/Default.md"}
CLOSING_REFERENCE = {"github": "Closes #<issue>", "gitlab": "Closes #<issue>", "linear": "Fixes {linear_team}-<number>", "local": "Closes <issue id>"}
FLOW_IGNORES = {".flow", ".flow/", "/.flow", "/.flow/"}


class ProfileError(Exception):
    pass


class Change(NamedTuple):
    path: str
    old: str | None
    new: str
    asks: bool


def load_answers(path: Path) -> dict:
    answers = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for key, allowed in (("forge", FORGES), ("tracker", tuple(TRACKERS)), ("publish_mode", PUBLISH_MODES), ("merge_strategy", MERGE_STRATEGIES)):
        if answers.get(key) not in allowed:
            errors.append(f"{key} must be one of {', '.join(allowed)}, got {answers.get(key)!r}")
    if not str(answers.get("base", "")).strip():
        errors.append("base must name the base branch")
    needs_repo = answers.get("forge") in ("github", "gitlab") or answers.get("tracker") in ("github", "gitlab")
    if needs_repo and "/" not in str(answers.get("repo", "")):
        errors.append("repo must be <owner>/<name> for a GitHub or GitLab forge or tracker")
    if answers.get("tracker") == "linear" and not str(answers.get("linear_team", "")).strip():
        errors.append("linear_team must name the Linear team key")
    for key, expected in (("commands", GATES), ("sources", SOURCES)):
        got = answers.get(key, {})
        if not isinstance(got, dict) or set(got) != set(expected):
            have = set(got) if isinstance(got, dict) else set()
            errors.append(f"{key} needs exactly {', '.join(expected)}; missing {sorted(set(expected) - have)}, extra {sorted(have - set(expected))}")
    for gate, command in answers.get("commands", {}).items():
        if not str(command).strip() or "|" in str(command) or "`" in str(command):
            errors.append(f"command for {gate} must be non-empty with no | or backtick; wrap a pipeline in a script")
    unknown = set(answers.get("labels", {})) - set(TRIAGE_ROLES)
    if unknown:
        errors.append(f"labels has unknown roles {sorted(unknown)}")
    board = answers.get("board", "")
    if not isinstance(board, str) and not (isinstance(board, list) and all(isinstance(line, str) for line in board)):
        errors.append("board must be a Markdown string or a list of lines")
    if errors:
        raise ProfileError("\n".join(errors))
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
    out = {key: str(answers.get(key, "")) for key in ("base", "publish_mode", "merge_strategy", "repo", "linear_team")}
    out["closing_reference"] = CLOSING_REFERENCE[answers["tracker"]].format(linear_team=answers.get("linear_team", ""))
    out["pr_template"] = f"`{pr_template}`" if pr_template else "none"
    for gate, command in answers["commands"].items():
        command = str(command).strip()
        out[f"cmd:{gate}"] = "n/a" if command.lower() == "n/a" else f"`{command}`"
    for concern, paths in answers["sources"].items():
        paths = [paths] if isinstance(paths, str) else list(paths)
        paths = [p.strip() for p in paths if p.strip() and p.strip().lower() != "none"]
        out[f"src:{concern}"] = ", ".join(f"`{p}`" for p in paths) if paths else "none"
    for role in TRIAGE_ROLES:
        out[f"label:{role}"] = str(answers.get("labels", {}).get(role, role))
    board = answers.get("board", "")
    out["board"] = ("\n".join(board) if isinstance(board, list) else board).strip()
    return out


def render(template: str, vals: dict[str, str]) -> str:
    text = (TEMPLATE / template).read_text(encoding="utf-8")
    unknown = sorted({m[2:-2] for m in PLACEHOLDER.findall(text)} - set(vals))
    if unknown:
        raise ProfileError(f"template {template} uses unknown placeholders {unknown}")
    for key, value in vals.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def appended(text: str, addition: str) -> str:
    if not text:
        return addition + "\n"
    gap = "" if text.endswith("\n\n") else "\n" if text.endswith("\n") else "\n\n"
    return text + gap + addition + "\n"


def splice(current: str | None, block: str) -> str:
    if not current:
        return block + "\n"
    begins, ends = current.count(BLOCK_BEGIN), current.count(BLOCK_END)
    if begins == 0 and ends == 0:
        return appended(current, block)
    if begins == 1 and ends == 1 and current.index(BLOCK_BEGIN) < current.index(BLOCK_END):
        start, end = current.index(BLOCK_BEGIN), current.index(BLOCK_END) + len(BLOCK_END)
        return current[:start] + block + current[end:]
    raise ProfileError(f"AGENTS.md has {begins} begin and {ends} end markers; fix them by hand so one block remains")


def read(root: Path, rel: str) -> str | None:
    path = root / rel
    return path.read_text(encoding="utf-8") if path.is_file() else None


def plan(root: Path, answers: dict) -> tuple[list[Change], list[str]]:
    forge = answers["forge"]
    found = existing_pr_template(root, forge)
    pr_template = found or PR_TEMPLATE_DEFAULT.get(forge)
    vals = values(answers, pr_template)
    block = render("agents-block.md", vals).strip("\n")
    if not (block.startswith(BLOCK_BEGIN) and block.endswith(BLOCK_END)):
        raise ProfileError("template agents-block.md must start and end with the flow markers")
    changes = [Change("AGENTS.md", read(root, "AGENTS.md"), splice(read(root, "AGENTS.md"), block), False)]
    claude = read(root, "CLAUDE.md")
    if claude is None:
        changes.append(Change("CLAUDE.md", None, render("CLAUDE.md", vals), False))
    else:
        changes.append(Change("CLAUDE.md", claude, claude if CLAUDE_IMPORT.search(claude) else appended(claude, "@AGENTS.md"), False))
    ignore = read(root, ".gitignore")
    text = ignore or ""
    if not FLOW_IGNORES & {line.strip() for line in text.splitlines()}:
        text += ("" if not text or text.endswith("\n") else "\n") + ".flow/\n"
    changes.append(Change(".gitignore", ignore, text, False))
    docs = {
        "docs/agents/issue-tracker.md": f"docs/agents/issue-tracker-{answers['tracker']}.md",
        "docs/agents/ticket-standard.md": "docs/agents/ticket-standard.md",
        "docs/agents/pr-standard.md": "docs/agents/pr-standard.md",
        "docs/agents/domain.md": "docs/agents/domain.md",
        "docs/agents/triage-labels.md": "docs/agents/triage-labels.md",
    }
    rendered = {rel: render(template, vals) for rel, template in docs.items()}
    if vals["board"]:
        rendered["docs/agents/issue-tracker.md"] += render("docs/agents/issue-tracker-board.md", vals)
    changes += [Change(rel, read(root, rel), text, True) for rel, text in rendered.items()]
    notes = []
    if forge == "none":
        notes.append("skip    pull request template (no forge)")
    elif found:
        notes.append(f"skip    {found} (the repository already has a pull request template)")
    else:
        changes.append(Change(pr_template, None, render(".github/pull_request_template.md", vals), False))
    return changes, notes


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    if path.exists():
        os.chmod(tmp, path.stat().st_mode)
    os.replace(tmp, path)


def diff(change: Change) -> str:
    lines = difflib.unified_diff((change.old or "").splitlines(True), change.new.splitlines(True), f"a/{change.path}", f"b/{change.path}")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the flow repository profile.")
    parser.add_argument("repo", type=Path)
    parser.add_argument("answers", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="append", default=[], metavar="PATH")
    args = parser.parse_args()
    root = args.repo.resolve()
    try:
        changes, notes = plan(root, load_answers(args.answers))
        unknown = set(args.overwrite) - {c.path for c in changes if c.asks}
        if unknown:
            raise ProfileError(f"--overwrite accepts only docs/agents/ files, got {sorted(unknown)}")
    except (ProfileError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if args.dry_run:
        print("dry run: nothing written")
    for change in changes:
        if change.old == change.new:
            print(f"same    {change.path}")
            continue
        if change.asks and change.old is not None and change.path not in args.overwrite:
            print(f"keep    {change.path} (differs from the template; pass --overwrite {change.path} to replace it)")
            print(diff(change), end="")
            continue
        print(f"{'create' if change.old is None else 'update'}  {change.path}")
        if args.dry_run and change.old is not None:
            print(diff(change), end="")
        if not args.dry_run:
            write(root / change.path, change.new)
    for note in notes:
        print(note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
