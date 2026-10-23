import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import { targetFingerprint } from "../lib/git.mjs";

const runner = fileURLToPath(new URL("../run-review.mjs", import.meta.url));

describe("adversarial review job lifecycle", () => {
	it("runs the same when started through a symlinked skill folder", () => {
		const temporary = mkdtempSync(join(tmpdir(), "flow-adv-symlink-"));
		try {
			const linked = join(temporary, "flow-adv-review");
			symlinkSync(dirname(dirname(runner)), linked);
			const run = (script) =>
				spawnSync(process.execPath, [script, "status", "no-such-job"], { cwd: temporary, encoding: "utf8" });
			const direct = run(runner);
			const viaLink = run(join(linked, "scripts", "run-review.mjs"));
			assert.notEqual(direct.status, 0);
			assert.equal(viaLink.status, direct.status);
			assert.equal(viaLink.stderr, direct.stderr);
		} finally {
			rmSync(temporary, { recursive: true, force: true });
		}
	});

	it("fails dead and expired jobs and refuses a live duplicate fingerprint", () => {
		const temporary = mkdtempSync(join(tmpdir(), "flow-adv-lifecycle-"));
		const repository = join(temporary, "repo");
		mkdirSync(repository);
		const git = (args) =>
			execFileSync("git", args, { cwd: repository, encoding: "utf8" });
		git(["init", "-b", "main"]);
		git(["config", "user.name", "Flow Test"]);
		git(["config", "user.email", "flow-test@example.invalid"]);
		writeFileSync(join(repository, ".gitignore"), ".flow/\n");
		writeFileSync(join(repository, "reviewed.ts"), "export const value = 1;\n");
		git(["add", ".gitignore", "reviewed.ts"]);
		git(["commit", "-m", "test: seed repository"]);
		const reviews = join(repository, ".flow", "reviews");
		mkdirSync(reviews, { recursive: true });
		const writeJob = (id, state, launcher, request = {}) => {
			const jobDir = join(reviews, id);
			mkdirSync(jobDir);
			writeFileSync(
				join(jobDir, "state.json"),
				JSON.stringify({ job_id: id, ...state }),
			);
			writeFileSync(join(jobDir, "launcher.json"), JSON.stringify(launcher));
			writeFileSync(
				join(jobDir, "request.json"),
				JSON.stringify({ job_id: id, ...request }),
			);
		};
		const status = (id) =>
			JSON.parse(
				execFileSync(process.execPath, [runner, "status", id], {
					cwd: repository,
					encoding: "utf8",
				}),
			);
		try {
			writeJob(
				"dead",
				{ status: "running", deadline_at: "2999-01-01T00:00:00.000Z" },
				{ pid: 2_147_483_647 },
			);
			const dead = status("dead");
			assert.equal(dead.status, "failed");
			assert.match(dead.error, /worker is no longer alive/);

			writeJob(
				"expired",
				{ status: "queued", deadline_at: "2000-01-01T00:00:00.000Z" },
				{ pid: 2_147_483_647 },
			);
			const expired = status("expired");
			assert.equal(expired.status, "failed");
			assert.match(expired.error, /deadline expired/);

			const target = { mode: "branch", baseRef: "main" };
			const fingerprint = targetFingerprint(repository, target);
			writeJob(
				"live",
				{ status: "running", deadline_at: "2999-01-01T00:00:00.000Z" },
				{ pid: process.pid },
				{ fingerprint },
			);
			const duplicate = spawnSync(
				process.execPath,
				[
					runner,
					"start",
					"--caller",
					"codex",
					"--scope",
					"branch",
					"--base",
					"main",
				],
				{ cwd: repository, encoding: "utf8" },
			);
			assert.equal(duplicate.status, 1);
			assert.match(duplicate.stderr, /already reviews this target fingerprint/);
		} finally {
			rmSync(temporary, { recursive: true, force: true });
		}
	});

	it("refuses to start until the work folder is git-ignored", () => {
		const repository = mkdtempSync(join(tmpdir(), "flow-adv-ignore-"));
		const git = (args) =>
			execFileSync("git", args, { cwd: repository, encoding: "utf8" });
		try {
			git(["init", "-b", "main"]);
			git(["config", "user.name", "Flow Test"]);
			git(["config", "user.email", "flow-test@example.invalid"]);
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 1;\n");
			git(["add", "reviewed.ts"]);
			git(["commit", "-m", "test: seed repository"]);
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 2;\n");
			const started = spawnSync(
				process.execPath,
				[runner, "start", "--caller", "claude", "--scope", "working-tree"],
				{ cwd: repository, encoding: "utf8" },
			);
			assert.equal(started.status, 1);
			assert.match(started.stderr, /\.flow\/ must be git-ignored/);
		} finally {
			rmSync(repository, { recursive: true, force: true });
		}
	});
});
