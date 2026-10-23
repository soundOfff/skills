"""Check the flow repository profile or this machine's kit install.

usage:
  python3 doctor.py repo [path]   check the profile of the git repository that holds path (default: cwd)
  python3 doctor.py machine       check kit links, flow agents, pstack, and duplicate skills

Every check prints one PASS, FAIL, or WARN line with its evidence. Indented lines
under a check say how to fix it. Exit status is 1 when any check fails.

CLAUDE_DIR, CODEX_DIR, and AGENTS_DIR override ~/.claude, ~/.codex, and the
skills CLI folder. AGENTS_DIR defaults to a .agents folder next to CLAUDE_DIR,
so a sandboxed CLAUDE_DIR never reads the real ~/.agents.

Runs on Python 3.9, the version macOS ships.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
GATES = ("install", "dev", "format", "lint", "typecheck", "test", "test-file", "e2e", "build", "design", "health")
FULL_GATE = ("lint", "typecheck", "test", "build")
SOURCES = ("Domain language", "Decisions", "Conventions", "Design system", "Structure")
FORGES = ("github", "gitlab", "none")
TRACKERS = {"github": "GitHub", "gitlab": "GitLab", "linear": "Linear", "local": "Local"}
PUBLISH_MODES = ("draft", "ready")
MERGE_STRATEGIES = ("squash", "rebase", "merge")
READY_LABEL = "ready-for-agent"
SETTINGS = {
    "Base branch": (),
    "Publish mode": PUBLISH_MODES,
    "Merge strategy": MERGE_STRATEGIES,
    "Forge": FORGES,
    "Tracker": tuple(TRACKERS),
    "Pull request template": (),
    "Closing reference": (),
    "Ready label": (),
}
BLOCK_BEGIN = re.compile(r"<!-- flow:begin(?: v=([0-9a-f]+))? -->")
BLOCK_END = "<!-- flow:end -->"
BLOCK_HEADINGS = ("## Settings", "## Commands", "## Sources of truth", "## Delivery workflow", "## Golden rules")
BLOCK_COPY = re.compile(r"<!-- flow:(?:begin|end)\b|^\| Setting \| Value \|", re.M)
OPERATIONS = ("create", "read", "list", "comment", "label", "close", "set parent", "add dependency", "assign", "set status")
DOCS = {
    "issue-tracker.md": ("## Authorization gate", "## Operations", "## Claiming work"),
    "ticket-standard.md": ("## Template", "## Hierarchy", "## Sizing", "## Feature parent", "## Hygiene", "## Definition of Ready"),
    "pr-standard.md": ("## Scope and size", "## Body", "## Lifecycle", "## Ready-for-review checklist"),
    "domain.md": (),
}
LEGACY_DOCS = {"triage-labels.md": "the Ready label setting replaced it"}
PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")
CLAUDE_IMPORT = re.compile(r"(?m)(?:^|\s)@(?:\./)?AGENTS\.md(?:\s|$)")
TRACKER_TITLE = re.compile(r"^# Issue tracker: (GitHub|GitLab|Linear|Local)\s*$")
ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PACKAGE_MANAGERS = ("npm", "pnpm", "yarn", "bun")
MAKEFILES = ("GNUmakefile", "makefile", "Makefile")
MAKE_RULE = re.compile(r"^([^\s:#=][^:#=]*?)\s*::?(?![:=])")
MAKE_INCLUDE = re.compile(r"^-?s?include\s", re.M)
JUST_RECIPE = re.compile(r"^@?([A-Za-z_][\w-]*)(?:[ \t][^:\n]*)?:(?!=)", re.M)
JUST_ALIAS = re.compile(r"^alias[ \t]+([A-Za-z_][\w-]*)[ \t]*:=", re.M)
JUST_IMPORT = re.compile(r"^(?:import|mod)\??\s", re.M)
RANK = {"PASS": 0, "WARN": 1, "FAIL": 2}


class Check(NamedTuple):
    status: str
    name: str
    evidence: str
    fixes: tuple[str, ...] = ()


def template_files() -> list[Path]:
    return sorted(TEMPLATE.rglob("*.md"), key=lambda p: p.relative_to(TEMPLATE).as_posix())


def template_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8").replace("\r\n", "\n")


@lru_cache(maxsize=None)
def template_version() -> str:
    digest = hashlib.sha256()
    for path in template_files():
        digest.update(path.relative_to(TEMPLATE).as_posix().encode() + b"\0" + template_text(path).encode() + b"\0")
    return digest.hexdigest()[:12]


@lru_cache(maxsize=None)
def kit_keys() -> frozenset[str]:
    return frozenset(key for path in template_files() for key in PLACEHOLDER.findall(template_text(path)))


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True)


def git_root(path: Path) -> tuple[Path | None, str]:
    try:
        probe = git(path, "rev-parse", "--show-toplevel")
    except OSError as error:
        return None, f"git did not run: {error}"
    if probe.returncode != 0:
        return None, probe.stderr.strip() or "git rev-parse failed"
    return Path(probe.stdout.strip()).resolve(), ""


def valid_branch(name: str) -> bool:
    if not name or name.startswith("-"):
        return False
    return subprocess.run(["git", "check-ref-format", "--branch", name], capture_output=True).returncode == 0


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8", errors="replace")


def sections(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.rstrip()
            out[current] = ""
        elif current is not None:
            out[current] += line + "\n"
    return out


def first_table(body: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    lines: list[str] = []
    for line in body.splitlines():
        if line.strip().startswith("|"):
            lines.append(line.strip())
        elif lines:
            break
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0].strip("`")] = cells[1]
    return rows


def unquoted(cell: str) -> str:
    return cell.strip().strip("`").strip()


def backticked(cell: str) -> list[str]:
    found = re.findall(r"`([^`]+)`", cell)
    return found or [p.strip() for p in cell.split(",") if p.strip()]


def worst(statuses) -> str:
    return max(statuses, key=RANK.__getitem__, default="PASS")


def placeholders(name: str, text: str) -> list[Check]:
    left = sorted({key for key in PLACEHOLDER.findall(text) if key in kit_keys()})
    if not left:
        return []
    return [Check("FAIL", name, f"unfilled placeholders {', '.join('{{' + key + '}}' for key in left)}", ("re-run /flow-setup",))]


def linked(path: Path, root: Path) -> str:
    if not path.is_symlink():
        return ""
    target = Path(os.path.realpath(path))
    return f"; {path.name} links to {target.relative_to(root).as_posix() if target.is_relative_to(root) else target}"


def check_block(root: Path) -> tuple[list[Check], str | None]:
    path = root / "AGENTS.md"
    if not path.is_file():
        return [Check("FAIL", "AGENTS.md", "missing", ("run /flow-setup in this repository",))], None
    text = read_text(path)
    begins, ends = list(BLOCK_BEGIN.finditer(text)), text.count(BLOCK_END)
    if len(begins) != 1 or ends != 1 or begins[0].start() > text.index(BLOCK_END):
        return [Check("FAIL", "AGENTS.md flow block", f"{len(begins)} begin and {ends} end markers; need exactly one of each, begin first")], None
    start = begins[0].start()
    block = text[start : text.index(BLOCK_END) + len(BLOCK_END)]
    headings = tuple(line.rstrip() for line in block.splitlines() if line.startswith("## "))
    first = text.count("\n", 0, start) + 1
    span = f"lines {first}-{first + block.count(chr(10))}{linked(path, root)}"
    if headings == BLOCK_HEADINGS:
        results = [Check("PASS", "AGENTS.md flow block", f"{span}; {len(BLOCK_HEADINGS)} headings in order")]
    else:
        found = ", ".join(headings) or "none"
        results = [Check("FAIL", "AGENTS.md flow block", f"{span}; headings are {found}, need {', '.join(BLOCK_HEADINGS)} in that order", ("re-run /flow-setup",))]
    return results + placeholders("AGENTS.md flow block", block) + [check_version(begins[0].group(1))], block


def check_version(found: str | None) -> Check:
    current = template_version()
    if found == current:
        return Check("PASS", "flow block version", f"v={current} matches the kit templates")
    marker = f"v={found}" if found else "no version"
    return Check("WARN", "flow block version", f"begin marker has {marker}; the kit templates are v={current}", ("re-run /flow-setup",))


def setting_problem(name: str, value: str | None) -> str | None:
    allowed = SETTINGS[name]
    if value is None:
        return f"no {name} row"
    if not value:
        return f"{name} is empty"
    if allowed and value not in allowed:
        return f"{name} {value!r} is not one of {', '.join(allowed)}"
    if name == "Base branch" and not valid_branch(value):
        return f"Base branch {value!r} is not a valid branch name"
    return None


def check_settings(block: str, root: Path) -> tuple[list[Check], dict[str, str]]:
    rows = {name: unquoted(cell) for name, cell in first_table(sections(block).get("## Settings", "")).items()}
    problems = {name: setting_problem(name, rows.get(name)) for name in SETTINGS}
    valid = {name: rows[name] for name, problem in problems.items() if problem is None}
    if len(valid) < len(SETTINGS):
        results = [Check("FAIL", "settings", "; ".join(p for p in problems.values() if p), ("re-run /flow-setup",))]
    else:
        results = [Check("PASS", "settings", "; ".join(f"{name} {value}" for name, value in valid.items()))]
    extra = [name for name in rows if name not in SETTINGS]
    if extra:
        results.append(Check("WARN", "settings", f"rows outside the contract: {', '.join(extra)}"))
    if "Base branch" in valid:
        results.append(check_base(root, valid["Base branch"]))
    if "Pull request template" in valid:
        results.append(check_pr_template(root, valid["Pull request template"]))
    return results, valid


def check_base(root: Path, base: str) -> Check:
    for ref in (f"refs/heads/{base}", f"refs/remotes/origin/{base}"):
        if git(root, "rev-parse", "--verify", "--quiet", ref).returncode == 0:
            return Check("PASS", "base branch", f"{base} resolves to {ref}")
    return Check("WARN", "base branch", f"{base} has no local or origin ref yet")


def check_pr_template(root: Path, value: str) -> Check:
    if value.lower() == "none":
        return Check("PASS", "pull request template", "none")
    if (root / value).is_file():
        return Check("PASS", "pull request template", f"{value} exists")
    return Check("FAIL", "pull request template", f"{value} does not exist", (f"restore {value}, or re-run /flow-setup to write or detect the template",))


def command_words(command: str) -> list[str]:
    try:
        words = shlex.split(command)
    except ValueError:
        words = command.split()
    while words and ENV_ASSIGNMENT.match(words[0]):
        words.pop(0)
    return words


def resolve(word: str, root: Path) -> str | None:
    if "/" in word:
        path = Path(word) if word.startswith("/") else root / word
        return str(path) if path.exists() else None
    return shutil.which(word) or (str(root / word) if (root / word).is_file() else None)


def package_script(root: Path, name: str) -> tuple[str, str]:
    try:
        scripts = json.loads(read_text(root / "package.json")).get("scripts")
    except (OSError, ValueError, AttributeError):
        return "FAIL", "no readable package.json at the repository root"
    if isinstance(scripts, dict) and name in scripts:
        return "PASS", f"package.json declares {name}"
    return "FAIL", f"package.json declares no script {name}"


def make_target(root: Path, name: str) -> tuple[str, str]:
    present = set(os.listdir(root))
    found = next((n for n in MAKEFILES if n in present), None)
    if found is None:
        return "FAIL", "no Makefile at the repository root"
    text = read_text(root / found)
    targets = set()
    for line in text.splitlines():
        rule = MAKE_RULE.match(line)
        if rule:
            targets.update(rule.group(1).split())
    if name in targets:
        return "PASS", f"{found} declares {name}"
    if MAKE_INCLUDE.search(text) or any("%" in t for t in targets):
        return "WARN", f"{found} declares no target {name}; an include or a pattern rule may provide it"
    return "FAIL", f"{found} declares no target {name}"


def just_recipe(root: Path, name: str) -> tuple[str, str]:
    found = next((n for n in sorted(os.listdir(root)) if n.lower() in ("justfile", ".justfile")), None)
    if found is None:
        return "FAIL", "no justfile at the repository root"
    text = read_text(root / found)
    if name in set(JUST_RECIPE.findall(text)) | set(JUST_ALIAS.findall(text)):
        return "PASS", f"{found} declares {name}"
    if JUST_IMPORT.search(text):
        return "WARN", f"{found} declares no recipe {name}; an import or a module may provide it"
    return "FAIL", f"{found} declares no recipe {name}"


def declaration(words: list[str], root: Path) -> tuple[str, str] | None:
    runner = words[0]
    if runner in PACKAGE_MANAGERS and len(words) > 2 and words[1] == "run" and not words[2].startswith("-"):
        return package_script(root, words[2])
    if runner in ("make", "just") and len(words) > 1 and not words[1].startswith("-") and "=" not in words[1]:
        return (make_target if runner == "make" else just_recipe)(root, words[1])
    return None


def check_gate(gate: str, command: str, root: Path) -> Check:
    words = command_words(command)
    if not words:
        return Check("FAIL", f"gate {gate}", "empty command")
    where = resolve(words[0], root)
    findings = [("PASS", f"{words[0]} at {where}") if where else ("FAIL", f"{words[0]} is not on PATH or a repository file")]
    declared = declaration(words, root)
    if declared:
        findings.append(declared)
    return Check(worst(s for s, _ in findings), f"gate {gate}", f"`{command}`: {'; '.join(text for _, text in findings)}")


def check_commands(block: str, root: Path) -> list[Check]:
    rows = {gate: unquoted(cell) for gate, cell in first_table(sections(block).get("## Commands", "")).items()}
    unused = {gate for gate, command in rows.items() if command.lower() == "n/a"}
    missing = [g for g in GATES if g not in rows]
    extra = [g for g in rows if g not in GATES]
    if missing:
        results = [Check("FAIL", "commands table", f"missing gates: {', '.join(missing)}")]
    else:
        full = [g for g in FULL_GATE if g not in unused]
        results = [Check("PASS" if full else "WARN", "commands table", f"{len(GATES)} gates; full gate runs {', '.join(full) or 'nothing'}")]
    if extra:
        results.append(Check("WARN", "commands table", f"gates outside the contract: {', '.join(extra)}"))
    return results + [check_gate(gate, rows[gate], root) for gate in GATES if gate in rows and gate not in unused]


def check_sources(block: str, root: Path) -> list[Check]:
    rows = first_table(sections(block).get("## Sources of truth", ""))
    missing = [s for s in SOURCES if s not in rows]
    results = [Check("FAIL", "sources table", f"missing rows: {', '.join(missing)}")] if missing else [
        Check("PASS", "sources table", f"{len(SOURCES)} rows")
    ]
    for concern in SOURCES:
        if concern not in rows:
            continue
        cell = rows[concern]
        if unquoted(cell).lower() == "none":
            results.append(Check("PASS", f"source {concern}", "none"))
            continue
        paths = backticked(cell)
        absent = [p for p in paths if not p.startswith(("http://", "https://")) and not (root / p).exists()]
        if absent or not paths:
            results.append(Check("FAIL", f"source {concern}", f"missing paths: {', '.join(absent) or 'empty cell'}"))
        else:
            results.append(Check("PASS", f"source {concern}", ", ".join(paths)))
    return results


def check_docs(root: Path, tracker: str | None) -> list[Check]:
    results = []
    for name, headings in DOCS.items():
        label = f"docs/agents/{name}"
        path = root / "docs" / "agents" / name
        if not path.is_file():
            results.append(Check("FAIL", label, "missing", ("run /flow-setup in this repository",)))
            continue
        text = read_text(path)
        lines = [line.rstrip() for line in text.splitlines()]
        problems = [f"no {h}" for h in headings if h not in lines]
        fixes: tuple[str, ...] = ()
        if name == "issue-tracker.md":
            title = TRACKER_TITLE.match(lines[0]) if lines else None
            if not title:
                problems.append("first line is not '# Issue tracker: <GitHub | GitLab | Linear | Local>'")
            elif tracker in TRACKERS and title.group(1) != TRACKERS[tracker]:
                problems.append(f"the title says {title.group(1)}, but the Tracker setting is {tracker}")
                fixes = (f"re-run /flow-setup and pass --overwrite {label}, or correct the Tracker setting",)
            ops = sections(text).get("## Operations", "").lower()
            problems += [f"Operations lacks {op}" for op in OPERATIONS if not re.search(rf"\b{op}\b", ops)]
        results.append(Check("FAIL", label, "; ".join(problems), fixes) if problems else Check("PASS", label, "present with required sections"))
        results += placeholders(label, text)
    for name, reason in LEGACY_DOCS.items():
        if (root / "docs" / "agents" / name).exists():
            results.append(Check("WARN", f"docs/agents/{name}", f"left from an older profile; {reason}", (f"delete docs/agents/{name}",)))
    return results


def check_ignore(root: Path) -> Check:
    probe = git(root, "check-ignore", "-v", ".flow/")
    if probe.returncode == 0:
        return Check("PASS", ".flow/ ignored", probe.stdout.strip().replace("\t", " "))
    return Check("FAIL", ".flow/ ignored", "git check-ignore does not ignore .flow/", ("append .flow/ to .gitignore",))


def check_claude(root: Path) -> Check:
    path = root / "CLAUDE.md"
    if path.is_symlink() and not path.exists():
        return Check("FAIL", "CLAUDE.md", f"links to {os.readlink(path)}, which does not exist", ("point CLAUDE.md at AGENTS.md, or replace it with a file containing @AGENTS.md",))
    if not path.exists():
        return Check("WARN", "CLAUDE.md", "missing, so Claude Code does not load AGENTS.md", ("create CLAUDE.md containing @AGENTS.md",))
    if os.path.realpath(path) == os.path.realpath(root / "AGENTS.md"):
        how = "links to AGENTS.md" if path.is_symlink() else "is the file AGENTS.md links to"
        return Check("PASS", "CLAUDE.md", f"{how}, so Claude Code reads the flow block")
    text = read_text(path)
    if BLOCK_COPY.search(text):
        return Check(
            "FAIL",
            "CLAUDE.md",
            "repeats the flow block, so it drifts from AGENTS.md",
            ("replace the copy with the line @AGENTS.md, or make CLAUDE.md a link to AGENTS.md",),
        )
    if CLAUDE_IMPORT.search(text):
        return Check("PASS", "CLAUDE.md", "imports @AGENTS.md")
    return Check("FAIL", "CLAUDE.md", "exists without an @AGENTS.md import", ("add a line @AGENTS.md to CLAUDE.md",))


def repo_checks(path: Path) -> list[Check]:
    root, problem = git_root(path)
    if root is None:
        return [Check("FAIL", "git repository", f"{path} is not inside a git repository: {problem}")]
    results = [Check("PASS", "git repository", str(root))]
    block_results, block = check_block(root)
    results += block_results
    settings: dict[str, str] = {}
    if block is not None:
        settings_results, settings = check_settings(block, root)
        results += settings_results + check_commands(block, root) + check_sources(block, root)
    results += check_docs(root, settings.get("Tracker"))
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
