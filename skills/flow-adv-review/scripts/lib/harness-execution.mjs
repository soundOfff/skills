import { join } from "node:path";
import {
	buildHarnessInvocation,
	parseHarnessReview,
} from "./adapters.mjs";
import { persistRawAttempt } from "./attempt-persistence.mjs";
import { attemptError } from "./contract.mjs";
import { runProcess } from "./process.mjs";

export function assertSuccessfulProcess(harness, result) {
	if (result.stdinError) {
		throw new Error(`${harness} prompt delivery failed: ${result.stdinError}`);
	}
	if (result.code === 0 && !result.overflow) return;
	const failure = result.stderr.trim() || "no diagnostic output";
	throw new Error(
		`${harness} exited ${result.code ?? result.signal}: ${
			result.overflow ? "output limit exceeded" : failure.slice(0, 2000)
		}`,
	);
}

export async function executeHarness(
	harness,
	context,
	prompt,
	jobDir,
	attempt = 1,
) {
	const codexOutputPath = join(
		jobDir,
		`attempt-${String(attempt).padStart(2, "0")}-codex-output.json`,
	);
	const invocation = buildHarnessInvocation(harness, {
		repoRoot: context.repoRoot,
		prompt,
		codexOutputPath,
	});
	let result;
	try {
		result = await runProcess(invocation.command, invocation.args, {
			cwd: context.repoRoot,
			stdin: invocation.stdin,
		});
	} catch (error) {
		persistRawAttempt(
			jobDir,
			attempt,
			harness,
			{ error: attemptError(error), stdout: "", stderr: "" },
			codexOutputPath,
		);
		throw error;
	}
	persistRawAttempt(jobDir, attempt, harness, result, codexOutputPath);
	assertSuccessfulProcess(harness, result);
	return parseHarnessReview(harness, result.stdout, codexOutputPath);
}
