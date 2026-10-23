"""Check every skill and agent in this repo. Exit 1 on any error.

Run from anywhere: python3 tools/validate.py
"""

import pathlib
import re
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIRST_PARTY = ROOT / "skills"
VENDOR = ROOT / "vendor" / "skills"
AGENTS = ROOT / "agents"

PSTACK = {
    "architect", "arena", "automate-me", "babysit", "benchmark-checklist", "blast-radius", "bro",
    "correct", "create-formal-verification-skill", "create-verification-skill", "deslop",
    "figure-it-out", "fix-ci", "fix-merge-conflicts", "get-pr-comments", "how", "in-your-own-words",
    "interrogate", "ketchup", "maintain-formal-verification-skill", "maintain-verification-skill",
    "make-bot-ui", "make-pr-easy-to-review", "no-comments", "poteto-help", "poteto-mode", "recall",
    "reflect", "setup-pstack", "sharpen", "show-me-your-work", "swarm", "tdd", "teach",
    "technical-writing", "typescript-best-practices", "unslop", "what-did-i-get-done", "why",
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
SLASH = re.compile(r"(?:^|[\s`(\"'])/([a-z][a-z0-9-]{2,}(?::[a-z0-9-]+)?)(?![\w/.-])")
PSTACK_REF = re.compile(r"\bpstack:([a-z0-9-]+)")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

errors: list[str] = []
warnings: list[str] = []


def rel(p: pathlib.Path) -> str:
    return str(p.relative_to(ROOT))


def frontmatter(text: str) -> dict[str, str] | None:
    """Top-level scalar keys of a YAML frontmatter block. Nested maps and lists are skipped."""
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
        fm = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
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


def check_links_and_refs(skills: dict[str, pathlib.Path], agent_names: set[str]) -> None:
    known = set(skills) | agent_names | HARNESS_COMMANDS
    for p in text_files(FIRST_PARTY):
        if p.suffix != ".md":
            continue
        text = p.read_text(encoding="utf-8")
        for target in LINK.findall(text):
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
        if top.startswith("flow-") and top != "flow-setup":
            for m in STACK_WORDS.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{rel(p)}:{line}: stack-specific word {m.group(0)!r}; read commands from AGENTS.md instead")


def check_agents() -> set[str]:
    names: set[str] = set()
    claude = {p.stem: p for p in (AGENTS / "claude").glob("*.md")} if AGENTS.exists() else {}
    codex = {p.stem: p for p in (AGENTS / "codex").glob("*.toml")} if AGENTS.exists() else {}
    for stem, p in claude.items():
        fm = frontmatter(p.read_text(encoding="utf-8"))
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
    builder = ROOT / "tools" / "build_agents.py"
    if builder.exists():
        r = subprocess.run([sys.executable, str(builder), "--check"], capture_output=True, text=True)
        if r.returncode != 0:
            errors.append(f"tools/build_agents.py --check failed: {(r.stdout + r.stderr).strip()}")
    return names


def main() -> int:
    skills = skill_dirs()
    check_frontmatter(skills)
    agent_names = check_agents()
    check_links_and_refs(skills, agent_names)
    check_leaks()
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(skills)} skills, {len(agent_names)} agents, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
