"""Check every skill and agent in this repo. Exit 1 on any error.

Run from anywhere: python3 tools/validate.py
"""

import pathlib
import re
import shutil
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIRST_PARTY = ROOT / "skills"
VENDOR = ROOT / "vendor" / "skills"
AGENTS = ROOT / "agents"

PSTACK = {
    "architect", "arena", "automate-me", "benchmark-checklist", "blast-radius", "bro", "correct",
    "create-formal-verification-skill", "create-verification-skill", "figure-it-out", "how",
    "in-your-own-words", "interrogate", "ketchup", "maintain-formal-verification-skill",
    "maintain-verification-skill", "no-comments", "poteto-help", "poteto-mode", "recall", "reflect",
    "setup-pstack", "sharpen", "show-me-your-work", "swarm", "tdd", "teach", "technical-writing",
    "typescript-best-practices", "unslop", "why", "poteto-agent", "comment-sicko",
}
PSTACK |= {
    f"principle-{p}" for p in (
        "attack-the-premise", "boundary-discipline", "build-the-lever", "encode-lessons-in-structure",
        "exhaust-the-design-space", "experience-first", "explain-the-number", "fix-root-causes",
        "foundational-thinking", "guard-the-context-window", "laziness-protocol",
        "make-operations-idempotent", "migrate-callers-then-delete-legacy-apis", "minimize-reader-load",
        "model-the-domain", "never-block-on-the-human", "outcome-oriented-execution", "prove-it-works",
        "redesign-from-first-principles", "separate-before-serializing-shared-state",
        "sequence-verifiable-units", "subtract-before-you-add", "test-behavior-not-implementation",
        "type-system-discipline",
    )
}
HARNESS_COMMANDS = {"agents", "clear", "compact", "context", "effort", "loop", "model", "plugin", "rewind", "skills"}

STACK_WORDS = re.compile(r"\bbunx?\b|vitest|\bbiome\b|\bpnpm\b|npm run|tanstack|drizzle|\bzod\b", re.I)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
SLASH = re.compile(r"(?:^|[\s`(\"'])/([a-z][a-z0-9-]{2,}(?::[a-z0-9-]+)?)(?![\w/.-])")
PSTACK_REF = re.compile(r"\bpstack:([a-z0-9-]+)")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

errors: list[str] = []
warnings: list[str] = []


def rel(p: pathlib.Path) -> str:
    return str(p.relative_to(ROOT))


def frontmatter_scalars(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    out: dict[str, str] = {}
    lines = text[4:end].split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
        i += 1
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value in (">", ">-", "|", "|-", ">+", "|+"):
            block = []
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            value = " ".join(b for b in block if b)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key] = value
    return out


def skill_dirs() -> dict[str, pathlib.Path]:
    found: dict[str, pathlib.Path] = {}
    for base in (FIRST_PARTY, VENDOR):
        for d in sorted(p for p in base.glob("*") if p.is_dir()):
            skill = d / "SKILL.md"
            if not skill.is_file():
                errors.append(f"{rel(d)}: directory has no SKILL.md")
                continue
            if d.name in found:
                errors.append(f"{rel(d)}: name {d.name!r} also used by {rel(found[d.name])}")
            found[d.name] = d
    return found


def check_frontmatter(skills: dict[str, pathlib.Path]) -> None:
    for name, d in skills.items():
        fm = frontmatter_scalars((d / "SKILL.md").read_text(encoding="utf-8"))
        where = rel(d / "SKILL.md")
        if fm is None:
            errors.append(f"{where}: missing frontmatter")
            continue
        if fm.get("name") != name:
            errors.append(f"{where}: name {fm.get('name')!r} does not match directory {name!r}")
        if not NAME_RE.match(name):
            errors.append(f"{where}: name must be lowercase letters, digits and hyphens, at most 64 chars")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{where}: missing description")
        elif len(desc) > 1024:
            errors.append(f"{where}: description is {len(desc)} chars, limit 1024")


