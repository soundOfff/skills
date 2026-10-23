"""Tests for tools/skill_router.py. No key and no network.

Hook tests drive `run_hook` in-process. Their Config points a real Provider at a fake Jev
server on 127.0.0.1 and at a temp CLAUDE_DIR of fixture transcripts. Fixture records copy the
field names of real Claude Code transcript lines, trimmed. Subprocess tests cover what needs the
real command line: the installed command string and the key-less verbs.
"""

from __future__ import annotations

import dataclasses
import hashlib
import http.server
import itertools
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from collections.abc import Callable
from pathlib import Path

import skill_router as sr

SCRIPT = Path(sr.__file__).resolve()
KEY = "test-key"
IDS = itertools.count(1)

SKILLS = {
    "diagnose": (
        "Disciplined diagnosis loop for hard bugs and performance regressions.\n"
        "TRIGGER when the user says: it is broken, throwing, or slow.\n"
        "- not a skill: a bullet inside the description"
    ),
    "flow-tdd": "Test-drive executable behavior through public seams with a red, green, refactor loop.",
    "pstack:setup-pstack": "Configure which models pstack uses per role and at what reasoning budget.",
    "engineering:debug": "Structured debugging session: reproduce, isolate, diagnose, and fix.",
}

Reply = tuple[int, object]


class FakeJev:
    """A ThreadingHTTPServer that records each request and answers with `answer(body)`.

    `answer` returns (status, payload). A dict payload is sent as JSON, bytes as they are.
    `trickle_s` sends the body one byte at a time, so each socket read finishes quickly while
    the whole reply takes far longer.
    """

    def __init__(self, answer: Callable[[dict], Reply], trickle_s: float = 0.0) -> None:
        self.answer = answer
        self.trickle_s = trickle_s
        self.requests: list[dict] = []
        self.raw: list[bytes] = []
        self.authorization: list[str | None] = []

    def __enter__(self) -> FakeJev:
        fake = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                raw = self.rfile.read(int(self.headers["Content-Length"]))
                fake.raw.append(raw)
                fake.requests.append(json.loads(raw))
                fake.authorization.append(self.headers.get("Authorization"))
                status, payload = fake.answer(fake.requests[-1])
                data = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    for i in range(len(data)) if fake.trickle_s else ():
                        self.wfile.write(data[i : i + 1])
                        self.wfile.flush()
                        time.sleep(fake.trickle_s)
                    self.wfile.write(b"" if fake.trickle_s else data)
                except OSError:
                    pass

            def log_message(self, *args: object) -> None:
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}/v1/systemone"
        threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True).start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.server.shutdown()
        self.server.server_close()


def jev(choice: str, confidence: float, **others: float) -> Reply:
    """A well-formed Jev Choice response. Keyword names use __ for ':' and _ for '-'."""
    probabilities = {choice: confidence, **{k.replace("__", ":").replace("_", "-"): v for k, v in others.items()}}
    answer = {"type": "choice", "choice": choice, "confidence": confidence, "probabilities": probabilities}
    return 200, {
        "id": "dec_01",
        "model": "typesafe/jev-1.14",
        "provider": "TypeSafe",
        "answers": {"skill": answer},
        "usage": {"input_tokens": 7104, "output_tokens": 0, "cost": 0.00042},
    }


def always(reply: Reply) -> Callable[[dict], Reply]:
    return lambda body: reply


def by_prompt(replies: dict[str, Reply]) -> Callable[[dict], Reply]:
    return lambda body: replies[body["state"]]


def _base(session: str, cwd: str, kind: str) -> dict:
    return {
        "parentUuid": None,
        "isSidechain": False,
        "type": kind,
        "uuid": f"00000000-0000-4000-8000-{next(IDS):012d}",
        "timestamp": f"2026-10-23T17:{next(IDS) % 60:02d}:00.000Z",
        "userType": "external",
        "entrypoint": "cli",
        "cwd": cwd,
        "sessionId": session,
        "version": "2.1.309",
        "gitBranch": "main",
    }


def listing(session: str, cwd: str, skills: dict[str, str], initial: bool = True) -> dict:
    content = "\n".join(f"- {name}: {text}" for name, text in skills.items())
    attachment = {
        "type": "skill_listing",
        "content": content,
        "skillCount": len(skills),
        "isInitial": initial,
        "names": list(skills),
        "digests": [hashlib.sha256(text.encode()).hexdigest()[:16] for text in skills.values()],
    }
    return {**_base(session, cwd, "attachment"), "attachment": attachment}


