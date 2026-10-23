"""Render each agents/roles/<name>.md into a Claude Code agent and a Codex agent.

python3 tools/build_agents.py          write agents/claude/<name>.md and agents/codex/<name>.toml
python3 tools/build_agents.py --check  exit 1 when a rendered file is missing or stale
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROLES = ROOT / "agents" / "roles"
REQUIRED = ("name", "description", "claude-tools", "claude-model", "codex-model", "codex-effort")
INCLUDE = re.compile(r"^\{\{include:([^}]+)\}\}$", re.M)


def parse(path: pathlib.Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n\n?(.*)$", text, re.S)
    if not m:
        sys.exit(f"{path}: missing frontmatter")
    meta = dict(line.split(": ", 1) for line in m.group(1).splitlines() if line.strip())
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        sys.exit(f"{path}: missing {', '.join(missing)}")
    if meta["name"] != path.stem:
        sys.exit(f"{path}: name {meta['name']!r} must match the file name")
    body = INCLUDE.sub(lambda i: (ROOT / i.group(1)).read_text(encoding="utf-8").rstrip(), m.group(2)).rstrip() + "\n"
    if "'''" in body:
        sys.exit(f"{path}: body cannot contain ''' because it is written as a TOML literal string")
    return meta, body


def render(meta: dict[str, str], body: str) -> dict[pathlib.Path, str]:
    name = meta["name"]
    claude = (
        "---\n"
        f"name: {name}\n"
        f"description: {json.dumps(meta['description'], ensure_ascii=False)}\n"
        f"tools: {meta['claude-tools']}\n"
        f"model: {meta['claude-model']}\n"
        "---\n\n"
        f"{body}"
    )
    codex = (
        f"name = {json.dumps(name)}\n"
        f"description = {json.dumps(meta['description'], ensure_ascii=False)}\n"
        f"model = {json.dumps(meta['codex-model'])}\n"
        f"model_reasoning_effort = {json.dumps(meta['codex-effort'])}\n"
        + ('sandbox_mode = "read-only"\n' if meta.get("read-only") == "true" else "")
        + f"developer_instructions = '''\n{body}'''\n"
    )
    return {
        ROOT / "agents" / "claude" / f"{name}.md": claude,
        ROOT / "agents" / "codex" / f"{name}.toml": codex,
    }


def orphans(names: set[str]) -> list[pathlib.Path]:
    generated = list((ROOT / "agents" / "codex").glob("*.toml"))
    generated += list((ROOT / "agents" / "claude").glob("flow-*.md"))
    return [p for p in generated if p.stem not in names]


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    roles = sorted(ROLES.glob("*.md"))
    for path in orphans({r.stem for r in roles}):
        if check:
            stale.append(f"{path.relative_to(ROOT)} (no role in agents/roles/)")
        else:
            path.unlink()
            print(f"removed {path.relative_to(ROOT)}, which has no role")
    for role in roles:
        for path, content in render(*parse(role)).items():
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current == content:
                continue
            if check:
                stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print("stale, run python3 tools/build_agents.py: " + ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