def text_files(base: pathlib.Path):
    for p in sorted(base.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".toml", ".json", ".mjs", ".js", ".py", ".sh", ".txt", ".yaml", ".yml"):
            yield p


def authored_docs():
    yield from (p for p in text_files(FIRST_PARTY) if p.suffix == ".md")
    yield from sorted((AGENTS / "roles").glob("*.md"))
    yield from (ROOT / n for n in ("README.md", "AGENTS.md", "THIRD_PARTY_NOTICES.md") if (ROOT / n).exists())


def check_links_and_refs(skills: dict[str, pathlib.Path], agent_names: set[str]) -> None:
    known = set(skills) | agent_names | HARNESS_COMMANDS
    for p in authored_docs():
        text = p.read_text(encoding="utf-8")
        for target in LINK.findall(FENCE.sub("", text)):
            if re.match(r"^(https?:|mailto:|#|<)", target) or "<" in target:
                continue
            path = target.split("#", 1)[0]
            if path and not (p.parent / path).exists():
                errors.append(f"{rel(p)}: dead link {target}")
        for ref in SLASH.findall(text):
            base = ref.split(":", 1)
            if len(base) == 2:
                if base[0] != "pstack" or base[1] not in PSTACK:
                    errors.append(f"{rel(p)}: unknown command /{ref}")
            elif ref not in known:
                errors.append(f"{rel(p)}: unknown command /{ref}")
        for ref in PSTACK_REF.findall(text):
            if ref not in PSTACK:
                errors.append(f"{rel(p)}: unknown pstack skill pstack:{ref}")


PROFILE_FILE = re.compile(r"(?:(?<![\w-])(?:docs/agents/)?(ticket-standard|pr-standard|issue-tracker|domain)\.md|\bAGENTS\.md\b)")
HEADING_REF = re.compile(r"`(##\s[^`]+)`")


def template_headings() -> dict[str, set[str]] | None:
    template = FIRST_PARTY / "flow-setup" / "template"
    if not template.exists():
        return None
    heads: dict[str, set[str]] = {}
    for p in template.rglob("*.md"):
        text = FENCE.sub("", p.read_text(encoding="utf-8"))
        found = {line.strip() for line in text.splitlines() if line.startswith("## ")}
        key = "AGENTS" if p.name == "agents-block.md" else p.stem
        if key.startswith("issue-tracker-"):
            key = "issue-tracker"
        heads[key] = heads.get(key, set()) | found
    return heads


def nearest_file(files: list[tuple[int, int, str]], match: re.Match) -> str:
    def gap(f: tuple[int, int, str]) -> int:
        start, end, _ = f
        return match.start() - end if end <= match.start() else start - match.end()
    return min(files, key=gap)[2]


def check_profile_refs() -> None:
    heads = template_headings()
    if heads is None:
        return
    for p in text_files(FIRST_PARTY):
        if p.suffix != ".md" or p.is_relative_to(FIRST_PARTY / "flow-setup" / "template"):
            continue
        text = p.read_text(encoding="utf-8")
        for para in re.finditer(r"(?:[^\n]+\n?)+", text):
            files = [(f.start(), f.end(), "AGENTS" if f.group(1) is None else f.group(1)) for f in PROFILE_FILE.finditer(para.group(0))]
            if not files:
                continue
            for m in HEADING_REF.finditer(para.group(0)):
                owner = nearest_file(files, m)
                ref = m.group(1).strip()
                if ref not in heads.get(owner, set()):
                    line = text.count("\n", 0, para.start() + m.start()) + 1
                    errors.append(f"{rel(p)}:{line}: `{ref}` is not a heading of {owner} in the flow-setup template")


