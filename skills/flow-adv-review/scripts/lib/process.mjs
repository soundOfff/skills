import { spawn } from "node:child_process";
import process from "node:process";

const PROCESS_OUTPUT_MAX_BYTES = 5 * 1024 * 1024;
const REVIEW_TIMEOUT_MS = 30 * 60 * 1000;
const TERMINATION_GRACE_MS = 5_000;

export function sanitizeChildEnv(source = process.env) {
	const env = { ...source };
	for (const name of [
		"CLAUDECODE",
		"CLAUDE_CODE_ENTRYPOINT",
		"CLAUDE_CODE_SESSION_ID",
		"CODEX_THREAD_ID",
		"CURSOR_SESSION_ID",
	]) {
		delete env[name];
	}
	return env;
}

export function runProcess(command, args, options = {}) {
	return new Promise((resolvePromise, reject) => {
		const spawnChild = options.spawnChild ?? spawn;
		const child = spawnChild(command, args, {
			cwd: options.cwd,
			env: sanitizeChildEnv(),
			stdio: ["pipe", "pipe", "pipe"],
		});
		let stdout = Buffer.alloc(0);
		let stderr = Buffer.alloc(0);
		let overflow = false;
		let stdinError = null;
		let escalationTimer;
		let terminating = false;
		const terminate = () => {
			if (terminating) return;
			terminating = true;
			child.kill("SIGTERM");
			escalationTimer = setTimeout(
				() => child.kill("SIGKILL"),
				options.killGrace ?? TERMINATION_GRACE_MS,
			);
		};
		const timer = setTimeout(terminate, options.timeout ?? REVIEW_TIMEOUT_MS);
		const collect = (current, chunk) => {
			const next = Buffer.concat([current, chunk]);
			if (next.length > PROCESS_OUTPUT_MAX_BYTES) {
				overflow = true;
				terminate();
			}
			return next.subarray(0, PROCESS_OUTPUT_MAX_BYTES);
		};
		child.stdout.on("data", (chunk) => {
			stdout = collect(stdout, chunk);
		});
		child.stderr.on("data", (chunk) => {
			stderr = collect(stderr, chunk);
		});
		child.stdin.on("error", (error) => {
			stdinError = String(error?.message ?? error);
		});
		child.on("error", (error) => {
			clearTimeout(timer);
			clearTimeout(escalationTimer);
			reject(error);
		});
		child.on("close", (code, signal) => {
			clearTimeout(timer);
			clearTimeout(escalationTimer);
			resolvePromise({
				code,
				signal,
				overflow,
				stdinError,
				stdout: stdout.toString("utf8"),
				stderr: stderr.toString("utf8"),
			});
		});
		child.stdin.end(options.stdin ?? "");
	});
}
