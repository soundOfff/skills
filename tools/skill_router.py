"""Ask Jev which skill the agent should load first, as a Claude Code UserPromptSubmit hook.

The router chooses from the skill listing Claude Code showed the model, read from the session
transcript. It never rebuilds the catalog from skill folders, so it offers exactly the skills the
agent can load and none it cannot.

    export OPENROUTER_API_KEY=sk-or-...      # or TYPESAFE_API_KEY, in the shell that starts Claude Code
    python3 tools/skill_router.py ask "the build is throwing after the deploy"
    python3 tools/skill_router.py install [--dry-run] [--under PATH ...]
    python3 tools/skill_router.py score [--replay N]
    python3 tools/skill_router.py install --remove

`ask` makes one live call, prints everything it saw and got back, and logs nothing. `install` adds
the hook entry to $CLAUDE_DIR/settings.json. With `--under`, the hook only routes prompts whose
working directory is inside one of the given folders. `score` joins the decision log to the skills
the agent loaded. `score --replay N` asks Jev about the newest N past prompts instead, which gives a
baseline before any log exists.

Claude Code runs the hook verb on every prompt, with the event JSON on stdin:

    /opt/homebrew/bin/python3 /path/to/kit/tools/skill_router.py hook [--under PATH ...] || true

TYPESAFE_API_KEY asks api.typesafe.ai with jev-latest and wins when both keys are set.
OPENROUTER_API_KEY asks OpenRouter with typesafe/jev-1.14. No key means the hook does nothing.
CLAUDE_DIR overrides ~/.claude. No other variable is read.

The hook verb always exits 0 and prints nothing unless it advises. The `|| true` keeps a moved kit
or a missing interpreter from exiting 2, which would block the prompt. One session in
HOLDOUT_EVERY is a holdout. Jev is asked and logged there, but the hook stays quiet, so `score` can
compare the agent with and without advice. Every routed prompt leaves one line in
$CLAUDE_DIR/skill-router/decisions.jsonl.

Python 3.11+, stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, Literal, NewType, get_args

SPEAK_AT: Final = 0.5  # Jev confidence the hook needs before it speaks. Tune from `score`.
JEV_TIMEOUT_S: Final = 2.0  # one deadline for DNS, connect and read
HOOK_TIMEOUT_S: Final = 5  # Claude Code kills the hook here, so JEV_TIMEOUT_S fires first
HOLDOUT_EVERY: Final = 5  # one session in five stays quiet. 0 ends the holdout.
MAX_REQUEST_BYTES: Final = 30_000  # Jev switches to a slower, less accurate long-context mode near 32,000
PROMPT_BYTES: Final = 3_000
MIN_PROMPT_CHARS: Final = 12  # "yes", "go on" and "do it" never reach Jev
MAX_OPTIONS: Final = 255  # Jev's Choice limit, NO_SKILL included
SIBLINGS_TRIED: Final = 5
SIBLING_HEAD_LINES: Final = 400  # the initial listing sat within the first 60 lines of every local transcript
LOG_PROMPT_CHARS: Final = 160
TOP_N: Final = 5
LOG_VERSION: Final = 1

NO_SKILL: Final = "no skill"  # the space keeps it apart from every skill name
INSTRUCTIONS: Final = (
    "A coding agent is about to act on the user's prompt. Which of its skills, if any, should it "
    "load first? Each option is a skill name with the description the agent itself reads. Choose "
    f"`{NO_SKILL}` for short replies, follow-ups to earlier work, questions answered from knowledge, "
    "and ordinary coding that no description covers. Pick a skill only when the prompt asks for "
    "what its description says it is for."
)
NO_SKILL_DESCRIPTION: Final = "Load no skill. Answer the prompt directly with ordinary tools."

PROVIDERS: Final = (
    # (key variable, name, url, model). Order is precedence.
    ("TYPESAFE_API_KEY", "typesafe", "https://api.typesafe.ai/v1/systemone", "jev-latest"),
    ("OPENROUTER_API_KEY", "openrouter", "https://openrouter.ai/api/v1/systemone", "typesafe/jev-1.14"),
)
KEY_VARIABLES: Final = " or ".join(variable for variable, *_ in PROVIDERS)

SCRIPT: Final = Path(__file__).resolve()
MARKER: Final = "/tools/skill_router.py"  # identifies our settings entry wherever the kit lives
HOOK_EVENT: Final = "UserPromptSubmit"
SLASH_COMMAND: Final = re.compile(r"(?:^|[\s`(\"'])/[a-z][a-z0-9-]{2,}(?::[a-z0-9-]+)?(?![\w/.-])")
COMMAND_NAME: Final = re.compile(r"<command-name>/?([^<\s]+)</command-name>")

SkillName = NewType("SkillName", str)
Arm = Literal["live", "holdout"]
CatalogSource = Literal["own", "sibling"]
FailureKind = Literal["no_listing", "timeout", "network", "http", "bad_response", "crash"]


@dataclass(frozen=True)
class Skill:
    name: SkillName
    description: str  # as the model read it, whitespace collapsed


@dataclass(frozen=True)
class Catalog:
    """The skills the model could load when the listing was written.

    Invariants, enforced by `_listing_entries` and `_catalog`: names unique, none equal to
    NO_SKILL, every description non-empty, at most MAX_OPTIONS - 1 entries, listing order kept.
    """

    skills: tuple[Skill, ...]
    source: Path  # the transcript the listing came from


@dataclass(frozen=True)
class SessionView:
    listing: Catalog | None  # None on a session's first prompt, before Claude Code writes it
    in_context: frozenset[SkillName]  # loaded with the Skill tool or run as a slash command


@dataclass(frozen=True)
class Turn:
    """One user prompt in a transcript and the skills the agent loaded before the next one."""

    session_id: str
    prompt: str
    prompt_sha: str
    at: str
    in_context: frozenset[SkillName]  # skills in context when the prompt arrived
    loaded: tuple[SkillName, ...]  # Skill tool loads by the main agent during this turn


@dataclass(frozen=True)
class PromptEvent:
    session_id: str
    transcript: Path
    cwd: Path
    prompt: str


@dataclass(frozen=True)
class Provider:
    name: str  # logged with every decision
    url: str
    model: str  # what we ask for. Ranking.model records what answered.
    key: str = field(repr=False)

    @classmethod
    def from_env(cls, env: Mapping[str, str]) -> Provider | None:
        for variable, name, url, model in PROVIDERS:
            if key := env.get(variable, "").strip():
                return cls(name, url, model, key)
        return None


@dataclass(frozen=True)
class Config:
    """Everything a routing pass depends on besides its event. Tests build one directly with a
    Provider that points at a local fake, so production reads no test-only variable."""

    provider: Provider | None
    claude_dir: Path
    http_timeout_s: float = JEV_TIMEOUT_S
    speak_at: float = SPEAK_AT
    holdout_every: int = HOLDOUT_EVERY
    under: tuple[Path, ...] = ()  # empty means every working directory

    @classmethod
    def from_env(cls, env: Mapping[str, str], under: Sequence[Path] = ()) -> Config:
        claude_dir = Path(env.get("CLAUDE_DIR") or Path.home() / ".claude").expanduser()
        return cls(Provider.from_env(env), claude_dir, under=tuple(under))

    @property
    def log_path(self) -> Path:
        return self.claude_dir / "skill-router" / "decisions.jsonl"

    @property
    def projects_dir(self) -> Path:
        return self.claude_dir / "projects"

    @property
    def settings_path(self) -> Path:
        return self.claude_dir / "settings.json"


@dataclass(frozen=True)
class Request:
    body: bytes  # at most MAX_REQUEST_BYTES unless the names alone overflow it
    options: frozenset[str]  # catalog names plus NO_SKILL
    capped_at: int | None  # description length cap in characters, None when everything fit uncut
    capped: int  # how many descriptions the cap shortened


@dataclass(frozen=True)
class Ranking:
    choice: SkillName | None  # None when Jev picked NO_SKILL
    confidence: float
    top: tuple[tuple[str, float], ...]  # highest probabilities first, NO_SKILL included
    model: str  # the model that answered, so a silent upgrade shows in the log
    ms: int
    input_tokens: int | None
    cost: float | None  # USD, OpenRouter only


@dataclass(frozen=True)
class Failure:
    kind: FailureKind
    detail: str
    ms: int = 0


@dataclass(frozen=True)
class Advice:
    skill: SkillName
    confidence: float

    def line(self) -> str:
        """No description and no runners-up. The description is already in the model's context,
        and runners-up invite the deliberation this layer exists to cut."""
        return (
            f"Skill router: the `{self.skill}` skill fits this request (Jev confidence {self.confidence:.2f}). "
            "If that matches what the user asked for, load it with the Skill tool before you start. "
            "Otherwise ignore this note."
        )


class Silence(StrEnum):
    NO_SKILL = "no_skill"
    LOW_CONFIDENCE = "low_confidence"
    ALREADY_LOADED = "already_loaded"


@dataclass(frozen=True)
class Judged:
    ranking: Ranking
    verdict: Advice | Silence  # what the policy says, before the arm decides whether to speak


@dataclass(frozen=True)
class Decision:
    """One line of the decision log. Hook output never reaches the transcript, so this line is
    the only record of what the router said."""

    at: str
    session_id: str
    transcript: Path
    prompt_sha: str
    prompt_head: str
    arm: Arm
    catalog: CatalogSource | None  # None when no listing was found
    provider: str
    options: int
    capped_at: int | None
    result: Judged | Failure

    @property
    def spoken(self) -> Advice | None:
        if self.arm == "live" and isinstance(self.result, Judged) and isinstance(self.result.verdict, Advice):
            return self.result.verdict
        return None

    def to_json(self) -> str:
        row: dict[str, object] = {
            "v": LOG_VERSION, "at": self.at, "session": self.session_id, "transcript": str(self.transcript),
            "prompt_sha": self.prompt_sha, "prompt": self.prompt_head, "arm": self.arm, "catalog": self.catalog,
            "provider": self.provider, "options": self.options, "capped_at": self.capped_at,
            "spoke": self.spoken is not None,
        }
        if isinstance(self.result, Failure):
            row |= {"verdict": "failed", "error": self.result.kind, "detail": self.result.detail, "ms": self.result.ms}
        else:
            ranking, verdict = self.result.ranking, self.result.verdict
            row |= {
                "verdict": "advise" if isinstance(verdict, Advice) else verdict.value,
                "choice": ranking.choice, "confidence": round(ranking.confidence, 4),
                "top": [[name, round(p, 4)] for name, p in ranking.top], "model": ranking.model,
                "ms": ranking.ms, "input_tokens": ranking.input_tokens, "cost": ranking.cost,
            }
        return json.dumps(row, ensure_ascii=False)

    @staticmethod
    def from_json(line: str) -> Decision | None:
        """Boundary parser for log lines. Garbled lines and other versions return None."""
        try:
            row = json.loads(line)
            if not isinstance(row, dict) or row.get("v") != LOG_VERSION:
                return None
            arm, catalog = row["arm"], row["catalog"]
            if arm not in get_args(Arm) or catalog not in (*get_args(CatalogSource), None):
                return None
            return Decision(
                at=_typed(row, "at", str), session_id=_typed(row, "session", str),
                transcript=Path(_typed(row, "transcript", str)), prompt_sha=_typed(row, "prompt_sha", str),
                prompt_head=_typed(row, "prompt", str), arm=arm, catalog=catalog,
                provider=_typed(row, "provider", str), options=_typed(row, "options", int),
                capped_at=_typed(row, "capped_at", int, optional=True), result=_result_from_row(row),
            )
        except (KeyError, TypeError, ValueError):
            return None


@dataclass(frozen=True)
class HookChange:
    settings: Path
    command: str
    was_installed: bool
    is_installed: bool  # the state after this call, or the state a dry run would leave
    changed: bool
    written: bool  # False on a dry run and when nothing changed


class SettingsError(Exception):
    """settings.json is not a JSON object, `hooks` is not an object, or `hooks.UserPromptSubmit`
    is not a list. The installer never rewrites a file it cannot read in full."""


@dataclass(frozen=True)
class ArmScore:
    """Counts for one arm over rows joined to a turn. `named` rows had an Advice verdict."""

    prompts: int
    named: int
    followed: int  # named, and the agent loaded that skill this turn
    other: int  # named, and the agent loaded a different skill this turn
    ignored: int  # named, and the agent loaded nothing this turn
    quiet: int  # Jev chose no skill, was unsure, or named a skill already in context
    loaded_anyway: int  # quiet, and the agent loaded a skill this turn


@dataclass(frozen=True)
class Disagreement:
    at: str
    prompt: str
    jev: str | None
    confidence: float
    agent: tuple[str, ...]


@dataclass(frozen=True)
class Score:
    """live.followed / live.named against holdout.followed / holdout.named is the advice's lift.
    Holdout disagreements are where a human decides who was right."""

    rows: int
    answered: int
    unjoined: int  # answered rows whose prompt was not found in their transcript
    failures: dict[str, int]
    catalogs: dict[str, tuple[int, int]]  # catalog source -> (joined rows, agreed)
    latency_ms: tuple[int, int] | None  # p50, p95 over answered rows
    cost: float
    live: ArmScore
    holdout: ArmScore
    calibration: tuple[tuple[float, int, int], ...]  # holdout only: (bucket floor, rows, agreed)
    disagreements: tuple[Disagreement, ...]  # holdout, newest first


# Hook protocol.


def run_hook(stdin_text: str, config: Config) -> str:
    """Return what the hook prints for one UserPromptSubmit event, or "" for silence. Never raises.

    An event that does not parse, a prompt outside `config.under`, a prompt that should not be
    routed, and a missing key all stay silent and log nothing. Every other path logs one line.
    """
    event = _parse_event(stdin_text)
    provider = config.provider
    if event is None or provider is None or not _inside(event.cwd, config.under) or not _wants_routing(event.prompt):
        return ""
    arm = _arm(event.session_id, config.holdout_every)
    try:
        decision = _route(event, arm, provider, config)
    except Exception as error:  # a hook must never block the prompt it decorates
        result = Failure("crash", f"{type(error).__name__}: {error}"[:200])
        decision = _decision(event.session_id, event.transcript, event.prompt, arm, provider, result)
    _append(decision, config.log_path)
    advice = decision.spoken
    if advice is None:
        return ""
    return json.dumps({"hookSpecificOutput": {"hookEventName": HOOK_EVENT, "additionalContext": advice.line()}})


def _route(event: PromptEvent, arm: Arm, provider: Provider, config: Config) -> Decision:
    view = _session_view(event.transcript)
    catalog, source = view.listing, "own"
    if catalog is None:
        catalog, source = _recent_listing(event.transcript.parent, exclude=event.transcript), "sibling"
    if catalog is None:
        failure = Failure("no_listing", f"no skill listing in {event.transcript.parent}")
        return _decision(event.session_id, event.transcript, event.prompt, arm, provider, failure)
    request, result = _decide(event.prompt, catalog, view.in_context, provider, config)
    return _decision(event.session_id, event.transcript, event.prompt, arm, provider, result, source=source, request=request)


def _parse_event(raw: str) -> PromptEvent | None:
    try:
        data = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(data, dict):
        return None
    session_id, transcript, cwd, prompt = (data.get(k) for k in ("session_id", "transcript_path", "cwd", "prompt"))
    if not all(isinstance(v, str) and v for v in (session_id, transcript, cwd)) or not isinstance(prompt, str):
        return None
    return PromptEvent(session_id, Path(transcript).expanduser(), Path(cwd).expanduser(), prompt)


def _wants_routing(prompt: str) -> bool:
    """False for empty and short prompts, harness text that starts with `<`, and any prompt that
    runs or names a slash command. A user who names a skill already chose one."""
    text = prompt.strip()
    return not (
        len(text) < MIN_PROMPT_CHARS or text.startswith(("<", "/")) or SLASH_COMMAND.search(text)
    )


def _inside(cwd: Path, roots: Sequence[Path]) -> bool:
    if not roots:
        return True
    here = cwd.resolve()
    return any(here.is_relative_to(root.expanduser().resolve()) for root in roots)


def _arm(session_id: str, every: int) -> Arm:
    """Deterministic per session, so a session never mixes arms."""
    if every > 0 and int(hashlib.sha256(session_id.encode()).hexdigest()[:8], 16) % every == 0:
        return "holdout"
    return "live"


# Claude Code transcripts. The only code that knows the JSONL record shapes.


def _records(path: Path, needles: Sequence[bytes], max_lines: int | None = None) -> Iterator[dict]:
    """JSON records from lines that contain any needle. Lines that do not parse are skipped."""
    try:
        with path.open("rb") as lines:
            for number, line in enumerate(lines):
                if max_lines is not None and number >= max_lines:
                    return
                if not any(needle in line for needle in needles):
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                if isinstance(record, dict):
                    yield record
    except OSError:
        return


def _listing_entries(attachment: object) -> dict[SkillName, str] | None:
    """Boundary parser for one skill_listing attachment, in content order.

    `content` holds "- name: description" lines, and a description may run over several lines
    and contain colons and "- " of its own. An entry starts only at "- <name>: " for a name in
    `names`, longest names first. Names without a description are dropped.
    """
    if not isinstance(attachment, dict) or attachment.get("type") != "skill_listing":
        return None
    names, content = attachment.get("names"), attachment.get("content")
    if not isinstance(names, list) or not isinstance(content, str) or not all(isinstance(n, str) for n in names):
        return None
    known = sorted({n for n in names if n and n != NO_SKILL}, key=len, reverse=True)
    if not known:
        return {}
    anchor = re.compile(r"^- (" + "|".join(map(re.escape, known)) + r"): ", re.M)
    hits = list(anchor.finditer(content))
    entries: dict[SkillName, str] = {}
    for hit, following in zip(hits, [*hits[1:], None]):
        description = " ".join(content[hit.end() : following.start() if following else len(content)].split())
        if description:
            entries.setdefault(SkillName(hit.group(1)), description)
    return entries


def _catalog(entries: Mapping[SkillName, str], source: Path) -> Catalog:
    return Catalog(tuple(Skill(name, text) for name, text in entries.items())[: MAX_OPTIONS - 1], source)


def _session_view(transcript: Path) -> SessionView:
    """One prefiltered pass over the live transcript. An initial listing replaces the catalog, a
    later one adds or replaces entries by name."""
    entries: dict[SkillName, str] | None = None
    in_context: set[SkillName] = set()
    for record in _records(transcript, (b'"skill_listing"', b'"name":"Skill"', b"<command-name>")):
        if record.get("isSidechain"):
            continue
        kind = record.get("type")
        if kind == "attachment":
            attachment = record.get("attachment")
            listed = _listing_entries(attachment)
            if listed is None:
                continue
            if entries is None or attachment.get("isInitial"):
                entries = {}
            entries.update(listed)
        elif kind == "assistant":
            in_context.update(_skill_loads(record))
        elif kind == "user" and not record.get("isMeta"):
            in_context.update(SkillName(c) for c in COMMAND_NAME.findall(_prompt_text(record) or ""))
    return SessionView(_catalog(entries, transcript) if entries else None, frozenset(in_context))


def _recent_listing(project_dir: Path, exclude: Path | None) -> Catalog | None:
    """The initial listing of the newest other session in the same project folder. It covers a
    session's first prompt, whose own listing Claude Code writes just after the hook runs. It
    never looks in another project folder, so another repository's project skills stay out."""
    try:
        siblings = sorted(
            (p for p in project_dir.glob("*.jsonl") if p != exclude), key=lambda p: p.stat().st_mtime, reverse=True
        )
    except OSError:
        return None
    for path in siblings[:SIBLINGS_TRIED]:
        for record in _records(path, (b'"skill_listing"',), SIBLING_HEAD_LINES):
            attachment = record.get("attachment")
            if record.get("type") == "attachment" and isinstance(attachment, dict) and attachment.get("isInitial"):
                if entries := _listing_entries(attachment):
                    return _catalog(entries, path)
    return None


