"""Rewrite the skill catalog in README.md from each skill's frontmatter.

python3 tools/readme_catalog.py          rewrite the block between the catalog markers
python3 tools/readme_catalog.py --check  exit 1 when the block is stale
"""

import json
import pathlib
import re
import sys

from validate import frontmatter

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN, END = "<!-- catalog:begin -->", "<!-- catalog:end -->"
FLOW_ORDER = [
    "flow-setup", "flow-mode", "flow-help", "flow-create", "flow-to-issues", "flow-build", "flow-to-pr",
    "flow-code-check", "flow-code-review", "flow-code-quality-review", "flow-design-check",
    "flow-adv-review", "flow-subagent",
]


def summary(desc: str) -> str:
    first = re.split(r"(?<=[.!?])\s", desc.strip(), maxsplit=1)[0]
    return first.replace("|", "\\|")


def rows(paths: list[pathlib.Path], source: dict[str, str] | None = None) -> list[str]:
    out = []
    for d in paths:
        fm = frontmatter((d / "SKILL.md").read_text(encoding="utf-8")) or {}
        how = "you type it" if fm.get("disable-model-invocation") == "true" else "you or the agent"
        cells = [f"`{d.name}`", summary(fm.get("description", "")), how]
        if source is not None:
            cells.append(source.get(d.name, "unknown"))
        out.append("| " + " | ".join(cells) + " |")
    return out


def render() -> str:
    first_party = [p for p in sorted((ROOT / "skills").iterdir()) if (p / "SKILL.md").is_file()]
    flow = sorted(
        (p for p in first_party if p.name.startswith("flow-")),
        key=lambda p: (FLOW_ORDER.index(p.name) if p.name in FLOW_ORDER else len(FLOW_ORDER), p.name),
    )
    own = [p for p in first_party if not p.name.startswith("flow-")]
    vendor = [p for p in sorted((ROOT / "vendor" / "skills").iterdir()) if (p / "SKILL.md").is_file()]
    lock = json.loads((ROOT / "vendor" / "skills.lock.json").read_text())["skills"]
    upstream = {name: f"[{e['source']}](https://github.com/{e['source']})" for name, e in lock.items()}
    head = ["| Skill | What it does | Invoked by |", "| --- | --- | --- |"]
    lines = [BEGIN, "", "### Delivery workflow", "", *head, *rows(flow), ""]
    lines += ["### Everyday skills", "", *head, *rows(own), ""]
    lines += ["### Vendored", "", "| Skill | What it does | Invoked by | Upstream |",
              "| --- | --- | --- | --- |", *rows(vendor, upstream), "", END]
    return "\n".join(lines)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"README.md has no {BEGIN} ... {END} block")
        return 1
    start, end = text.index(BEGIN), text.index(END) + len(END)
    updated = text[:start] + render() + text[end:]
    if updated == text:
        return 0
    if "--check" in sys.argv:
        print("README catalog is stale, run python3 tools/readme_catalog.py")
        return 1
    README.write_text(updated, encoding="utf-8")
    print("rewrote the README catalog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