def leak_patterns() -> list[tuple[re.Pattern, str]]:
    path = ROOT / "tools" / "leak-patterns.local"
    if not path.exists():
        warnings.append("tools/leak-patterns.local is missing, so the company-data scan did not run")
        return []
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        label, _, pattern = line.partition("\t")
        if pattern:
            patterns.append((re.compile(pattern), label))
    return patterns


def check_leaks() -> None:
    patterns = leak_patterns()
    scanned = [p for base in (FIRST_PARTY, AGENTS) if base.exists() for p in text_files(base)]
    scanned += [ROOT / n for n in ("README.md", "AGENTS.md", "install.sh") if (ROOT / n).exists()]
    for p in scanned:
        text = p.read_text(encoding="utf-8", errors="replace")
        for pattern, label in patterns:
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{rel(p)}:{line}: {label} leak {m.group(0)!r}")
        top = p.relative_to(FIRST_PARTY).parts[0] if p.is_relative_to(FIRST_PARTY) else ""
        if p.suffix == ".md" and "—" in text:
            line = text.count("\n", 0, text.index("—")) + 1
            msg = f"{rel(p)}:{line}: em dash; use a period or a comma (pstack:unslop rule 13)"
            authored = top.startswith("flow-") or p.is_relative_to(AGENTS / "roles") or p.parent == ROOT
            (errors if authored else warnings).append(msg)
        if top.startswith("flow-") and top != "flow-setup":
            for m in STACK_WORDS.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{rel(p)}:{line}: stack-specific word {m.group(0)!r}; read commands from AGENTS.md instead")


def check_agents() -> set[str]:
    names: set[str] = set()
    claude = {p.stem: p for p in (AGENTS / "claude").glob("*.md")} if AGENTS.exists() else {}
    codex = {p.stem: p for p in (AGENTS / "codex").glob("*.toml")} if AGENTS.exists() else {}
    for stem, p in claude.items():
        fm = frontmatter_scalars(p.read_text(encoding="utf-8"))
        if not fm or fm.get("name") != stem or not fm.get("description"):
            errors.append(f"{rel(p)}: needs frontmatter with name {stem!r} and a description")
        names.add(stem)
    for stem, p in codex.items():
        try:
            data = tomllib.loads(p.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            errors.append(f"{rel(p)}: invalid TOML: {e}")
            continue
        if data.get("name") != stem or not data.get("description") or not str(data.get("developer_instructions", "")).strip():
            errors.append(f"{rel(p)}: needs name {stem!r}, description and developer_instructions")
        if stem not in claude:
            errors.append(f"{rel(p)}: no matching agents/claude/{stem}.md")
        names.add(stem)
    for stem in claude:
        if stem.startswith("flow-") and stem not in codex:
            errors.append(f"agents/claude/{stem}.md: flow role has no agents/codex/{stem}.toml")
    return names


def check_script_tests() -> None:
    tests = sorted(str(p.relative_to(ROOT)) for p in FIRST_PARTY.glob("*/scripts/tests/*.test.mjs"))
    if not tests:
        return
    if shutil.which("node") is None:
        warnings.append("node is not on PATH, so the skill script tests did not run")
        return
    r = subprocess.run(["node", "--test", *tests], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        errors.append(f"node --test failed for skill scripts:\n{(r.stdout + r.stderr).strip()[-2000:]}")


def check_generated() -> None:
    for script in ("build_agents.py", "readme_catalog.py"):
        path = ROOT / "tools" / script
        if path.exists():
            r = subprocess.run([sys.executable, str(path), "--check"], capture_output=True, text=True)
            if r.returncode != 0:
                errors.append(f"tools/{script} --check failed: {(r.stdout + r.stderr).strip()}")


def main() -> int:
    skills = skill_dirs()
    check_frontmatter(skills)
    agent_names = check_agents()
    check_generated()
    check_script_tests()
    check_links_and_refs(skills, agent_names)
    check_profile_refs()
    check_leaks()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(skills)} skills, {len(agent_names)} agents, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