def user(session: str, cwd: str, text: str) -> dict:
    return {**_base(session, cwd, "user"), "message": {"role": "user", "content": text}, "promptId": "p-1"}


def slash(session: str, cwd: str, name: str) -> dict:
    text = f"<command-name>/{name}</command-name>\n            <command-message>{name}</command-message>\n            <command-args></command-args>"
    return {**_base(session, cwd, "user"), "message": {"role": "user", "content": text}}


def skill_load(session: str, cwd: str, name: str, sidechain: bool = False) -> dict:
    block = {"type": "tool_use", "id": f"toolu_{next(IDS)}", "name": "Skill", "input": {"skill": name}, "caller": {"type": "direct"}}
    message = {"model": "claude-fable-5-1", "id": f"msg_{next(IDS)}", "type": "message", "role": "assistant", "content": [block]}
    return {**_base(session, cwd, "assistant"), "isSidechain": sidechain, "message": message}


def reply_text(session: str, cwd: str) -> dict:
    message = {"model": "claude-fable-5-1", "id": f"msg_{next(IDS)}", "type": "message", "role": "assistant", "content": [{"type": "text", "text": "Done."}]}
    return {**_base(session, cwd, "assistant"), "message": message}


class RouterCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.claude = self.tmp / "claude"
        self.cwd = self.tmp / "work" / "app"
        self.cwd.mkdir(parents=True)
        self.project = self.claude / "projects" / "-work-app"
        self.project.mkdir(parents=True)

    def transcript(self, session: str, records: list[dict], project: Path | None = None) -> Path:
        path = (project or self.project) / f"{session}.jsonl"
        with path.open("a", encoding="utf-8") as out:
            for record in records:
                out.write(json.dumps(record, separators=(",", ":")) + "\n")
        return path

    def event(self, prompt: str, transcript: Path, cwd: Path | None = None) -> str:
        return json.dumps({
            "session_id": transcript.stem,
            "transcript_path": str(transcript),
            "cwd": str(cwd or self.cwd),
            "prompt": prompt,
            "hook_event_name": "UserPromptSubmit",
        })

    def config(self, url: str = "http://127.0.0.1:9/unused", **overrides: object) -> sr.Config:
        provider = sr.Provider.from_env({"OPENROUTER_API_KEY": KEY})
        settings = {"holdout_every": 0, **overrides}
        return sr.Config(provider=dataclasses.replace(provider, url=url), claude_dir=self.claude, **settings)

    def log(self) -> list[dict]:
        path = self.claude / "skill-router" / "decisions.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text().splitlines()]

    def live_session(self, *records: dict, session: str = "live-session") -> Path:
        cwd = str(self.cwd)
        return self.transcript(session, [user(session, cwd, "earlier prompt about the app"), listing(session, cwd, SKILLS), *records])


