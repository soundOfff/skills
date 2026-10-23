import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import {
	chmodSync,
	existsSync,
	mkdirSync,
	mkdtempSync,
	readdirSync,
	readFileSync,
	rmSync,
	statSync,
	writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import { targetFingerprint } from "../lib/git.mjs";

const runner = fileURLToPath(new URL("../run-review.mjs", import.meta.url));

const approved = {
	verdict: "approve",
	summary: "No material risk found.",
	findings: [],
	next_steps: [],
};

describe("adversarial review worker integration", () => {
	it(
		"persists bounded evidence, attempt data, and reviewer isolation metadata",
		{ timeout: 90_000 },
		async () => {
			const temporary = mkdtempSync(join(tmpdir(), "flow-adv-review-"));
			const repository = join(temporary, "repo");
			const binaries = join(temporary, "bin");
			mkdirSync(repository);
			mkdirSync(binaries);
			const git = (args) =>
				execFileSync("git", args, { cwd: repository, encoding: "utf8" });
			git(["init", "-b", "main"]);
			git(["config", "user.name", "Flow Test"]);
			git(["config", "user.email", "flow-test@example.invalid"]);
			writeFileSync(join(repository, ".gitignore"), ".flow/\n");
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 1;\n");
			git(["add", ".gitignore", "reviewed.ts"]);
			git(["commit", "-m", "test: seed repository"]);
			writeFileSync(join(repository, "reviewed.ts"), "export const value = 2;\n");

			const codex = join(binaries, "codex");
			writeFileSync(codex, "#!/bin/sh\nexit 1\n");
			chmodSync(codex, 0o755);
			const claude = join(binaries, "claude");
			writeFileSync(
				claude,
				`#!/bin/sh
if [ "$1" = "auth" ]; then
  printf '%s\\n' '{"loggedIn":true}'
  exit 0
fi
cat >/dev/null
printf '%s\\n' '${JSON.stringify({ structured_output: approved })}'
`,
			);
			chmodSync(claude, 0o755);
			try {
				const env = { ...process.env, PATH: `${binaries}:${process.env.PATH}` };
				const started = JSON.parse(
					execFileSync(
						process.execPath,
						[
							runner,
							"start",
							"--caller",
							"claude",
							"--harness",
							"auto",
							"--scope",
							"working-tree",
							"--focus",
							"challenge the change",
						],
						{ cwd: repository, encoding: "utf8", env },
					),
				);
				const jobDir = join(repository, ".flow", "reviews", started.job_id);
				const statePath = join(jobDir, "state.json");
				const deadline = Date.now() + 60_000;
				while (Date.now() < deadline) {
					if (existsSync(statePath)) {
						const state = JSON.parse(readFileSync(statePath, "utf8"));
						if (state.status === "completed" || state.status === "failed") break;
					}
					await new Promise((resolve) => setTimeout(resolve, 25));
				}
				const result = JSON.parse(
					execFileSync(process.execPath, [runner, "result", started.job_id], {
						cwd: repository,
						encoding: "utf8",
						env,
					}),
				);
				assert.equal(result.reviewer_harness, "claude");
				assert.equal(result.same_harness_fallback, true);
				assert.equal(result.input_mode, "bounded-diff");
				assert.deepEqual(result.review, approved);
				assert.equal(
					result.reviewer_isolation.customizations,
					"disabled-by-safe-mode",
				);
				assert.equal(result.reviewer_isolation.instruction_source, "runner-only");
				assert.equal(result.reviewer_isolation.tool_access, "none");
				assert.equal(
					result.reviewer_isolation.target_evidence,
					"runner-collected-bounded",
				);
				assert.equal(
					result.target.fingerprint,
					targetFingerprint(repository, result.target),
				);
				assert.ok(!readdirSync(jobDir).some((name) => name.endsWith(".patch")));
				const rawAttempt = readdirSync(jobDir).find((name) =>
					name.endsWith("-claude-raw.json"),
				);
				assert.ok(rawAttempt);
				const rawPath = join(jobDir, rawAttempt);
				assert.equal(statSync(rawPath).mode & 0o777, 0o600);
				const raw = JSON.parse(readFileSync(rawPath, "utf8"));
				assert.equal(raw.harness, "claude");
				assert.match(raw.stdout, /structured_output/);
				writeFileSync(join(repository, "reviewed.ts"), "export const value = 3;\n");
				assert.notEqual(
					targetFingerprint(repository, result.target),
					result.target.fingerprint,
				);
			} finally {
				rmSync(temporary, { recursive: true, force: true });
			}
		},
	);
});