def _project_dir_for(cwd: Path, claude_dir: Path) -> Path:
    """A guess at the transcript folder for a working directory. Long paths get shortened by
    Claude Code, so `ask` names the folder it tried when the guess finds nothing."""
    return claude_dir / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))


def _prompt_text(record: dict) -> str | None:
    """The text of a user record, or None for a tool result."""
    message = record.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, str):
        return content
    if not isinstance(content, list) or any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
        return None
    texts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str)]
    return "\n".join(texts) if texts else None


def _skill_loads(record: dict) -> list[SkillName]:
    message = record.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, list):
        return []
    loads = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
            skill = block.get("input", {}).get("skill") if isinstance(block.get("input"), dict) else None
            if isinstance(skill, str) and skill:
                loads.append(SkillName(skill.lstrip("/")))
    return loads


def _turns(transcript: Path) -> tuple[Turn, ...]:
    """Every user prompt with the Skill loads that followed it. Assistant records carry no
    prompt id, so order is the only link between a prompt and its loads."""
    built: list[tuple[str, str, frozenset[SkillName], list[SkillName]]] = []
    in_context: set[SkillName] = set()
    for record in _records(transcript, (b'"user"', b'"assistant"')):
        if record.get("isSidechain"):
            continue
        if record.get("type") == "user" and not record.get("isMeta"):
            text = _prompt_text(record)
            if text is None:
                continue
            at = record.get("timestamp")
            built.append((text, at if isinstance(at, str) else "", frozenset(in_context), []))
            in_context.update(SkillName(c) for c in COMMAND_NAME.findall(text))
        elif record.get("type") == "assistant":
            loads = _skill_loads(record)
            in_context.update(loads)
            if built:
                built[-1][3].extend(loads)
    session_id = transcript.stem
    return tuple(Turn(session_id, text, _prompt_sha(text), at, before, tuple(loaded)) for text, at, before, loaded in built)