class HookTest(RouterCase):
    def test_confident_choice_prints_advice_naming_only_the_skill(self) -> None:
        transcript = self.live_session()
        prompt = "the build is throwing after the deploy"
        with FakeJev(always(jev("diagnose", 0.83, engineering__debug=0.09, flow_tdd=0.05))) as fake:
            out = sr.run_hook(self.event(prompt, transcript), self.config(fake.url))

        context = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(context["hookEventName"], "UserPromptSubmit")
        self.assertIn("`diagnose`", context["additionalContext"])
        self.assertIn("0.83", context["additionalContext"])
        self.assertNotIn("Disciplined", context["additionalContext"])
        self.assertNotIn("engineering:debug", context["additionalContext"])

        [request] = fake.requests
        self.assertEqual(fake.authorization, [f"Bearer {KEY}"])
        self.assertEqual(request["model"], "typesafe/jev-1.14")
        self.assertEqual(request["state"], prompt)
        question = request["questions"]["skill"]
        self.assertEqual(question["type"], "choice")
        self.assertEqual(set(question["criteria"]), {*SKILLS, "no skill"})
        self.assertIn("TRIGGER when the user says: it is broken", question["criteria"]["diagnose"])
        self.assertIn("a bullet inside the description", question["criteria"]["diagnose"])

        [row] = self.log()
        self.assertEqual(
            {k: row[k] for k in ("v", "verdict", "spoke", "arm", "catalog", "choice", "provider", "options")},
            {"v": 1, "verdict": "advise", "spoke": True, "arm": "live", "catalog": "own", "choice": "diagnose", "provider": "openrouter", "options": 5},
        )

    def test_no_skill_and_low_confidence_stay_quiet_but_are_logged(self) -> None:
        transcript = self.live_session()
        replies = {"explain what this function returns": jev("no skill", 0.9), "maybe look at the parser tests": jev("flow-tdd", 0.3)}
        with FakeJev(by_prompt(replies)) as fake:
            outs = [sr.run_hook(self.event(p, transcript), self.config(fake.url)) for p in replies]
        self.assertEqual(outs, ["", ""])
        self.assertEqual([(r["verdict"], r["spoke"]) for r in self.log()], [("no_skill", False), ("low_confidence", False)])

    def test_skill_already_in_context_is_not_advised_again(self) -> None:
        cwd = str(self.cwd)
        cases = {
            "skill tool": skill_load("tool-session", cwd, "diagnose"),
            "slash command": slash("slash-session", cwd, "diagnose"),
        }
        for label, record in cases.items():
            with self.subTest(label):
                transcript = self.live_session(record, session=record["sessionId"])
                with FakeJev(always(jev("diagnose", 0.9))) as fake:
                    out = sr.run_hook(self.event("the build is throwing again after the fix", transcript), self.config(fake.url))
                self.assertEqual(out, "")
                self.assertEqual(self.log()[-1]["verdict"], "already_loaded")

    def test_sidechain_skill_loads_do_not_count_as_in_context(self) -> None:
        transcript = self.live_session(skill_load("live-session", str(self.cwd), "diagnose", sidechain=True))
        with FakeJev(always(jev("diagnose", 0.9))) as fake:
            out = sr.run_hook(self.event("the build is throwing again after the fix", transcript), self.config(fake.url))
        self.assertIn("`diagnose`", out)

    def test_later_listing_adds_skills_and_the_newest_description_wins(self) -> None:
        cwd = str(self.cwd)
        delta = {"plugin-authoring": "Make a mod for the interface.", "flow-tdd": "Rewritten description for the tdd loop."}
        transcript = self.live_session(listing("live-session", cwd, delta, initial=False))
        with FakeJev(always(jev("no skill", 0.9))) as fake:
            sr.run_hook(self.event("add a status line that shows the branch", transcript), self.config(fake.url))
        criteria = fake.requests[0]["questions"]["skill"]["criteria"]
        self.assertEqual(set(criteria), {*SKILLS, "plugin-authoring", "no skill"})
        self.assertEqual(criteria["flow-tdd"], "Rewritten description for the tdd loop.")

    def test_first_prompt_uses_the_newest_sibling_listing_in_the_same_folder(self) -> None:
        cwd = str(self.cwd)
        older = self.transcript("older", [listing("older", cwd, {"diagnose": SKILLS["diagnose"]})])
        newer = self.transcript("newer", [listing("newer", cwd, {"flow-tdd": SKILLS["flow-tdd"], "grilling": "Interview the user."})])
        os.utime(older, (1_000_000, 1_000_000))
        os.utime(newer, (2_000_000, 2_000_000))
        other_project = self.claude / "projects" / "-other-repo"
        other_project.mkdir()
        self.transcript("elsewhere", [listing("elsewhere", "/other/repo", {"repo-only-skill": "Only in another repository."})], other_project)
        live = self.transcript("first-prompt", [{"type": "mode", "mode": "default", "sessionId": "first-prompt"}])

        with FakeJev(always(jev("flow-tdd", 0.8))) as fake:
            out = sr.run_hook(self.event("write the failing test for the parser first", live), self.config(fake.url))

        self.assertIn("`flow-tdd`", out)
        self.assertEqual(set(fake.requests[0]["questions"]["skill"]["criteria"]), {"flow-tdd", "grilling", "no skill"})
        self.assertEqual(self.log()[-1]["catalog"], "sibling")

    def test_first_session_in_a_new_folder_logs_no_listing_and_sends_nothing(self) -> None:
        other_project = self.claude / "projects" / "-other-repo"
        other_project.mkdir()
        self.transcript("elsewhere", [listing("elsewhere", "/other/repo", SKILLS)], other_project)
        live = self.project / "brand-new.jsonl"
        with FakeJev(always(jev("diagnose", 0.9))) as fake:
            out = sr.run_hook(self.event("the build is throwing after the deploy", live), self.config(fake.url))
        self.assertEqual(out, "")
        self.assertEqual(fake.requests, [])
        [row] = self.log()
        self.assertEqual((row["verdict"], row["error"], row["catalog"]), ("failed", "no_listing", None))

    def test_failures_stay_silent_and_are_logged_by_kind(self) -> None:
        transcript = self.live_session()
        cases: list[tuple[str, Reply, str]] = [
            ("server error", (500, {"error": "boom"}), "http"),
            ("garbage body", (200, b"<html>not json</html>"), "bad_response"),
            ("choice never offered", jev("unknown-skill", 0.9), "bad_response"),
            ("confidence out of range", jev("diagnose", 1.7), "bad_response"),
        ]
        for label, reply, kind in cases:
            with self.subTest(label), FakeJev(always(reply)) as fake:
                out = sr.run_hook(self.event(f"the build is throwing, case {label}", transcript), self.config(fake.url))
                self.assertEqual(out, "")
                self.assertEqual(self.log()[-1]["error"], kind)

        with self.subTest("trickles past the deadline"), FakeJev(always(jev("diagnose", 0.9)), trickle_s=0.02) as fake:
            started = time.monotonic()
            out = sr.run_hook(self.event("the build is throwing, slow case", transcript), self.config(fake.url, http_timeout_s=0.2))
            self.assertLess(time.monotonic() - started, 1.0)
            self.assertEqual(out, "")
            self.assertEqual(self.log()[-1]["error"], "timeout")

        with self.subTest("nothing listening"):
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", 0))
                port = probe.getsockname()[1]
            out = sr.run_hook(self.event("the build is throwing, closed port", transcript), self.config(f"http://127.0.0.1:{port}/v1"))
            self.assertEqual(out, "")
            self.assertEqual(self.log()[-1]["error"], "network")

    def test_commands_harness_text_and_short_replies_never_reach_jev(self) -> None:
        transcript = self.live_session()
        prompts = ["/flow-build 12", "<task-notification>done</task-notification>", "yes", "use /pstack:architect for this change"]
        with FakeJev(always(jev("diagnose", 0.9))) as fake:
            outs = [sr.run_hook(self.event(p, transcript), self.config(fake.url)) for p in prompts]
        self.assertEqual(outs, [""] * len(prompts))
        self.assertEqual(fake.requests, [])
        self.assertEqual(self.log(), [])

    def test_garbage_stdin_is_silent(self) -> None:
        for raw in ["", "[]", "not json", '{"prompt": 3}', '{"session_id": "s", "prompt": "the build is throwing"}']:
            with self.subTest(raw):
                self.assertEqual(sr.run_hook(raw, self.config()), "")
        self.assertEqual(self.log(), [])

    def test_holdout_session_asks_and_logs_but_stays_quiet(self) -> None:
        transcript = self.live_session()
        with FakeJev(always(jev("diagnose", 0.9))) as fake:
            out = sr.run_hook(self.event("the build is throwing after the deploy", transcript), self.config(fake.url, holdout_every=1))
        self.assertEqual(out, "")
        self.assertEqual(len(fake.requests), 1)
        [row] = self.log()
        self.assertEqual((row["arm"], row["verdict"], row["spoke"]), ("holdout", "advise", False))

    def test_under_limits_routing_to_the_chosen_roots(self) -> None:
        transcript = self.live_session()
        outside = self.tmp / "employer" / "repo"
        outside.mkdir(parents=True)
        with FakeJev(always(jev("diagnose", 0.9))) as fake:
            config = self.config(fake.url, under=(self.tmp / "work",))
            silent = sr.run_hook(self.event("the build is throwing after the deploy", transcript, cwd=outside), config)
            self.assertEqual((silent, fake.requests, self.log()), ("", [], []))
            spoken = sr.run_hook(self.event("the build is throwing after the deploy", transcript), config)
        self.assertIn("`diagnose`", spoken)

    def test_request_fits_the_byte_budget_with_a_150_skill_listing(self) -> None:
        short = {f"skill-{i:03d}": f"Short description number {i} " + "x" * 120 for i in range(144)}
        long = {f"long-{i}": f"Long description {i} " + "word " * 280 for i in range(6)}
        skills = {**short, **long}
        transcript = self.transcript("big", [listing("big", str(self.cwd), skills)])
        with FakeJev(always(jev("no skill", 0.9))) as fake:
            sr.run_hook(self.event("a long prompt " * 400, transcript), self.config(fake.url))

        self.assertLessEqual(len(fake.raw[0]), 30_000)
        criteria = fake.requests[0]["questions"]["skill"]["criteria"]
        self.assertEqual(set(criteria), {*skills, "no skill"})
        for name, text in short.items():
            self.assertEqual(criteria[name], text)
        for name, text in long.items():
            self.assertLess(len(criteria[name]), len(text.strip()))
            self.assertTrue(text.startswith(criteria[name]))
        self.assertIsNotNone(self.log()[-1]["capped_at"])


