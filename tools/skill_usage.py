"""Count how often each skill in this repo was invoked across Claude Code, Codex and Cursor history.

python3 tools/skill_usage.py         only skills that live in this repo
python3 tools/skill_usage.py --all   every slash command and skill seen
"""

import collections, datetime as dt, glob, json, os, pathlib, re, sys, tomllib

HOME = os.path.expanduser("~")
NOW = dt.datetime.now(dt.timezone.utc)
SLASH = re.compile(r"^\s*/([a-z][a-z0-9:_-]{1,60})\b")
CMD_TAG = re.compile(r"<command-name>/?([a-z][a-z0-9:_-]{1,60})</command-name>")
DOLLAR = re.compile(r"(?<![\w$])\$([a-z][a-z0-9-]{2,60})\b")
SKILL_PATH = re.compile(r"/skills/([a-z0-9][a-z0-9_-]+)/SKILL\.md", re.I)

events = []


def add(harness, kind, name, when, project):
    events.append((harness, kind, name.lower(), when, project))


def parse_ts(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v / 1000 if v > 1e12 else v, dt.timezone.utc)
    try:
        return dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None


def texts(content):
    if isinstance(content, str):
        yield content
    elif isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and isinstance(b.get("text"), str):
                yield b["text"]


def scan_user_text(harness, text, when, project):
    m = SLASH.match(text)
    if m:
        add(harness, "slash", m.group(1), when, project)
    for m in CMD_TAG.finditer(text):
        add(harness, "slash", m.group(1), when, project)
    if harness == "codex":
        for m in DOLLAR.finditer(text):
            add(harness, "dollar", m.group(1), when, project)


def claude():
    for line in open(f"{HOME}/.claude/history.jsonl", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = SLASH.match(d.get("display", ""))
        if m:
            add("claude-history", "slash", m.group(1), parse_ts(d.get("timestamp")), d.get("project", ""))
    for f in glob.glob(f"{HOME}/.claude/projects/*/*.jsonl"):
        project = os.path.basename(os.path.dirname(f))
        for line in open(f, errors="replace"):
            if '"Skill"' not in line and "command-name" not in line and "SKILL.md" not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            when = parse_ts(d.get("timestamp"))
            msg = d.get("message") or {}
            if d.get("type") == "user":
                for t in texts(msg.get("content")):
                    for m in CMD_TAG.finditer(t):
                        add("claude", "slash", m.group(1), when, project)
            elif d.get("type") == "assistant":
                for b in msg.get("content") or []:
                    if not isinstance(b, dict) or b.get("type") != "tool_use":
                        continue
                    inp = b.get("input") or {}
                    if b.get("name") == "Skill" and inp.get("skill"):
                        add("claude", "skill-tool", inp["skill"], when, project)
                    elif b.get("name") == "Read":
                        m = SKILL_PATH.search(str(inp.get("file_path", "")))
                        if m:
                            add("claude", "skill-read", m.group(1), when, project)


def codex():
    for f in glob.glob(f"{HOME}/.codex/sessions/**/*.jsonl", recursive=True) + glob.glob(
        f"{HOME}/.codex/archived_sessions/**/*.jsonl", recursive=True
    ):
        project = None
        for line in open(f, errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            p = d.get("payload") if isinstance(d.get("payload"), dict) else {}
            if d.get("type") == "session_meta":
                project = p.get("cwd")
            when = parse_ts(d.get("timestamp"))
            if d.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "user":
                for t in texts(p.get("content")):
                    if t.startswith("<environment_context>") or t.startswith("# AGENTS.md"):
                        continue
                    scan_user_text("codex", t, when, project)
            elif d.get("type") == "response_item" and p.get("type") in ("function_call", "custom_tool_call"):
                for m in SKILL_PATH.finditer(str(p.get("arguments", "")) + str(p.get("input", ""))):
                    add("codex", "skill-read", m.group(1), when, project)


def cursor():
    for f in glob.glob(f"{HOME}/.cursor/projects/*/agent-transcripts/**/*.jsonl", recursive=True):
        project = f.split("/projects/")[1].split("/")[0]
        when = dt.datetime.fromtimestamp(os.path.getmtime(f), dt.timezone.utc)
        for line in open(f, errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get("message") or {}
            if d.get("role") == "user":
                for t in texts(msg.get("content")):
                    t = re.sub(r"^<user_query>\s*", "", t)
                    scan_user_text("cursor", t, when, project)
            else:
                for b in msg.get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        for m in SKILL_PATH.finditer(json.dumps(b.get("input"))):
                            add("cursor", "skill-read", m.group(1), when, project)


claude()
codex()
cursor()

repo = pathlib.Path(__file__).resolve().parent.parent
known = None if "--all" in sys.argv else (
    {d.parent.name for d in repo.glob("skills/*/SKILL.md")}
    | {s["name"] for s in tomllib.loads((repo / "agents.toml").read_text(encoding="utf-8")).get("skills", [])}
)
table = collections.defaultdict(lambda: collections.Counter())
projects = collections.defaultdict(collections.Counter)
for harness, kind, name, when, project in events:
    base = name.split(":")[-1]
    if known is not None and base not in known and name not in known:
        continue
    age = (NOW - when).days if when else 9999
    bucket = "30d" if age <= 30 else "90d" if age <= 90 else "older"
    table[base][f"{harness}:{bucket}"] += 1
    table[base]["total"] += 1
    if age <= 90:
        table[base]["recent90"] += 1
    projects[base][str(project)[-40:]] += 1

rows = sorted(table.items(), key=lambda kv: (-kv[1]["recent90"], -kv[1]["total"]))
out = []
for name, c in rows:
    by = ", ".join(f"{k}={v}" for k, v in sorted(c.items()) if k not in ("total", "recent90"))
    top = ", ".join(f"{p}({n})" for p, n in projects[name].most_common(3))
    out.append(f"{c['recent90']:5d} {c['total']:6d}  {name:40s} {by}  | {top}")
print("recent90 total  skill  breakdown | top projects")
print("\n".join(out))
