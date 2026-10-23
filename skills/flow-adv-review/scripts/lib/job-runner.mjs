import { join } from "node:path";
import process from "node:process";
import {
	harnessAvailable,
	harnessIsolationEvidence,
} from "./adapters.mjs";
import { attemptError, runReviewCandidates } from "./contract.mjs";
import {
	collectReviewContext,
	resolveReviewTarget,
	targetFingerprint,
} from "./git.mjs";
import { executeHarness } from "./harness-execution.mjs";
import {
	now,
	readJson,
	statePath,
	updateState,
	writeJson,
} from "./job-store.mjs";
import { buildPrompt } from "./prompt.mjs";
import { candidateOrder, reviewIndependence } from "./routing.mjs";

export async function runJob(jobDir) {
	const request = readJson(join(jobDir, "request.json"));
	if (readJson(statePath(jobDir)).status === "failed") return;
	updateState(jobDir, { status: "running", started_at: now() });
	try {
		const target = resolveReviewTarget(request.cwd, {
			base: request.base,
			scope: request.scope,
		});
		const context = collectReviewContext(request.cwd, target);
		if (request.fingerprint && request.fingerprint !== context.fingerprint) {
			throw new Error("The review target changed before the worker collected it.");
		}
		const prompt = buildPrompt(context, request.focus);
		const candidates = candidateOrder(request.caller, request.harness);
		const completed = await runReviewCandidates({
			candidates,
			isAvailable: async (harness) => harnessAvailable(harness),
			execute: async (harness, attempt) =>
				executeHarness(harness, context, prompt, jobDir, attempt),
		});
		if (targetFingerprint(context.repoRoot, target) !== context.fingerprint) {
			throw Object.assign(
				new Error("The reviewed target changed while the review was running."),
				{ attempts: completed.attempts },
			);
		}
		if (readJson(statePath(jobDir)).status === "failed") return;
		const result = {
			job_id: request.job_id,
			status: "completed",
			caller_harness: request.caller,
			requested_harness: request.harness,
			reviewer_harness: completed.harness,
			...reviewIndependence(request.caller, completed.harness, candidates[0]),
			target: {
				...target,
				fingerprint: context.fingerprint,
				...context.metadata,
			},
			input_mode: context.inputMode,
			reviewer_isolation: harnessIsolationEvidence(completed.harness),
			attempts: completed.attempts,
			review: completed.review,
			completed_at: now(),
		};
		writeJson(join(jobDir, "result.json"), result);
		updateState(jobDir, {
			status: "completed",
			completed_at: result.completed_at,
		});
	} catch (error) {
		if (readJson(statePath(jobDir)).status === "failed") return;
		const failure = {
			status: "failed",
			error: attemptError(error),
			attempts: error.attempts ?? [],
			completed_at: now(),
		};
		writeJson(join(jobDir, "failure.json"), failure);
		updateState(jobDir, failure);
		process.exitCode = 1;
	}
}
