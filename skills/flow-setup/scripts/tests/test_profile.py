"""Behavior tests for write_profile.py and doctor.py.

Run from the kit root with any Python 3.9 or later:

    python3 -m unittest discover -s skills/flow-setup/scripts/tests -t skills/flow-setup/scripts

Each test builds a throwaway git repository and drives both scripts through
their command lines with the interpreter that runs the suite. Running the suite
with /usr/bin/python3 therefore also proves the scripts run on Python 3.9.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
GATES = ("install", "dev", "format", "lint", "typecheck", "test", "test-file", "e2e", "build", "design", "health")
SOURCES = ("Domain language", "Decisions", "Conventions", "Design system", "Structure")
DOCS = ("issue-tracker.md", "ticket-standard.md", "pr-standard.md", "domain.md")
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def answers(**changes: object) -> dict:
    commands = {gate: "n/a" for gate in GATES}
    commands.update(lint="git diff --check", test="git --version")
    data = {
        "forge": "github",
        "tracker": "github",
        "base": "main",
        "publish_mode": "draft",
        "merge_strategy": "squash",
        "commands": commands,
        "sources": {source: "none" for source in SOURCES},
    }
    data.update(changes)
    return data


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), capture_output=True, text=True, env=ENV)


class Repo:
    def __init__(self, test: unittest.TestCase) -> None:
        self.home = Path(tempfile.mkdtemp(prefix="flow-setup-test-")).resolve()
        test.addCleanup(shutil.rmtree, self.home)
        self.root = self.home / "repo"
        self.root.mkdir()
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/main")
        self.git("-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-q", "--allow-empty", "-m", "init")

    def git(self, *args: str) -> None:
        result = run("git", "-C", str(self.root), *args)
        if result.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")

    def write(self, data: object, *flags: str, where: Path | None = None) -> subprocess.CompletedProcess:
        path = self.home / "answers.json"
        path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        return run(sys.executable, str(SCRIPTS / "write_profile.py"), str(where or self.root), str(path), *flags)

    def doctor(self, where: Path | None = None) -> subprocess.CompletedProcess:
        return run(sys.executable, str(SCRIPTS / "doctor.py"), "repo", str(where or self.root))

    def text(self, rel: str) -> str:
        return (self.root / rel).read_bytes().decode("utf-8")

    def snapshot(self) -> dict[str, bytes]:
        return {
            p.relative_to(self.root).as_posix(): p.read_bytes()
            for p in sorted(self.root.rglob("*"))
            if ".git" not in p.relative_to(self.root).parts and p.is_file()
        }


class ProfileTest(unittest.TestCase):
    def assertWrote(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assertHealthy(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r"\d+ checks, 0 failed, ")

    def test_each_tracker_writes_a_profile_the_doctor_passes(self) -> None:
        cases = (
            ("github", "github", "GitHub", ".github/pull_request_template.md", "Closes #<issue>"),
            ("gitlab", "gitlab", "GitLab", ".gitlab/merge_request_templates/Default.md", "Closes #<issue>"),
            ("linear", "github", "Linear", ".github/pull_request_template.md", "Fixes ENG-<number>"),
            ("local", "none", "Local", None, "Closes <issue id>"),
        )
        for tracker, forge, title, template, closing in cases:
            with self.subTest(tracker=tracker):
                repo = Repo(self)
                self.assertWrote(repo.write(answers(tracker=tracker, forge=forge, linear_team="ENG")))
                self.assertHealthy(repo.doctor())
                block = repo.text("AGENTS.md")
                headings = [line for line in block.splitlines() if line.startswith("## ")]
                self.assertEqual(headings, ["## Settings", "## Commands", "## Sources of truth", "## Delivery workflow", "## Golden rules"])
                self.assertIn(f"| Tracker | `{tracker}` |", block)
                self.assertIn(f"| Closing reference | `{closing}` |", block)
                self.assertIn("| Ready label | `ready-for-agent` |", block)
                self.assertIn(f"| Pull request template | `{template}` |" if template else "| Pull request template | none |", block)
                if template:
                    self.assertTrue((repo.root / template).is_file())
                self.assertEqual(repo.text("docs/agents/issue-tracker.md").splitlines()[0], f"# Issue tracker: {title}")
                for name in DOCS:
                    self.assertNotIn("{{", repo.text(f"docs/agents/{name}"), name)
                self.assertFalse((repo.root / "docs/agents/triage-labels.md").exists())

    def test_claude_md_linked_to_agents_md_stays_a_link(self) -> None:
        repo = Repo(self)
        (repo.root / "AGENTS.md").write_text("# Notes\n", encoding="utf-8")
        os.symlink("AGENTS.md", repo.root / "CLAUDE.md")
        dry = repo.write(answers(), "--dry-run")
        self.assertWrote(dry)
        self.assertIn("CLAUDE.md -> AGENTS.md", dry.stdout)
        self.assertEqual(repo.text("AGENTS.md"), "# Notes\n", "a dry run writes nothing")
        self.assertWrote(repo.write(answers()))
        self.assertTrue((repo.root / "CLAUDE.md").is_symlink())
        self.assertEqual(os.readlink(repo.root / "CLAUDE.md"), "AGENTS.md")
        self.assertFalse((repo.root / "AGENTS.md").is_symlink())
        text = repo.text("AGENTS.md")
        self.assertTrue(text.startswith("# Notes\n"))
        self.assertNotIn("@AGENTS.md", text)
        doctor = repo.doctor()
        self.assertHealthy(doctor)
        self.assertIn("PASS CLAUDE.md: links to AGENTS.md", doctor.stdout)

    def test_agents_md_linked_to_claude_md_stays_a_link(self) -> None:
        repo = Repo(self)
        (repo.root / "CLAUDE.md").write_text("# Team notes\n", encoding="utf-8")
        os.symlink("CLAUDE.md", repo.root / "AGENTS.md")
        dry = repo.write(answers(), "--dry-run")
        self.assertWrote(dry)
        self.assertIn("AGENTS.md -> CLAUDE.md", dry.stdout)
        self.assertIn("through the link", dry.stdout)
        self.assertWrote(repo.write(answers()))
        self.assertTrue((repo.root / "AGENTS.md").is_symlink())
        self.assertEqual(os.readlink(repo.root / "AGENTS.md"), "CLAUDE.md")
        self.assertFalse((repo.root / "CLAUDE.md").is_symlink())
        text = repo.text("CLAUDE.md")
        self.assertTrue(text.startswith("# Team notes\n"))
        self.assertIn("<!-- flow:end -->", text)
        self.assertNotIn("@AGENTS.md", text)
        doctor = repo.doctor()
        self.assertHealthy(doctor)
        self.assertIn("PASS CLAUDE.md: is the file AGENTS.md links to", doctor.stdout)

    def test_doctor_fails_a_claude_md_that_copies_the_block(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        (repo.root / "CLAUDE.md").write_text("@AGENTS.md\n\n" + repo.text("AGENTS.md"), encoding="utf-8")
        doctor = repo.doctor()
        self.assertEqual(doctor.returncode, 1, doctor.stdout)
        self.assertIn("FAIL CLAUDE.md: repeats the flow block", doctor.stdout)

    def test_changed_base_branch_updates_only_the_settings(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        docs = {name: repo.text(f"docs/agents/{name}") for name in DOCS}
        repo.git("branch", "develop")
        second = repo.write(answers(base="develop"))
        self.assertWrote(second)
        self.assertIn("update  AGENTS.md", second.stdout)
        for name in DOCS:
            self.assertIn(f"same    docs/agents/{name}", second.stdout)
            self.assertEqual(repo.text(f"docs/agents/{name}"), docs[name])
        block = repo.text("AGENTS.md")
        self.assertIn("| Base branch | `develop` |", block)
        self.assertNotIn("`main`", block)
        doctor = repo.doctor()
        self.assertHealthy(doctor)
        self.assertIn("PASS base branch: develop resolves to refs/heads/develop", doctor.stdout)

    def test_crlf_text_outside_the_block_keeps_its_bytes(self) -> None:
        repo = Repo(self)
        before = b"# Notes\r\n\r\nKeep this line.\r\n"
        (repo.root / "AGENTS.md").write_bytes(before)
        (repo.root / "CLAUDE.md").write_bytes(b"# Claude\r\n")
        self.assertWrote(repo.write(answers()))
        agents = (repo.root / "AGENTS.md").read_bytes()
        self.assertTrue(agents.startswith(before))
        self.assertIsNone(re.search(rb"(?<!\r)\n", agents), "every line of AGENTS.md ends in CRLF")
        self.assertEqual((repo.root / "CLAUDE.md").read_bytes(), b"# Claude\r\n\r\n@AGENTS.md\r\n")
        self.assertEqual(agents[: agents.index(b"<!-- flow:begin")], before + b"\r\n", "the block is appended after one blank line")
        (repo.root / "AGENTS.md").write_bytes(agents + b"\r\nTrailing note, no final newline")

        def outside(data: bytes) -> tuple[bytes, bytes]:
            end = data.index(b"<!-- flow:end -->") + len(b"<!-- flow:end -->")
            return data[: data.index(b"<!-- flow:begin")], data[end:]

        kept = outside((repo.root / "AGENTS.md").read_bytes())
        repo.git("branch", "develop")
        self.assertWrote(repo.write(answers(base="develop")))
        agents = (repo.root / "AGENTS.md").read_bytes()
        self.assertEqual(outside(agents), kept)
        self.assertIn(b"| Base branch | `develop` |\r\n", agents)
        self.assertHealthy(repo.doctor())

    def test_unchanged_second_run_reports_nothing_to_change(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        files = repo.snapshot()
        second = repo.write(answers())
        self.assertWrote(second)
        lines = second.stdout.splitlines()
        self.assertEqual(lines[-1], "nothing to change")
        self.assertEqual([line for line in lines[:-1] if not line.startswith(("same ", "skip "))], [])
        self.assertEqual(repo.snapshot(), files)

    def test_stale_version_marker_warns_and_a_rerun_clears_it(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        current = re.search(r"<!-- flow:begin v=[0-9a-f]{12} -->", repo.text("AGENTS.md")).group(0)
        for stale in ("<!-- flow:begin v=000000000000 -->", "<!-- flow:begin -->"):
            with self.subTest(marker=stale):
                (repo.root / "AGENTS.md").write_text(repo.text("AGENTS.md").replace(current, stale), encoding="utf-8")
                doctor = repo.doctor()
                self.assertHealthy(doctor)
                self.assertIn("WARN flow block version:", doctor.stdout)
                self.assertIn("fix: re-run /flow-setup", doctor.stdout)
                self.assertWrote(repo.write(answers()))
                self.assertIn(current, repo.text("AGENTS.md"))
                self.assertIn("PASS flow block version:", repo.doctor().stdout)

    def test_broken_profile_fails_the_doctor(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        block = repo.text("AGENTS.md").replace("| Publish mode | `draft` |", "| Publish mode | `sometimes` |")
        (repo.root / "AGENTS.md").write_text(block, encoding="utf-8")
        (repo.root / ".github/pull_request_template.md").unlink()
        tracker = repo.text("docs/agents/issue-tracker.md").replace("# Issue tracker: GitHub", "# Issue tracker: Linear", 1)
        (repo.root / "docs/agents/issue-tracker.md").write_text(tracker, encoding="utf-8")
        doctor = repo.doctor()
        self.assertEqual(doctor.returncode, 1, doctor.stdout)
        self.assertRegex(doctor.stdout, r"FAIL settings: .*Publish mode 'sometimes' is not one of draft, ready")
        self.assertIn("FAIL pull request template: .github/pull_request_template.md does not exist", doctor.stdout)
        self.assertIn("FAIL docs/agents/issue-tracker.md: the title says Linear, but the Tracker setting is github", doctor.stdout)

    def test_doctor_checks_that_runner_gates_are_declared(self) -> None:
        repo = Repo(self)
        (repo.root / "package.json").write_text(json.dumps({"scripts": {"lint": "true"}}), encoding="utf-8")
        (repo.root / "Makefile").write_text("VERSION := 1\n.PHONY: build\nbuild: deps\n\t@true\n", encoding="utf-8")
        (repo.root / "justfile").write_text("set shell := [\"sh\", \"-c\"]\nfmt:\n    true\n", encoding="utf-8")
        commands = {gate: "n/a" for gate in GATES}
        commands.update(
            lint="npm run lint",
            test="pnpm run nope",
            build="make build",
            typecheck="make nope",
            format="just fmt",
            e2e="just nope",
            dev="N/A",
        )
        self.assertWrote(repo.write(answers(commands=commands)))
        out = repo.doctor().stdout
        self.assertRegex(out, r"gate lint: `npm run lint`: .*package\.json declares lint")
        self.assertRegex(out, r"FAIL gate test: `pnpm run nope`: .*package\.json declares no script nope")
        self.assertRegex(out, r"gate build: `make build`: .*Makefile declares build")
        self.assertRegex(out, r"FAIL gate typecheck: `make nope`: .*Makefile declares no target nope")
        self.assertRegex(out, r"gate format: `just fmt`: .*justfile declares fmt")
        self.assertRegex(out, r"FAIL gate e2e: `just nope`: .*justfile declares no recipe nope")
        self.assertNotIn("gate dev", out)

    def test_doctor_reports_only_the_kits_placeholders(self) -> None:
        repo = Repo(self)
        self.assertWrote(repo.write(answers()))
        (repo.root / "docs/agents/domain.md").write_text(repo.text("docs/agents/domain.md") + "\n{{base}} and {{name}}\n", encoding="utf-8")
        doctor = repo.doctor()
        self.assertEqual(doctor.returncode, 1, doctor.stdout)
        self.assertIn("FAIL docs/agents/domain.md: unfilled placeholders {{base}}\n", doctor.stdout)

    def test_a_value_is_substituted_once(self) -> None:
        repo = Repo(self)
        commands = {gate: "n/a" for gate in GATES}
        commands.update(test="make test ARGS={{src:Structure}}")
        sources = {source: "none" for source in SOURCES}
        sources.update(Structure="docs/{{cmd:test}}.md")
        self.assertWrote(repo.write(answers(commands=commands, sources=sources)))
        block = repo.text("AGENTS.md")
        self.assertIn("| test | `make test ARGS={{src:Structure}}` |", block)
        self.assertIn("| Structure | `docs/{{cmd:test}}.md` |", block)

    def test_invalid_answers_exit_2_without_a_traceback(self) -> None:
        cases = {
            "commands": answers(commands=["npm test"]),
            "sources": answers(sources="none"),
            "forge": answers(forge=3),
            "labels": answers(labels={}),
            "ready_label": answers(ready_label=""),
            "base": answers(base="not a branch"),
            "linear_team": answers(tracker="linear"),
            "JSON object": "[]",
            "not valid JSON": "{",
        }
        for word, data in cases.items():
            with self.subTest(case=word):
                repo = Repo(self)
                result = repo.write(data)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertIn(word, result.stderr)
                self.assertFalse((repo.root / "AGENTS.md").exists())

    def test_new_files_get_0666_minus_the_umask_and_existing_files_keep_their_mode(self) -> None:
        repo = Repo(self)
        (repo.root / "CLAUDE.md").write_text("# Claude\n", encoding="utf-8")
        os.chmod(repo.root / "CLAUDE.md", 0o640)
        mask = os.umask(0)
        os.umask(mask)
        self.assertWrote(repo.write(answers()))
        for rel in ("AGENTS.md", "docs/agents/domain.md", ".github/pull_request_template.md"):
            self.assertEqual((repo.root / rel).stat().st_mode & 0o777, 0o666 & ~mask, rel)
        self.assertEqual((repo.root / "CLAUDE.md").stat().st_mode & 0o777, 0o640)

    def test_a_subdirectory_resolves_to_the_repository_root(self) -> None:
        repo = Repo(self)
        inner = repo.root / "packages" / "app"
        inner.mkdir(parents=True)
        self.assertWrote(repo.write(answers(), where=inner))
        self.assertTrue((repo.root / "AGENTS.md").is_file())
        self.assertFalse((inner / "AGENTS.md").exists())
        doctor = repo.doctor(where=inner)
        self.assertHealthy(doctor)
        self.assertIn(f"PASS git repository: {repo.root}\n", doctor.stdout)


if __name__ == "__main__":
    unittest.main()