def _prompt_sha(prompt: str) -> str:
    """The join key between a log line and a transcript turn."""
    return hashlib.sha256(" ".join(prompt.split()).encode()).hexdigest()[:16]


# Jev. Owns the request wire format, the byte budget, HTTP and response parsing.


def _build_request(prompt: str, catalog: Catalog, model: str) -> Request:
    """One Choice over the whole catalog plus NO_SKILL. When the body is over MAX_REQUEST_BYTES,
    the largest description cap that fits is found by binary search, so only the longest
    descriptions shrink."""
    state = prompt.encode("utf-8")[:PROMPT_BYTES].decode("utf-8", "ignore")
    names = [skill.name for skill in catalog.skills]
    full = [skill.description for skill in catalog.skills]

    def encode(descriptions: Sequence[str]) -> bytes:
        criteria = {**dict(zip(names, descriptions)), NO_SKILL: NO_SKILL_DESCRIPTION}
        question = {"type": "choice", "instructions": INSTRUCTIONS, "criteria": criteria}
        body = {"model": model, "state": state, "questions": {"skill": question}}
        return json.dumps(body, ensure_ascii=False).encode("utf-8")

    options = frozenset(names) | {NO_SKILL}
    body = encode(full)
    if len(body) <= MAX_REQUEST_BYTES:
        return Request(body, options, None, 0)
    low, high = 0, max(map(len, full))
    while low < high:
        middle = (low + high + 1) // 2
        if len(encode([_cut(d, middle) for d in full])) <= MAX_REQUEST_BYTES:
            low = middle
        else:
            high = middle - 1
    return Request(encode([_cut(d, low) for d in full]), options, low, sum(len(d) > low for d in full))


