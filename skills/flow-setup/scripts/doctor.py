"""Check the flow repository profile or this machine's kit install.

usage:
  python3 doctor.py repo [path]   check the profile of the git repository at path (default: cwd)
  python3 doctor.py machine       check kit links, flow agents, pstack, and duplicate skills

Every check prints one PASS, FAIL, or WARN line with its evidence. Indented lines
under a check say how to fix it. Exit status is 1 when any check fails.

CLAUDE_DIR, CODEX_DIR, and AGENTS_DIR override ~/.claude, ~/.codex, and the
skills CLI folder. AGENTS_DIR defaults to a .agents folder next to CLAUDE_DIR,
so a sandboxed CLAUDE_DIR never reads the real ~/.agents.
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

GATES = ("install", "dev", "format", "lint", "typecheck", "test", "test-file", "e2e", "build", "design", "health")
FULL_GATE = ("lint", "typecheck", "test", "build")
SOURCES = ("Domain language", "Decisions", "Conventions", "Design system", "Structure")
BLOCK_BEGIN = "<!-- flow:begin -->"
BLOCK_END = "<!-- flow:end -->"
BLOCK_HEADINGS = ("## Commands", "## Sources of truth", "## Delivery workflow", "## Golden rules")
TRACKERS = {"github": "GitHub", "gitlab": "GitLab", "linear": "Linear", "local": "Local"}
FORGES = ("github", "gitlab", "none")
OPERATIONS = ("create", "read", "list", "comment", "label", "close", "set parent", "add dependency", "assign", "set status")
TRIAGE_ROLES = ("needs-triage", "needs-info", "ready-for-agent", "ready-for-human", "wontfix")
PUBLISH_MODES = ("draft", "ready")
MERGE_STRATEGIES = ("squash", "rebase", "merge")
DOCS = {
    "issue-tracker.md": ("## Authorization gate", "## Operations", "## Claiming work"),
    "ticket-standard.md": ("## Template", "## Hierarchy", "## Sizing", "## Feature parent", "## Hygiene", "## Definition of Ready"),
    "pr-standard.md": ("## Scope and size", "## Body", "## Lifecycle", "## Ready-for-review checklist"),
    "domain.md": (),
    "triage-labels.md": (),
}
PLACEHOLDER = re.compile(r"\{\{[^{}]*\}\}")
CLAUDE_IMPORT = re.compile(r"(?m)(?:^|\s)@AGENTS\.md(?:\s|$)")
TRACKER_TITLE = re.compile(r"^# Issue tracker: (GitHub|GitLab|Linear|Local)\s*$")


class Check(NamedTuple):
    status: str
    name: str
    evidence: str
    fixes: tuple[str, ...] = ()


def sections(text: str) -> dict[str, str]:
    """Body text under each level-two heading, keyed by the heading line."""
    out: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.rstrip()
            out[current] = ""
        elif current is not None:
            out[current] += line + "\n"
    return out


def table(body: str) -> dict[str, str]:
    """First column to second column for each data row of the first Markdown table."""
    rows: dict[str, str] = {}
    lines = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0].strip("`")] = cells[1]
    return rows


def backticked(cell: str) -> list[str]:
    found = re.findall(r"`([^`]+)`", cell)
    return found or [p.strip() for p in cell.split(",") if p.strip()]


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def first_word(command: str) -> str:
    try:
        words = shlex.split(command.strip("`"))
    except ValueError:
        words = command.strip("`").split()
    words = [w for w in words if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", w)]
    return words[0] if words else ""


def resolve(word: str, root: Path) -> str | None:
    if "/" in word:
        path = Path(word) if word.startswith("/") else root / word
        return str(path) if path.exists() else None
    return shutil.which(word) or (str(root / word) if (root / word).is_file() else None)


def placeholders(name: str, text: str) -> list[Check]:
    left = sorted(set(PLACEHOLDER.findall(text)))
    return [Check("FAIL", name, f"unfilled placeholders {', '.join(left)}")] if left else []


def check_block(root: Path) -> tuple[list[Check], str | None]:
    path = root / "AGENTS.md"
    if not path.is_file():
        return [Check("FAIL", "AGENTS.md", "missing", ("run /flow-setup in this repository",))], None
    text = path.read_text(encoding="utf-8")
    begins, ends = text.count(BLOCK_BEGIN), text.count(BLOCK_END)
    if begins != 1 or ends != 1 or text.index(BLOCK_BEGIN) > text.index(BLOCK_END):
        return [Check("FAIL", "AGENTS.md flow block", f"{begins} begin and {ends} end markers; need exactly one of each, begin first")], None
    start = text.index(BLOCK_BEGIN)
    block = text[start : text.index(BLOCK_END) + len(BLOCK_END)]
    lines = [line.rstrip() for line in block.splitlines()]
    wrong = [f"{h} x{lines.count(h)}" for h in BLOCK_HEADINGS if lines.count(h) != 1]
    first = text.count("\n", 0, start) + 1
    span = f"lines {first}-{first + block.count(chr(10))}"
    results = [Check("FAIL", "AGENTS.md flow block", f"{span}; headings not exactly once: {', '.join(wrong)}")] if wrong else [
        Check("PASS", "AGENTS.md flow block", f"{span}, {len(BLOCK_HEADINGS)} headings once each")
    ]
    return results + placeholders("AGENTS.md flow block", block), block


def check_commands(block: str, root: Path) -> list[Check]:
    rows = table(sections(block).get("## Commands", ""))
    missing = [g for g in GATES if g not in rows]
    extra = [g for g in rows if g not in GATES]
    if missing:
        results = [Check("FAIL", "commands table", f"missing gates: {', '.join(missing)}")]
    else:
        full = [g for g in FULL_GATE if rows[g] != "n/a"]
        status = "PASS" if full else "WARN"
        results = [Check(status, "commands table", f"{len(GATES)} gates; full gate runs {', '.join(full) or 'nothing'}")]
    if extra:
        results.append(Check("WARN", "commands table", f"gates outside the contract: {', '.join(extra)}"))
    for gate in GATES:
        command = rows.get(gate, "")
        if gate not in rows or command == "n/a":
            continue
        word = first_word(command)
        where = resolve(word, root) if word else None
        if where:
            results.append(Check("PASS", f"gate {gate}", f"{command} ({word} at {where})"))
        else:
            results.append(Check("FAIL", f"gate {gate}", f"{command or 'empty'}: {word or 'no command'} is not on PATH or a repository file"))
    return results


def check_sources(block: str, root: Path) -> list[Check]:
    rows = table(sections(block).get("## Sources of truth", ""))
    missing = [s for s in SOURCES if s not in rows]
    results = [Check("FAIL", "sources table", f"missing rows: {', '.join(missing)}")] if missing else [
        Check("PASS", "sources table", f"{len(SOURCES)} rows")
    ]
    for concern in SOURCES:
        if concern not in rows:
            continue
        cell = rows[concern]
        if cell.strip("`") == "none":
            results.append(Check("PASS", f"source {concern}", "none"))
            continue
        paths = backticked(cell)
        absent = [p for p in paths if not p.startswith(("http://", "https://")) and not (root / p).exists()]
        if absent or not paths:
            results.append(Check("FAIL", f"source {concern}", f"missing paths: {', '.join(absent) or 'empty cell'}"))
        else:
            results.append(Check("PASS", f"source {concern}", ", ".join(paths)))
    return results


def lifecycle_checks(root: Path, text: str) -> list[str]:
    problems = []
    rows = table(sections(text).get("## Lifecycle", ""))
    base = rows.get("Base branch", "").strip("`")
    mode = rows.get("Publish mode", "").strip("`")
    merge = rows.get("Merge strategy", "").strip("`")
    if not base:
        problems.append("Lifecycle has no Base branch row")
    if mode not in PUBLISH_MODES:
        problems.append(f"Publish mode {mode or 'missing'} is not draft or ready")
    if merge not in MERGE_STRATEGIES:
        problems.append(f"Merge strategy {merge or 'missing'} is not squash, rebase, or merge")
    for path in re.findall(r"`([^`\s]+\.md)`", sections(text).get("## Body", "")):
        if not (root / path).is_file():
            problems.append(f"Body names template {path}, which does not exist")
    return problems


def check_docs(root: Path) -> list[Check]:
    results = []
    for name, headings in DOCS.items():
        label = f"docs/agents/{name}"
        path = root / "docs" / "agents" / name
        if not path.is_file():
            results.append(Check("FAIL", label, "missing", ("run /flow-setup in this repository",)))
            continue
        text = path.read_text(encoding="utf-8")
        lines = [line.rstrip() for line in text.splitlines()]
        problems = [f"no {h}" for h in headings if h not in lines]
        if name == "issue-tracker.md":
            if not lines or not TRACKER_TITLE.match(lines[0]):
                problems.append("first line is not '# Issue tracker: <GitHub | GitLab | Linear | Local>'")
            ops = sections(text).get("## Operations", "").lower()
            problems += [f"Operations lacks {op}" for op in OPERATIONS if not re.search(rf"\b{op}\b", ops)]
        if name == "pr-standard.md":
            problems += lifecycle_checks(root, text)
        if name == "triage-labels.md":
            rows = table(text)
            problems += [f"no row for {role}" for role in TRIAGE_ROLES if role not in rows]
        results += [Check("FAIL", label, "; ".join(problems))] if problems else [Check("PASS", label, "present with required sections")]
        results += placeholders(label, text)
    return results


def check_base(root: Path) -> list[Check]:
    path = root / "docs" / "agents" / "pr-standard.md"
    if not path.is_file():
        return []
    base = table(sections(path.read_text(encoding="utf-8")).get("## Lifecycle", "")).get("Base branch", "").strip("`")
    if not base:
        return []
    for ref in (f"refs/heads/{base}", f"refs/remotes/origin/{base}"):
        if git(root, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return [Check("PASS", "base branch", f"{base} resolves to {ref}")]
    return [Check("WARN", "base branch", f"{base} has no local or origin ref yet")]


def check_ignore(root: Path) -> Check:
    probe = git(root, "check-ignore", "-v", ".flow/")
    if probe.returncode == 0:
        return Check("PASS", ".flow/ ignored", probe.stdout.strip().replace("\t", " "))
    return Check("FAIL", ".flow/ ignored", "git check-ignore does not ignore .flow/", ("append .flow/ to .gitignore",))


def check_claude(root: Path) -> Check:
    path = root / "CLAUDE.md"
    if not path.is_file():
        return Check("WARN", "CLAUDE.md", "missing, so Claude Code does not load AGENTS.md", ("create CLAUDE.md containing @AGENTS.md",))
    if CLAUDE_IMPORT.search(path.read_text(encoding="utf-8")):
        return Check("PASS", "CLAUDE.md", "imports @AGENTS.md")
    return Check("FAIL", "CLAUDE.md", "exists without an @AGENTS.md import", ("add a line @AGENTS.md to CLAUDE.md",))


def repo_checks(path: Path) -> list[Check]:
    top = git(path, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        return [Check("FAIL", "git repository", f"{path} is not inside a git repository")]
    root = Path(top.stdout.strip())
    results = [Check("PASS", "git repository", str(root))]
    block_results, block = check_block(root)
    results += block_results
    if block is not None:
        results += check_commands(block, root) + check_sources(block, root)
    results += check_docs(root) + check_base(root)
    results += [check_ignore(root), check_claude(root)]
    return results


def home_dir(env: str, default: Path) -> Path:
    return Path(os.environ[env]).expanduser() if os.environ.get(env) else default


def check_links(label: str, dest: Path, sources: dict[str, Path], kit: Path) -> Check:
    fix = (f"cd {kit} && ./install.sh --dry-run && ./install.sh",)
    missing, wrong = [], []
    for name, src in sorted(sources.items()):
        entry = dest / name
        if not entry.is_symlink() and not entry.exists():
            missing.append(name)
        elif not entry.is_symlink() or entry.resolve() != src.resolve():
            wrong.append(name)
    stale = []
    if dest.is_dir():
        for entry in sorted(dest.iterdir()):
            if entry.is_symlink() and entry.name not in sources:
                target = Path(os.readlink(entry))
                target = target if target.is_absolute() else entry.parent / target
                if not entry.exists() or kit in target.resolve().parents:
                    stale.append(entry.name)
    if missing or wrong:
        parts = [f"{len(sources) - len(missing) - len(wrong)}/{len(sources)} linked into {dest}"]
        if missing:
            parts.append(f"missing {short(missing)}")
        if wrong:
            parts.append(f"not linked to the kit {short(wrong)}")
        return Check("FAIL", label, "; ".join(parts), fix)
    if stale:
        return Check("WARN", label, f"{len(sources)}/{len(sources)} linked; stale links {short(stale)}", fix)
    return Check("PASS", label, f"{len(sources)}/{len(sources)} linked into {dest}")


def short(names: list[str], limit: int = 6) -> str:
    more = f" and {len(names) - limit} more" if len(names) > limit else ""
    return ", ".join(names[:limit]) + more


def check_claude_pstack(claude: Path) -> Check:
    fixes = ("in Claude Code: /plugin marketplace add cursor/plugins", "then: /plugin install pstack@cursor-plugins")
    path = claude / "plugins" / "installed_plugins.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return Check("FAIL", "Claude Code pstack", f"cannot read {path}: {error.__class__.__name__}", fixes)
    plugins = data.get("plugins", data) if isinstance(data, dict) else {}
    entry = plugins.get("pstack@cursor-plugins") if isinstance(plugins, dict) else None
    if entry is None:
        return Check("FAIL", "Claude Code pstack", f"pstack@cursor-plugins not in {path}", fixes)
    installs = entry if isinstance(entry, list) else [entry]
    versions = sorted({str(i.get("version")) for i in installs if isinstance(i, dict) and i.get("version")})
    return Check("PASS", "Claude Code pstack", f"pstack@cursor-plugins {', '.join(versions) or 'installed'}")


def check_codex_pstack(codex: Path) -> Check:
    fixes = ("in a terminal: codex plugin marketplace add michael-denyer/pstack-claude", "then: codex plugin add pstack@pstack-claude")
    config = codex / "config.toml"
    text = config.read_text(encoding="utf-8") if config.is_file() else ""
    cache = codex / "plugins" / "cache" / "pstack-claude"
    skill = next(iter(sorted(cache.glob("**/poteto-mode/SKILL.md"))), None) if cache.is_dir() else None
    problems = []
    if "pstack-claude" not in text:
        problems.append(f"no pstack-claude marketplace in {config}")
    if skill is None:
        problems.append(f"no poteto-mode under {cache}")
    if problems:
        return Check("FAIL", "Codex pstack", "; ".join(problems), fixes)
    return Check("PASS", "Codex pstack", f"pstack-claude marketplace configured; {skill}")


def check_model_rule(label: str, path: Path, harness: str) -> Check:
    if path.is_file():
        return Check("PASS", label, str(path))
    command = "$setup-pstack" if harness == "Codex" else "/pstack:setup-pstack"
    return Check("WARN", label, f"{path} missing, so pstack uses its default models", (f"in {harness}: {command}",))


def check_duplicates(agents: Path, skills: dict[str, Path], kit: Path) -> Check:
    folder = agents / "skills"
    present = sorted(e.name for e in folder.iterdir()) if folder.is_dir() else []
    both = [name for name in present if name in skills]
    if not both:
        return Check("PASS", "~/.agents/skills duplicates", f"none in {folder}")
    return Check(
        "WARN",
        "~/.agents/skills duplicates",
        f"Codex also reads {folder}, so it sees two copies of {short(both)}",
        (f"npx skills remove -g {' '.join(both)}", f"then relink the kit: cd {kit} && ./install.sh"),
    )


def machine_checks() -> list[Check]:
    kit = Path(__file__).resolve().parents[3]
    if not (kit / "install.sh").is_file() or not (kit / "skills").is_dir():
        return [Check("FAIL", "kit root", f"{kit} has no install.sh and skills folder; run the doctor from the kit's skills/flow-setup")]
    claude = home_dir("CLAUDE_DIR", Path.home() / ".claude")
    codex = home_dir("CODEX_DIR", Path.home() / ".codex")
    agents = home_dir("AGENTS_DIR", claude.parent / ".agents")
    skills = {
        d.name: d
        for base in (kit / "skills", kit / "vendor" / "skills")
        if base.is_dir()
        for d in sorted(base.iterdir())
        if (d / "SKILL.md").is_file()
    }
    claude_agents = {p.name: p for p in sorted((kit / "agents" / "claude").glob("*.md"))}
    codex_agents = {p.name: p for p in sorted((kit / "agents" / "codex").glob("*.toml"))}
    flow = sorted(p.stem for p in (kit / "agents" / "roles").glob("flow-*.md"))
    return [
        Check("PASS", "kit root", f"{kit}; {len(skills)} skills, flow agents {', '.join(flow)}"),
        check_links("Claude Code skills", claude / "skills", skills, kit),
        check_links("Codex skills", codex / "skills", skills, kit),
        check_links("Claude Code agents", claude / "agents", claude_agents, kit),
        check_links("Codex agents", codex / "agents", codex_agents, kit),
        check_claude_pstack(claude),
        check_codex_pstack(codex),
        check_model_rule("Claude Code model rules", claude / "rules" / "pstack-models.md", "Claude Code"),
        check_model_rule("Codex model rules", codex / "pstack-models.md", "Codex"),
        check_duplicates(agents, skills, kit),
    ]


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] not in ("repo", "machine") or (argv[1] == "machine" and len(argv) > 2) or len(argv) > 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    results = repo_checks(Path(argv[2] if len(argv) == 3 else ".").resolve()) if argv[1] == "repo" else machine_checks()
    for check in results:
        print(f"{check.status} {check.name}: {check.evidence}")
        for fix in check.fixes:
            print(f"     fix: {fix}")
    failed = sum(c.status == "FAIL" for c in results)
    warned = sum(c.status == "WARN" for c in results)
    print(f"{len(results)} checks, {failed} failed, {warned} warnings")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
