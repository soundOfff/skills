import {
	existsSync,
	readFileSync,
	readdirSync,
	renameSync,
	writeFileSync,
} from "node:fs";
import { join, resolve, sep } from "node:path";
import process from "node:process";

export const now = () => new Date().toISOString();

export function writeJson(path, value) {
	const temporary = `${path}.${process.pid}.tmp`;
	writeFileSync(temporary, `${JSON.stringify(value, null, 2)}\n`);
	renameSync(temporary, path);
}

export const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));
export const statePath = (jobDir) => join(jobDir, "state.json");
export const reviewRoot = (root) => join(root, ".flow", "reviews");

export function updateState(jobDir, patch) {
	const path = statePath(jobDir);
	const previous = existsSync(path) ? readJson(path) : {};
	writeJson(path, { ...previous, ...patch, updated_at: now() });
}

function resolveJobDir(root, reference) {
	const base = reviewRoot(root);
	const path = resolve(base, reference);
	if (path !== base && !path.startsWith(`${base}${sep}`)) {
		throw new Error("Invalid job reference.");
	}
	return path;
}

function processIsAlive(pid) {
	if (!Number.isInteger(pid) || pid <= 0) return false;
	try {
		process.kill(pid, 0);
		return true;
	} catch (error) {
		return error?.code === "EPERM";
	}
}

function failDetachedJob(jobDir, error) {
	const state = readJson(statePath(jobDir));
	const failure = {
		status: "failed",
		error,
		attempts: state.attempts ?? [],
		completed_at: now(),
	};
	writeJson(join(jobDir, "failure.json"), failure);
	updateState(jobDir, failure);
	return readJson(statePath(jobDir));
}

export function reconcileJob(jobDir) {
	const state = readJson(statePath(jobDir));
	if (!["queued", "running"].includes(state.status)) return state;
	const deadline = Date.parse(state.deadline_at ?? "");
	if (!Number.isFinite(deadline) || deadline <= Date.now()) {
		return failDetachedJob(jobDir, "The review job deadline expired.");
	}
	const launcherPath = join(jobDir, "launcher.json");
	const launcher = existsSync(launcherPath) ? readJson(launcherPath) : {};
	if (!processIsAlive(launcher.pid)) {
		return failDetachedJob(
			jobDir,
			"The detached review worker is no longer alive.",
		);
	}
	return state;
}

export function assertNoLiveDuplicate(root, fingerprint) {
	const base = reviewRoot(root);
	if (!existsSync(base)) return;
	for (const entry of readdirSync(base, { withFileTypes: true })) {
		if (!entry.isDirectory()) continue;
		const jobDir = join(base, entry.name);
		const requestPath = join(jobDir, "request.json");
		if (!existsSync(requestPath) || !existsSync(statePath(jobDir))) continue;
		const state = reconcileJob(jobDir);
		const request = readJson(requestPath);
		if (
			["queued", "running"].includes(state.status) &&
			request.fingerprint === fingerprint
		) {
			throw new Error(
				`Review job ${request.job_id ?? entry.name} already reviews this target fingerprint.`,
			);
		}
	}
}

export function getJob(root, reference) {
	const jobDir = resolveJobDir(root, reference);
	if (!existsSync(statePath(jobDir))) {
		throw new Error(`Unknown review job: ${reference}`);
	}
	return { jobDir, state: reconcileJob(jobDir) };
}