class ProviderTest(unittest.TestCase):
    def test_no_key_means_no_provider(self) -> None:
        self.assertIsNone(sr.Provider.from_env({}))
        self.assertIsNone(sr.Provider.from_env({"OPENROUTER_API_KEY": " ", "TYPESAFE_API_KEY": ""}))

    def test_typesafe_wins_and_openrouter_is_pinned_to_jev_1_14(self) -> None:
        both = sr.Provider.from_env({"OPENROUTER_API_KEY": "or-key", "TYPESAFE_API_KEY": "ts-key"})
        self.assertEqual((both.name, both.url, both.model), ("typesafe", "https://api.typesafe.ai/v1/systemone", "jev-latest"))
        openrouter = sr.Provider.from_env({"OPENROUTER_API_KEY": "or-key"})
        self.assertEqual(
            (openrouter.name, openrouter.url, openrouter.model),
            ("openrouter", "https://openrouter.ai/api/v1/systemone", "typesafe/jev-1.14"),
        )
        self.assertNotIn("or-key", repr(openrouter))


FOREIGN = {"hooks": [{"type": "command", "command": "printf '{}\\n'", "timeout": 10}]}
STOP = {"hooks": [{"type": "command", "command": "notify done"}]}


class InstallTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.settings = self.tmp / "settings.json"
        self.original = {
            "model": "opus",
            "hooks": {"UserPromptSubmit": [FOREIGN, "not-a-dict-entry"], "Stop": [STOP]},
            "enabledPlugins": {"pstack@cursor-plugins": True},
            "skillListingBudgetFraction": 0.05,
        }
        self.settings.write_text(json.dumps(self.original, indent=2))

    def read(self) -> dict:
        return json.loads(self.settings.read_text())

    def ours(self) -> list[dict]:
        return [e for e in self.read()["hooks"]["UserPromptSubmit"] if isinstance(e, dict) and "/tools/skill_router.py" in json.dumps(e)]

    def test_install_twice_writes_once_and_keeps_every_other_entry(self) -> None:
        first = sr.apply_hook(self.settings, want=True, dry_run=False)
        after_first = self.settings.read_bytes()
        second = sr.apply_hook(self.settings, want=True, dry_run=False)

        self.assertEqual((first.written, second.written, second.changed), (True, False, False))
        self.assertEqual(self.settings.read_bytes(), after_first)
        data = self.read()
        self.assertEqual(data["hooks"]["UserPromptSubmit"][:2], [FOREIGN, "not-a-dict-entry"])
        self.assertEqual(data["hooks"]["Stop"], [STOP])
        self.assertEqual({k: data[k] for k in ("model", "enabledPlugins", "skillListingBudgetFraction")},
                         {k: self.original[k] for k in ("model", "enabledPlugins", "skillListingBudgetFraction")})
        [entry] = self.ours()
        [hook] = entry["hooks"]
        self.assertEqual(hook["timeout"], 5)
        self.assertIn(str(SCRIPT), hook["command"])
        self.assertTrue(hook["command"].endswith(" hook || true"))

    def test_reinstall_from_a_moved_kit_replaces_the_entry(self) -> None:
        stale = {"hooks": [{"type": "command", "command": "/usr/bin/python3 /old/kit/tools/skill_router.py hook || true", "timeout": 5}]}
        self.original["hooks"]["UserPromptSubmit"].append(stale)
        self.settings.write_text(json.dumps(self.original))
        change = sr.apply_hook(self.settings, want=True, dry_run=False)
        self.assertEqual((change.was_installed, change.written), (True, True))
        [entry] = self.ours()
        self.assertNotIn("/old/kit", json.dumps(entry))

    def test_remove_deletes_only_ours_and_dry_run_writes_nothing(self) -> None:
        sr.apply_hook(self.settings, want=True, dry_run=False)
        installed = self.settings.read_bytes()
        dry = sr.apply_hook(self.settings, want=False, dry_run=True)
        self.assertEqual((dry.changed, dry.written, dry.is_installed), (True, False, False))
        self.assertEqual(self.settings.read_bytes(), installed)

        removed = sr.apply_hook(self.settings, want=False, dry_run=False)
        self.assertTrue(removed.written)
        self.assertEqual(self.read()["hooks"], self.original["hooks"])
        self.assertFalse(sr.apply_hook(self.settings, want=False, dry_run=False).written)

    def test_dry_run_install_reports_the_change_and_writes_nothing(self) -> None:
        before = self.settings.read_bytes()
        change = sr.apply_hook(self.settings, want=True, dry_run=True)
        self.assertEqual((change.changed, change.written, change.is_installed), (True, False, True))
        self.assertEqual(self.settings.read_bytes(), before)

    def test_under_is_baked_into_the_command(self) -> None:
        root = self.tmp / "personal"
        root.mkdir()
        change = sr.apply_hook(self.settings, want=True, dry_run=False, under=[root])
        self.assertIn(f"hook --under {root.resolve()} || true", change.command)
        self.assertEqual(self.ours()[0]["hooks"][0]["command"], change.command)

    def test_refuses_settings_it_cannot_read_and_leaves_them_untouched(self) -> None:
        for label, text in {
            "invalid json": "{not json",
            "top-level list": "[]",
            "hooks is a string": '{"hooks": "none"}',
            "event is an object": '{"hooks": {"UserPromptSubmit": {}}}',
        }.items():
            with self.subTest(label):
                self.settings.write_text(text)
                with self.assertRaises(sr.SettingsError):
                    sr.apply_hook(self.settings, want=True, dry_run=False)
                self.assertEqual(self.settings.read_text(), text)


class CommandLineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(self.tmp), "CLAUDE_DIR": str(self.tmp / "claude")}
        self.event = json.dumps({
            "session_id": "s-1", "transcript_path": str(self.tmp / "s-1.jsonl"), "cwd": str(self.tmp),
            "prompt": "the build is throwing after the deploy", "hook_event_name": "UserPromptSubmit",
        })

    def run_router(self, *args: str, stdin: str = "") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True, env=self.env, timeout=60)

    def test_installed_command_exits_zero_when_the_script_is_gone(self) -> None:
        kit = self.tmp / "kit" / "tools"
        kit.mkdir(parents=True)
        shutil.copy(SCRIPT, kit / "skill_router.py")
        subprocess.run([sys.executable, str(kit / "skill_router.py"), "install"], env=self.env, check=True, capture_output=True, timeout=60)
        settings = json.loads((self.tmp / "claude" / "settings.json").read_text())
        command = settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        shutil.rmtree(self.tmp / "kit")

        result = subprocess.run(["/bin/sh", "-c", command], input=self.event, capture_output=True, text=True, env=self.env, timeout=60)
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_hook_without_a_key_prints_nothing_and_exits_zero(self) -> None:
        result = self.run_router("hook", stdin=self.event)
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertFalse((self.tmp / "claude" / "skill-router").exists())

    def test_ask_without_a_key_exits_one_naming_both_variables(self) -> None:
        result = self.run_router("ask", "the build is throwing after the deploy")
        self.assertEqual(result.returncode, 1)
        self.assertIn("TYPESAFE_API_KEY", result.stdout + result.stderr)
        self.assertIn("OPENROUTER_API_KEY", result.stdout + result.stderr)