def _cut(text: str, cap: int) -> str:
    if len(text) <= cap:
        return text
    head = text[:cap]
    space = head.rfind(" ")
    return head[:space] if space > 0 else head


def _ask_jev(provider: Provider, request: Request, timeout_s: float) -> Ranking | Failure:
    """POST in a daemon thread under one deadline, which bounds DNS and connect as well as read
    and leaves time to log before Claude Code kills the hook."""
    started = time.monotonic()
    box: list[Ranking | Failure] = []

    def work() -> None:
        try:
            box.append(_post(provider, request, timeout_s, started))
        except Exception as error:
            box.append(Failure("crash", type(error).__name__, _ms(started)))

    worker = threading.Thread(target=work, daemon=True)
    worker.start()
    worker.join(timeout_s)
    return box[0] if box else Failure("timeout", f"no answer within {timeout_s:g} s", _ms(started))


def _post(provider: Provider, request: Request, timeout_s: float, started: float) -> Ranking | Failure:
    # Imported here so the prompts that never reach Jev skip the network stack's import time.
    import http.client
    import urllib.error
    import urllib.request

    headers = {"Authorization": f"Bearer {provider.key}", "Content-Type": "application/json", "X-Title": "skill router"}
    http_request = urllib.request.Request(provider.url, data=request.body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(http_request, timeout=timeout_s) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        try:
            excerpt = error.read(200).decode("utf-8", "replace")
        except (OSError, http.client.HTTPException):
            excerpt = ""
        finally:
            error.close()
        return Failure("http", f"HTTP {error.code} {error.reason}: {excerpt}".strip(), _ms(started))
    except urllib.error.URLError as error:
        kind: FailureKind = "timeout" if isinstance(error.reason, TimeoutError) else "network"
        return Failure(kind, str(error.reason), _ms(started))
    except TimeoutError:
        return Failure("timeout", f"read timed out after {timeout_s:g} s", _ms(started))
    except (OSError, http.client.HTTPException) as error:
        return Failure("network", f"{type(error).__name__}: {error}", _ms(started))
    ms = _ms(started)
    try:
        payload = json.loads(raw)
    except ValueError:
        payload = None
    ranking = _parse_answer(payload, request.options, provider.model, ms)
    return ranking or Failure("bad_response", raw[:200].decode("utf-8", "replace"), ms)


def _parse_answer(payload: object, options: frozenset[str], requested: str, ms: int) -> Ranking | None:
    """Boundary parser for Jev's response. Anything off the documented shape returns None."""
    if not isinstance(payload, dict):
        return None
    answers = payload.get("answers")
    answer = answers.get("skill") if isinstance(answers, dict) else None
    if not isinstance(answer, dict) or answer.get("type") != "choice":
        return None
    choice, confidence, probabilities = answer.get("choice"), answer.get("confidence"), answer.get("probabilities")
    if not isinstance(choice, str) or choice not in options or not _number(confidence) or not 0 <= confidence <= 1:
        return None
    if not isinstance(probabilities, dict):
        return None
    ranked = []
    for option, p in probabilities.items():
        if option in options:
            if not _number(p):
                return None
            ranked.append((option, float(p)))
    ranked.sort(key=lambda pair: -pair[1])
    usage = payload.get("usage") if isinstance(payload.get("usage"), dict) else {}
    tokens, cost, model = usage.get("input_tokens"), usage.get("cost"), payload.get("model")
    return Ranking(
        choice=None if choice == NO_SKILL else SkillName(choice),
        confidence=float(confidence),
        top=tuple(ranked[:TOP_N]),
        model=model if isinstance(model, str) else requested,
        ms=ms,
        input_tokens=tokens if isinstance(tokens, int) and not isinstance(tokens, bool) else None,
        cost=float(cost) if _number(cost) else None,
    )


def _number(value: object) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and math.isfinite(value)


def _ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


# Verdict. Pure policy, shared by the hook, `ask` and `score --replay`.


def _judge(ranking: Ranking, in_context: frozenset[SkillName], speak_at: float) -> Advice | Silence:
    if ranking.choice is None:
        return Silence.NO_SKILL
    if ranking.confidence < speak_at:
        return Silence.LOW_CONFIDENCE
    if ranking.choice in in_context:
        return Silence.ALREADY_LOADED  # a reload costs the whole SKILL.md again
    return Advice(ranking.choice, ranking.confidence)


def _decide(
    prompt: str, catalog: Catalog, in_context: frozenset[SkillName], provider: Provider, config: Config
) -> tuple[Request, Judged | Failure]:
    request = _build_request(prompt, catalog, provider.model)
    answer = _ask_jev(provider, request, config.http_timeout_s)
    if isinstance(answer, Failure):
        return request, answer
    return request, Judged(answer, _judge(answer, in_context, config.speak_at))


# Decision log. One append-only file, one writer per line, read by `score`.


def _decision(
    session_id: str,
    transcript: Path,
    prompt: str,
    arm: Arm,
    provider: Provider,
    result: Judged | Failure,
    *,
    at: str | None = None,
    source: CatalogSource | None = None,
    request: Request | None = None,
) -> Decision:
    return Decision(
        at=at or datetime.now().astimezone().isoformat(timespec="seconds"),
        session_id=session_id,
        transcript=transcript,
        prompt_sha=_prompt_sha(prompt),
        prompt_head=" ".join(prompt.split())[:LOG_PROMPT_CHARS],
        arm=arm,
        catalog=source,
        provider=provider.name,
        options=len(request.options) if request else 0,
        capped_at=request.capped_at if request else None,
        result=result,
    )


def _append(decision: Decision, path: Path) -> None:
    """One O_APPEND write per line, so concurrent sessions do not interleave. A full disk must
    not block a prompt, so OSError is swallowed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        try:
            os.write(fd, (decision.to_json() + "\n").encode("utf-8"))
        finally:
            os.close(fd)
    except OSError:
        pass


def _read_log(path: Path) -> list[Decision]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return [d for d in map(Decision.from_json, lines) if d is not None]


def _typed(row: dict, key: str, kind: type, optional: bool = False) -> Any:
    value = row.get(key)
    if value is None and optional:
        return None
    if not isinstance(value, kind) or (isinstance(value, bool) and kind is not bool):
        raise ValueError(key)
    return value


def _result_from_row(row: dict) -> Judged | Failure:
    verdict = row["verdict"]
    if verdict == "failed":
        kind = row["error"]
        if kind not in get_args(FailureKind):
            raise ValueError(kind)
        return Failure(kind, _typed(row, "detail", str), _typed(row, "ms", int))
    choice = _typed(row, "choice", str, optional=True)
    confidence = row["confidence"]
    if not _number(confidence):
        raise ValueError("confidence")
    cost = row.get("cost")
    ranking = Ranking(
        choice=SkillName(choice) if choice else None,
        confidence=float(confidence),
        top=tuple((str(name), float(p)) for name, p in _typed(row, "top", list)),
        model=_typed(row, "model", str),
        ms=_typed(row, "ms", int),
        input_tokens=_typed(row, "input_tokens", int, optional=True),
        cost=float(cost) if _number(cost) else None,
    )
    if verdict == "advise":
        if ranking.choice is None:
            raise ValueError("advice without a choice")
        return Judged(ranking, Advice(ranking.choice, ranking.confidence))
    return Judged(ranking, Silence(verdict))


# Scoring. Agreement between Jev and the agent, from the log or from a replay.


def score(config: Config) -> Score:
    """Join every log line to the turn it routed, by prompt hash and order, and count."""
    return _score(_read_log(config.log_path))


def replay(limit: int, config: Config) -> Score:
    """Ask Jev about the newest `limit` past prompts and score the answers. Nothing is logged.

    Each prompt uses its own session's listing and the skills in context before it. The agent
    handled those prompts with no router, so the decisions count as holdout.
    """
    provider = config.provider
    if provider is None:
        raise ValueError(f"no key: export {KEY_VARIABLES}")
    try:
        transcripts = sorted(config.projects_dir.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        transcripts = []
    asked: list[Decision] = []
    for transcript in transcripts:
        if len(asked) >= limit:
            break
        turns = [t for t in _turns(transcript) if _wants_routing(t.prompt)]
        listing = _session_view(transcript).listing if turns else None
        if listing is None:
            continue
        for turn in reversed(turns[-(limit - len(asked)) :]):
            request, result = _decide(turn.prompt, listing, turn.in_context, provider, config)
            asked.append(
                _decision(turn.session_id, transcript, turn.prompt, "holdout", provider, result, at=turn.at, source="own", request=request)
            )
    return _score(asked)


def _score(decisions: Sequence[Decision]) -> Score:
    turns_by_path: dict[Path, tuple[Turn, ...]] = {}
    taken: dict[Path, set[int]] = {}
    joined: list[tuple[Decision, Ranking, Advice | Silence, Turn]] = []
    failures: Counter[str] = Counter()
    answered: list[Ranking] = []
    unjoined = 0
    for decision in decisions:
        if isinstance(decision.result, Failure):
            failures[decision.result.kind] += 1
            continue
        answered.append(decision.result.ranking)
        if decision.transcript not in turns_by_path:
            turns_by_path[decision.transcript] = _turns(decision.transcript)
        turns, used = turns_by_path[decision.transcript], taken.setdefault(decision.transcript, set())
        index = next((i for i, t in enumerate(turns) if i not in used and t.prompt_sha == decision.prompt_sha), None)
        if index is None:
            unjoined += 1
            continue
        used.add(index)
        joined.append((decision, decision.result.ranking, decision.result.verdict, turns[index]))

    def agreed(ranking: Ranking, turn: Turn) -> bool:
        return ranking.choice in turn.loaded if ranking.choice else not turn.loaded

    catalogs: dict[str, tuple[int, int]] = {}
    for decision, ranking, _, turn in joined:
        rows, agreeing = catalogs.get(decision.catalog or "none", (0, 0))
        catalogs[decision.catalog or "none"] = (rows + 1, agreeing + agreed(ranking, turn))

    holdout = [(r, t) for d, r, _, t in joined if d.arm == "holdout"]
    buckets: dict[float, tuple[int, int]] = {}
    for ranking, turn in holdout:
        floor = min(int(ranking.confidence * 10), 9) / 10
        rows, agreeing = buckets.get(floor, (0, 0))
        buckets[floor] = (rows + 1, agreeing + agreed(ranking, turn))
    disagreements = sorted(
        (
            Disagreement(d.at, d.prompt_head, r.choice, r.confidence, t.loaded)
            for d, r, _, t in joined
            if d.arm == "holdout" and not agreed(r, t)
        ),
        key=lambda x: x.at,
        reverse=True,
    )[:10]
    latencies = sorted(r.ms for r in answered)
    return Score(
        rows=len(decisions),
        answered=len(answered),
        unjoined=unjoined,
        failures=dict(failures),
        catalogs=catalogs,
        latency_ms=(latencies[len(latencies) // 2], latencies[min(len(latencies) - 1, int(len(latencies) * 0.95))]) if latencies else None,
        cost=sum(r.cost or 0.0 for r in answered),
        live=_arm_score([(v, t) for d, _, v, t in joined if d.arm == "live"]),
        holdout=_arm_score([(v, t) for d, _, v, t in joined if d.arm == "holdout"]),
        calibration=tuple((floor, *buckets[floor]) for floor in sorted(buckets)),
        disagreements=tuple(disagreements),
    )


def _arm_score(rows: Sequence[tuple[Advice | Silence, Turn]]) -> ArmScore:
    counts: Counter[str] = Counter()
    for verdict, turn in rows:
        if isinstance(verdict, Advice):
            counts["named"] += 1
            counts["followed" if verdict.skill in turn.loaded else "other" if turn.loaded else "ignored"] += 1
        else:
            counts["quiet"] += 1
            counts["loaded_anyway"] += bool(turn.loaded)
    return ArmScore(len(rows), counts["named"], counts["followed"], counts["other"], counts["ignored"], counts["quiet"], counts["loaded_anyway"])


def _render(result: Score, source: str) -> str:
    def arm(name: str, s: ArmScore) -> str:
        return (
            f"{name:<10} {s.prompts} prompts. Named {s.named}: followed {s.followed}, other skill {s.other}, "
            f"ignored {s.ignored}. Quiet {s.quiet}: loaded a skill anyway {s.loaded_anyway}."
        )

    failed = ", ".join(f"{kind} {n}" for kind, n in sorted(result.failures.items())) or "none"
    latency = f"p50 {result.latency_ms[0]} ms, p95 {result.latency_ms[1]} ms" if result.latency_ms else "no answers"
    lines = [
        f"source     {source}",
        f"health     {result.rows} decisions, {result.answered} answered, failures {failed}. {latency}. Cost ${result.cost:.4f}.",
        f"matched    {result.answered - result.unjoined} of {result.answered} answered prompts found in their transcripts.",
        "catalog    " + (" | ".join(f"{src} {rows} rows, {ok} agreed" for src, (rows, ok) in sorted(result.catalogs.items())) or "no joined rows"),
        arm("live", result.live),
        arm("holdout", result.holdout),
        "calibration (holdout) " + (" | ".join(f"{floor:.1f}+ {rows} rows, {ok} agreed" for floor, rows, ok in result.calibration) or "no rows"),
    ]
    if result.disagreements:
        lines.append("disagreements (holdout, newest first)")
        for d in result.disagreements:
            agent = ", ".join(d.agent) or "nothing"
            lines.append(f"  {d.at[:10]}  agent {agent}  jev {d.jev or NO_SKILL} {d.confidence:.2f}  \"{d.prompt[:70]}\"")
    if result.live.named:
        lines.append("note       Live advice may have caused the load it matches. Compare with the holdout arm.")
    return "\n".join(lines)


# Claude Code settings. Owns the hook entry and its command line.


def apply_hook(settings: Path, want: bool, dry_run: bool, under: Sequence[Path] = ()) -> HookChange:
    """Make settings.json hold exactly one router entry (want=True) or none (want=False).

    It states the end state instead of applying a delta, so a second run changes nothing. An
    entry whose command holds MARKER is ours, so a moved kit or a new interpreter replaces it.
    Every other entry stays, in order, whatever its shape.
    """
    command = _hook_command(under)
    data = _read_settings(settings)
    hooks = data.get("hooks", {})
    entries = hooks.get(HOOK_EVENT, [])
    ours = [e for e in entries if _is_ours(e)]
    others = [e for e in entries if not _is_ours(e)]
    entry = {"hooks": [{"type": "command", "command": command, "timeout": HOOK_TIMEOUT_S}]}
    changed = ours != [entry] if want else bool(ours)
    if changed and not dry_run:
        wanted = [*others, entry] if want else others
        if wanted:
            hooks[HOOK_EVENT] = wanted
        else:
            hooks.pop(HOOK_EVENT, None)
        data["hooks"] = hooks
        _write_json(settings, data)
    return HookChange(settings, command, bool(ours), want, changed, changed and not dry_run)


def _read_settings(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as error:
        raise SettingsError(f"{path}: {error}") from None
    try:
        data = json.loads(text)
    except ValueError as error:
        raise SettingsError(f"{path} is not valid JSON: {error}") from None
    if not isinstance(data, dict):
        raise SettingsError(f"{path} is not a JSON object")
    if not isinstance(data.get("hooks", {}), dict):
        raise SettingsError(f"{path}: hooks is not an object")
    if not isinstance(data.get("hooks", {}).get(HOOK_EVENT, []), list):
        raise SettingsError(f"{path}: hooks.{HOOK_EVENT} is not a list")
    return data


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            out.write(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        if path.exists():
            shutil.copymode(path, temp)
        os.replace(temp, path)
    except BaseException:
        Path(temp).unlink(missing_ok=True)
        raise


def _is_ours(entry: object) -> bool:
    hooks = entry.get("hooks") if isinstance(entry, dict) else None
    return isinstance(hooks, list) and any(
        isinstance(h, dict) and isinstance(h.get("command"), str) and MARKER in h["command"] for h in hooks
    )


def _hook_command(under: Sequence[Path]) -> str:
    """`|| true` because Python exits 2 when the script is missing, and exit 2 blocks the prompt."""
    parts = [_hook_python(), str(SCRIPT), "hook"]
    for root in under:
        parts += ["--under", str(Path(root).expanduser().resolve())]
    return " ".join(shlex.quote(part) for part in parts) + " || true"


def _hook_python() -> str:
    """`python3` from PATH when it is 3.11 or newer, else this interpreter. A Homebrew
    sys.executable names a minor version that the next upgrade deletes, while the PATH entry
    is a stable link. macOS's own python3 is 3.9, so it never qualifies."""
    found = shutil.which("python3")
    if found:
        check = "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
        try:
            if subprocess.run([found, "-c", check], capture_output=True, timeout=10).returncode == 0:
                return found
        except (OSError, subprocess.SubprocessError):
            pass
    return sys.executable


def _installed_command(settings: Path) -> str | None:
    try:
        entries = _read_settings(settings).get("hooks", {}).get(HOOK_EVENT, [])
    except SettingsError:
        return None
    for entry in entries:
        if _is_ours(entry):
            return next(h["command"] for h in entry["hooks"] if isinstance(h, dict) and MARKER in str(h.get("command")))
    return None


# Verbs.


def _ask(prompt: str, config: Config, cwd: Path) -> int:
    print(f"python     {sys.version.split()[0]} at {sys.executable}")
    installed = _installed_command(config.settings_path)
    if installed is None:
        print(f"hook       not installed in {config.settings_path}")
    else:
        print(f"hook       {installed}")
        interpreter = shlex.split(installed)[0]
        try:
            version = subprocess.run([interpreter, "--version"], capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            version = ""
        print(f"hook runs  {interpreter}, {version or 'which does not start'}")
    provider = config.provider
    if provider is None:
        return _fail(f"export {KEY_VARIABLES} in the shell that starts Claude Code.")
    print(f"provider   {provider.name} {provider.model} via {provider.url}")
    project = _project_dir_for(cwd, config.claude_dir)
    catalog = _recent_listing(project, exclude=None)
    if catalog is None:
        return _fail(f"no skill listing in {project}. Start a Claude Code session in {cwd} first.")
    print(f"catalog    {len(catalog.skills)} skills from {catalog.source}")
    request, result = _decide(prompt, catalog, frozenset(), provider, config)
    capped = f"{request.capped} descriptions capped at {request.capped_at} chars" if request.capped_at is not None else "nothing capped"
    print(f"request    {len(request.body):,} of {MAX_REQUEST_BYTES:,} bytes, {capped}")
    if isinstance(result, Failure):
        print(f"failed     {result.kind} after {result.ms} ms: {result.detail}")
        return _fail(_fix(result, provider))
    ranking, verdict = result.ranking, result.verdict
    tokens = f"{ranking.input_tokens:,} input tokens" if ranking.input_tokens is not None else "tokens not reported"
    cost = f"${ranking.cost:.5f}" if ranking.cost is not None else "cost not reported"
    print(f"answer     {ranking.model} in {ranking.ms} ms, {tokens}, {cost}")
    print("top        " + ", ".join(f"{name} {p:.2f}" for name, p in ranking.top))
    print(f"verdict    {'advise' if isinstance(verdict, Advice) else verdict.value} (threshold {config.speak_at:.2f})")
    print(f"model sees {verdict.line() if isinstance(verdict, Advice) else 'nothing'}")
    return 0


def _fail(fix: str) -> int:
    sys.stdout.flush()
    print(f"fix        {fix}", file=sys.stderr)
    return 1


def _fix(failure: Failure, provider: Provider) -> str:
    variable = next((v for v, name, *_ in PROVIDERS if name == provider.name), "the key")
    if failure.kind == "http" and failure.detail.startswith(("HTTP 401", "HTTP 403")):
        return f"the provider refused the key. Check {variable}."
    if failure.kind == "http" and failure.detail.startswith("HTTP 404"):
        return "the endpoint in PROVIDERS answered 404. Try https://openrouter.ai/api/alpha/decisions there."
    if failure.kind == "timeout":
        return f"Jev did not answer within {JEV_TIMEOUT_S:g} s. Retry, or check the network."
    if failure.kind == "network":
        return "the request did not reach the provider. Check the network."
    return "the provider answered something else. The detail above shows its first bytes."


def _install(remove: bool, dry_run: bool, under: Sequence[Path], config: Config) -> int:
    try:
        change = apply_hook(config.settings_path, want=not remove, dry_run=dry_run, under=under)
    except SettingsError as error:
        return _fail(f"{error}. Repair the file, then run install again.")
    where = change.settings
    if remove:
        if change.changed:
            done = "would remove" if dry_run else "removed"
            print(f"{done} the skill router hook from {where}. The log stays at {config.log_path}.")
        else:
            print(f"no skill router hook in {where}")
        return 0
    if change.changed:
        done = ("would replace" if dry_run else "replaced") if change.was_installed else ("would add" if dry_run else "added")
        print(f"{done} the skill router {HOOK_EVENT} hook in {where}")
    else:
        print(f"the skill router hook is already installed in {where}")
    print(f"  {change.command}   (timeout {HOOK_TIMEOUT_S} s)")
    if not under:
        print("routes prompts from every folder. Pass --under PATH to limit it, since each routed prompt leaves the machine.")
    if config.provider is None:
        print(f"no key in this shell. Export {KEY_VARIABLES} where Claude Code starts, or the hook stays silent.")
    else:
        print(f"this shell has a {config.provider.name} key, so new sessions ask {config.provider.model}")
    return 0


def _score_verb(replay_limit: int | None, config: Config) -> int:
    if replay_limit is not None:
        if config.provider is None:
            return _fail(f"export {KEY_VARIABLES} to replay past prompts.")
        print(_render(replay(replay_limit, config), f"replay of up to {replay_limit} past prompts, nothing logged"))
        return 0
    if not config.log_path.exists():
        print(f"no decisions in {config.log_path} yet. Run score --replay N for a baseline.")
        return 0
    print(_render(score(config), str(config.log_path)))
    return 0


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="skill_router.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    verbs = parser.add_subparsers(dest="verb", required=True)
    hook = verbs.add_parser("hook", help="what Claude Code runs on every prompt")
    install = verbs.add_parser("install", help="add or remove the hook in settings.json")
    install.add_argument("--remove", action="store_true")
    install.add_argument("--dry-run", action="store_true")
    for verb in (hook, install):
        verb.add_argument("--under", action="append", default=[], type=Path, metavar="PATH")
    verbs.add_parser("ask", help="one live call, printed in full").add_argument("prompt", nargs="+")
    verbs.add_parser("score", help="Jev's picks against the skills the agent loaded").add_argument(
        "--replay", type=int, metavar="N"
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exit_:
        return 0 if list(argv[:1]) == ["hook"] else int(exit_.code or 0)
    config = Config.from_env(os.environ, under=getattr(args, "under", ()))
    if args.verb == "hook":
        try:
            if output := run_hook(sys.stdin.buffer.read().decode("utf-8", "replace"), config):
                print(output)
        except Exception:
            pass
        return 0
    if args.verb == "install":
        return _install(args.remove, args.dry_run, args.under, config)
    if args.verb == "ask":
        return _ask(" ".join(args.prompt), config, Path.cwd())
    return _score_verb(args.replay, config)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
