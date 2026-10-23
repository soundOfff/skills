import { spawn, spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import {
	closeSync,
	mkdirSync,
	openSync,
	readFileSync,
	writeFileSync,
} from "node:fs";
import { join, relative } from "node:path";
import process from "node:process";
import {
	repoRoot,
	resolveReviewTarget,
	targetFingerprint,
} from "./git.mjs";
import {
	assertNoLiveDuplicate,
	getJob,
	now,
	reviewRoot,
	writeJson,
} from "./job-store.mjs";
import { sanitizeChildEnv } from "./process.mjs";
import { candidateOrder } from "./routing.mjs";

const SCOPES = new Set(["auto", "working-tree", "branch"]);
const JOB_TIMEOUT_MS = 100 * 60 * 1000;

function ensureFlowStateIsIgnored(root) {
	const ignored = spawnSync(
		"git",
		["check-ignore", "--quiet", ".flow/reviews/flow-adv-review"],
		{ cwd: root },
	);
	if (ignored.status !== 0) {
		throw new Error(
			".flow/ must be git-ignored before starting an adversarial review.",
		);
	}
}

export function startJob(options, runnerPath) {
	const root = repoRoot(options.cwd ?? process.cwd());
	ensureFlowStateIsIgnored(root);
	const caller = options.caller ?? "unknown";
	const harness = options.harness ?? "auto";
	const scope = options.scope ?? "auto";
	if (!SCOPES.has(scope)) throw new Error(`Unsupported scope: ${scope}`);
	candidateOrder(caller, harness);
	const target = resolveReviewTarget(root, {
		base: options.base,
		scope,
	});
	const fingerprint = targetFingerprint(root, target);
	mkdirSync(reviewRoot(root), { recursive: true });
	assertNoLiveDuplicate(root, fingerprint);
	const jobId = `${new Date()
		.toISOString()
		.replace(/[-:.]/g, "")
		.slice(0, 15)}-${randomBytes(4).toString("hex")}`;
	const jobDir = join(reviewRoot(root), jobId);
	mkdirSync(jobDir, { recursive: true });
	const createdAt = now();
	const deadlineAt = new Date(Date.now() + JOB_TIMEOUT_MS).toISOString();
	const request = {
		job_id: jobId,
		cwd: root,
		caller,
		harness,
		scope,
		base: options.base ?? null,
		focus: options.focus ?? "",
		fingerprint,
		created_at: createdAt,
		deadline_at: deadlineAt,
	};
	writeJson(join(jobDir, "request.json"), request);
	writeJson(join(jobDir, "state.json"), {
		job_id: jobId,
		status: "queued",
		created_at: request.created_at,
		deadline_at: deadlineAt,
	});
	const stdout = openSync(join(jobDir, "worker.log"), "a");
	const stderr = openSync(join(jobDir, "worker.log"), "a");
	const child = spawn(
		process.execPath,
		[runnerPath, "worker", "--job-dir", jobDir],
		{
			cwd: root,
			detached: true,
			env: sanitizeChildEnv(),
			stdio: ["ignore", stdout, stderr],
		},
	);
	child.unref();
	closeSync(stdout);
	closeSync(stderr);
	writeJson(join(jobDir, "launcher.json"), {
		pid: child.pid,
		launched_at: now(),
	});
	return {
		job_id: jobId,
		status: "queued",
		job_dir: relative(root, jobDir),
	};
}

export function outputJob(command, options) {
	const root = repoRoot(options.cwd ?? process.cwd());
	const reference = options.positionals[0];
	if (!reference) throw new Error(`${command} requires a job id`);
	const job = getJob(root, reference);
	if (command === "status") return job.state;
	if (job.state.status === "completed") {
		const result = JSON.parse(
			readFileSync(join(job.jobDir, "result.json"), "utf8"),
		);
		const current = targetFingerprint(root, result.target);
		if (current !== result.target.fingerprint) {
			process.exitCode = 4;
			return {
				...result,
				status: "stale",
				error: "The reviewed target has changed.",
			};
		}
		return result;
	}
	if (job.state.status === "failed") {
		process.exitCode = 2;
		return JSON.parse(
			readFileSync(join(job.jobDir, "failure.json"), "utf8"),
		);
	}
	process.exitCode = 3;
	return job.state;
}