class ScoreTest(RouterCase):
    def test_score_joins_each_arm_to_the_skills_the_agent_loaded(self) -> None:
        cwd = str(self.cwd)
        a, b = "session-a", "session-b"
        replies = {
            "the build is throwing after the deploy": jev("diagnose", 0.83),
            "write the failing test for the parser first": jev("flow-tdd", 0.8),
            "explain what this function returns to callers": jev("no skill", 0.9),
            "this prompt never reaches the transcript": jev("no skill", 0.7),
            "the tests are flaky on CI, find out why": jev("diagnose", 0.7),
            "set up the models for the pstack roles": jev("flow-tdd", 0.6),
        }
        live_turns = [
            ("the build is throwing after the deploy", ["diagnose"]),
            ("write the failing test for the parser first", []),
            ("explain what this function returns to callers", ["engineering:debug"]),
        ]
        session_a = self.transcript(a, [user(a, cwd, "start the app"), listing(a, cwd, SKILLS)])
        with FakeJev(by_prompt(replies)) as fake:
            live = self.config(fake.url, holdout_every=0)
            for prompt, loads in live_turns:
                sr.run_hook(self.event(prompt, session_a), live)
                self.transcript(a, [user(a, cwd, prompt), *(skill_load(a, cwd, s) for s in loads), reply_text(a, cwd)])
            sr.run_hook(self.event("this prompt never reaches the transcript", session_a), live)

            holdout = self.config(fake.url, holdout_every=1)
            session_b = self.transcript(b, [{"type": "mode", "mode": "default", "sessionId": b}])
            sr.run_hook(self.event("the tests are flaky on CI, find out why", session_b), holdout)
            self.transcript(b, [user(b, cwd, "the tests are flaky on CI, find out why"), listing(b, cwd, SKILLS), skill_load(b, cwd, "diagnose")])
            sr.run_hook(self.event("set up the models for the pstack roles", session_b), holdout)
            self.transcript(b, [user(b, cwd, "set up the models for the pstack roles"), skill_load(b, cwd, "pstack:setup-pstack")])

        empty_project = self.claude / "projects" / "-empty"
        empty_project.mkdir()
        sr.run_hook(self.event("the build is throwing after the deploy", empty_project / "c.jsonl"), live)

        result = sr.score(live)
        self.assertEqual(result.live, sr.ArmScore(prompts=3, named=2, followed=1, other=0, ignored=1, quiet=1, loaded_anyway=1))
        self.assertEqual(result.holdout, sr.ArmScore(prompts=2, named=2, followed=1, other=1, ignored=0, quiet=0, loaded_anyway=0))
        self.assertEqual((result.rows, result.answered, result.unjoined), (7, 6, 1))
        self.assertEqual(result.failures, {"no_listing": 1})
        self.assertEqual(result.catalogs, {"own": (4, 1), "sibling": (1, 1)})
        self.assertEqual(sum(rows for _, rows, _ in result.calibration), 2)
        self.assertEqual([(d.jev, d.agent) for d in result.disagreements], [("flow-tdd", ("pstack:setup-pstack",))])
        self.assertAlmostEqual(result.cost, 6 * 0.00042)

    def test_replay_scores_past_prompts_and_writes_no_log(self) -> None:
        cwd, s = str(self.cwd), "past-session"
        self.transcript(s, [
            user(s, cwd, "the build is throwing after the deploy"), listing(s, cwd, SKILLS), skill_load(s, cwd, "diagnose"),
            user(s, cwd, "yes"),
            user(s, cwd, "write the failing test for the parser first"), skill_load(s, cwd, "flow-tdd"),
            user(s, cwd, "rename this variable across the module"),
        ])
        replies = {
            "the build is throwing after the deploy": jev("diagnose", 0.8),
            "write the failing test for the parser first": jev("engineering:debug", 0.6),
            "rename this variable across the module": jev("no skill", 0.9),
        }
        with FakeJev(by_prompt(replies)) as fake:
            result = sr.replay(10, self.config(fake.url))
        self.assertEqual(sorted(r["state"] for r in fake.requests), sorted(replies))
        self.assertEqual(result.holdout, sr.ArmScore(prompts=3, named=2, followed=1, other=1, ignored=0, quiet=1, loaded_anyway=0))
        self.assertEqual(result.catalogs, {"own": (3, 2)})
        self.assertFalse((self.claude / "skill-router").exists())


if __name__ == "__main__":
    unittest.main()
