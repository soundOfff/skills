import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, it } from "node:test";
import { collectReviewContext, targetFingerprint } from "../lib/git.mjs";

function temporaryRepository(prefix) {
	const repository = mkdtempSync(join(tmpdir(), prefix));
	const git = (args) =>
		execFileSync("git", args, { cwd: repository, encoding: "utf8" });
	git(["init", "-b", "main"]);
	git(["config", "user.name", "Flow Test"]);
	git(["config", "user.email", "flow-test@example.invalid"]);
	return { repository, git };
}

describe("bounded review evidence", () => {
	it("collects multi-file diffs instead of asking the reviewer to run Git", () => {
		const { repository, git } = temporaryRepository("flow-adv-context-");
		try {
			for (const name of ["one.ts", "two.ts", "three.ts"]) {
				writeFileSync(join(repository, name), "export const value = 1;\n");
			}
			git(["add", "."]);
			git(["commit", "-m", "test: seed repository"]);
			for (const name of ["one.ts", "two.ts", "three.ts"]) {
				writeFileSync(join(repository, name), "export const value = 2;\n");
			}
			const context = collectReviewContext(repository, {
				mode: "working-tree",
				label: "working tree diff",
			});
			assert.equal(context.inputMode, "bounded-diff");
			assert.ok(context.content.includes("diff --git a/one.ts b/one.ts"));
			assert.ok(context.content.includes("diff --git a/three.ts b/three.ts"));
			assert.ok(!context.guidance.includes("git"));
		} finally {
			rmSync(repository, { recursive: true, force: true });
		}
	});

	it("fails explicitly when a safe bounded target cannot be supplied", () => {
		const { repository, git } = temporaryRepository("flow-adv-bounds-");
		try {
			writeFileSync(join(repository, "seed.ts"), "export {};\n");
			git(["add", "."]);
			git(["commit", "-m", "test: seed repository"]);
			writeFileSync(join(repository, "large.txt"), "x".repeat(128 * 1024 + 1));
			assert.throws(
				() =>
					collectReviewContext(repository, {
						mode: "working-tree",
						label: "working tree diff",
					}),
				/Cannot safely collect review evidence/,
			);
		} finally {
			rmSync(repository, { recursive: true, force: true });
		}
	});
});

describe("target freshness", () => {
	it("invalidates branch evidence when tracked or untracked state changes", () => {
		const { repository, git } = temporaryRepository("flow-adv-fingerprint-");
		try {
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 1;\n");
			git(["add", "reviewed.ts"]);
			git(["commit", "-m", "test: seed repository"]);
			const target = { mode: "branch", baseRef: "main" };
			const clean = targetFingerprint(repository, target);
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 2;\n");
			const unstaged = targetFingerprint(repository, target);
			git(["add", "reviewed.ts"]);
			const staged = targetFingerprint(repository, target);
			writeFileSync(join(repository, "untracked.ts"), "export {};\n");
			const untracked = targetFingerprint(repository, target);
			assert.equal(new Set([clean, unstaged, staged, untracked]).size, 4);
		} finally {
			rmSync(repository, { recursive: true, force: true });
		}
	});
});
