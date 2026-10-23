import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const SCOPES = new Set(["auto", "working-tree", "branch"]);
const EVIDENCE_MAX_FILES = 500;
const EVIDENCE_MAX_BYTES = 2 * 1024 * 1024;
const UNTRACKED_MAX_BYTES = 128 * 1024;

function sha256(value) {
	return createHash("sha256").update(value).digest("hex");
}

function runGit(cwd, args, options = {}) {
	const result = spawnSync("git", args, {
		cwd,
		encoding: "utf8",
		maxBuffer: options.maxBuffer ?? 64 * 1024 * 1024,
	});
	if (result.error) throw result.error;
	const allowed = options.allowedStatuses ?? [0];
	if (!allowed.includes(result.status)) {
		throw new Error(
			`git ${args[0]} failed (${result.status}): ${(result.stderr || result.stdout).trim()}`,
		);
	}
	return result.stdout;
}

export function repoRoot(cwd) {
	return runGit(cwd, ["rev-parse", "--show-toplevel"]).trim();
}

function currentBranch(cwd) {
	return runGit(cwd, ["branch", "--show-current"]).trim() || "HEAD";
}

function defaultBase(cwd) {
	const symbolic = spawnSync(
		"git",
		["symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"],
		{ cwd, encoding: "utf8" },
	);
	if (symbolic.status === 0) {
		return symbolic.stdout.trim().replace("refs/remotes/", "");
	}
	for (const candidate of [
		"origin/main",
		"main",
		"origin/master",
		"master",
		"trunk",
	]) {
		const found = spawnSync(
			"git",
			["rev-parse", "--verify", "--quiet", candidate],
			{ cwd, encoding: "utf8" },
		);
		if (found.status === 0) return candidate;
	}
	throw new Error("Unable to detect a base branch; pass --base <ref>.");
}

function lines(value) {
	return value.trim() ? value.trim().split("\n").filter(Boolean) : [];
}

function workingTreeState(cwd) {
	return {
		staged: lines(runGit(cwd, ["diff", "--cached", "--name-only"])),
		unstaged: lines(runGit(cwd, ["diff", "--name-only"])),
		untracked: lines(
			runGit(cwd, ["ls-files", "--others", "--exclude-standard"]),
		),
	};
}

function hasWorkingChanges(state) {
	return state.staged.length + state.unstaged.length + state.untracked.length > 0;
}

export function resolveReviewTarget(cwd, options = {}) {
	const root = repoRoot(cwd);
	const scope = options.scope ?? "auto";
	if (!SCOPES.has(scope)) throw new Error(`Unsupported scope: ${scope}`);
	if (options.base) {
		return {
			mode: "branch",
			baseRef: options.base,
			label: `branch diff against ${options.base}`,
		};
	}
	if (scope === "working-tree") {
		return { mode: "working-tree", label: "working tree diff" };
	}
	if (scope === "branch") {
		const baseRef = defaultBase(root);
		return { mode: "branch", baseRef, label: `branch diff against ${baseRef}` };
	}
	if (hasWorkingChanges(workingTreeState(root))) {
		return { mode: "working-tree", label: "working tree diff" };
	}
	const baseRef = defaultBase(root);
	return { mode: "branch", baseRef, label: `branch diff against ${baseRef}` };
}

function section(title, body) {
	return `## ${title}\n\n${body.trim() || "(none)"}\n`;
}

function untrackedFileContext(root, path) {
	const absolute = join(root, path);
	try {
		const stat = statSync(absolute);
		if (!stat.isFile()) {
			throw new Error(`Cannot safely collect review evidence for non-file ${path}.`);
		}
		if (stat.size > UNTRACKED_MAX_BYTES) {
			throw new Error(
				`Cannot safely collect review evidence for ${path}: ${stat.size} bytes exceeds the ${UNTRACKED_MAX_BYTES} byte per-file limit.`,
			);
		}
		const content = readFileSync(absolute);
		if (content.includes(0)) {
			throw new Error(`Cannot safely collect binary review evidence for ${path}.`);
		}
		return `### ${path}\n\`\`\`\n${content.toString("utf8").trimEnd()}\n\`\`\``;
	} catch (error) {
		if (error instanceof Error && error.message.startsWith("Cannot safely")) {
			throw error;
		}
		throw new Error(`Cannot safely collect review evidence for unreadable file ${path}.`);
	}
}

function assertEvidenceBounds(changedFiles, content) {
	if (changedFiles.length > EVIDENCE_MAX_FILES) {
		throw new Error(
			`Cannot safely collect bounded review evidence: ${changedFiles.length} changed files exceeds the ${EVIDENCE_MAX_FILES} file limit.`,
		);
	}
	const bytes = Buffer.byteLength(content);
	if (bytes > EVIDENCE_MAX_BYTES) {
		throw new Error(
			`Cannot safely collect bounded review evidence: ${bytes} bytes exceeds the ${EVIDENCE_MAX_BYTES} byte limit.`,
		);
	}
}

function unique(values) {
	return [...new Set(values)].sort();
}

function branchDetails(root, target) {
	const mergeBase = runGit(root, ["merge-base", "HEAD", target.baseRef]).trim();
	const headSha = runGit(root, ["rev-parse", "HEAD"]).trim();
	const baseSha = runGit(root, ["rev-parse", target.baseRef]).trim();
	const range = `${mergeBase}..HEAD`;
	const changedFiles = lines(runGit(root, ["diff", "--name-only", range]));
	if (changedFiles.length === 0) {
		throw new Error(`No changes found in ${target.label}.`);
	}
	const log = runGit(root, ["log", "--oneline", "--decorate", range]);
	const stat = runGit(root, ["diff", "--stat", range]);
	const diff = runGit(root, ["diff", "--no-ext-diff", "--unified=80", range]);
	const content = [
		section("Commit Log", log),
		section("Diff Stat", stat),
		section("Branch Diff", diff),
	].join("\n");
	assertEvidenceBounds(changedFiles, content);
	return {
		content,
		changedFiles,
		inputMode: "bounded-diff",
		metadata: { baseSha, headSha, mergeBase, range },
	};
}

function workingTreeDetails(root) {
	const state = workingTreeState(root);
	const changedFiles = unique([
		...state.staged,
		...state.unstaged,
		...state.untracked,
	]);
	if (changedFiles.length === 0) throw new Error("No working-tree changes found.");
	const status = runGit(root, ["status", "--short", "--untracked-files=all"]);
	const stagedDiff = runGit(root, [
		"diff",
		"--cached",
		"--no-ext-diff",
		"--unified=80",
	]);
	const unstagedDiff = runGit(root, ["diff", "--no-ext-diff", "--unified=80"]);
	const untracked = state.untracked
		.map((path) => untrackedFileContext(root, path))
		.join("\n\n");
	const content = [
		section("Git Status", status),
		section("Staged Diff", stagedDiff),
		section("Unstaged Diff", unstagedDiff),
		section("Untracked Files", untracked),
	].join("\n");
	assertEvidenceBounds(changedFiles, content);
	return {
		content,
		changedFiles,
		inputMode: "bounded-diff",
		metadata: { headSha: runGit(root, ["rev-parse", "HEAD"]).trim() },
	};
}

function untrackedHashes(root, paths) {
	return paths.map((path) => [
		path,
		runGit(root, ["hash-object", "--no-filters", "--", path]).trim(),
	]);
}

function workingTreeFingerprint(root) {
	const state = workingTreeState(root);
	return {
		status: runGit(root, ["status", "--short", "--untracked-files=all"]),
		staged: runGit(root, [
			"diff",
			"--cached",
			"--binary",
			"--no-ext-diff",
		]),
		unstaged: runGit(root, ["diff", "--binary", "--no-ext-diff"]),
		untracked: untrackedHashes(root, state.untracked),
	};
}

export function targetFingerprint(root, target) {
	if (target.mode === "branch") {
		const mergeBase = runGit(root, ["merge-base", "HEAD", target.baseRef]).trim();
		return sha256(
			JSON.stringify({
				baseSha: runGit(root, ["rev-parse", target.baseRef]).trim(),
				headSha: runGit(root, ["rev-parse", "HEAD"]).trim(),
				mergeBase,
				workingTree: workingTreeFingerprint(root),
			}),
		);
	}
	return sha256(
		JSON.stringify({
			headSha: runGit(root, ["rev-parse", "HEAD"]).trim(),
			workingTree: workingTreeFingerprint(root),
		}),
	);
}

export function collectReviewContext(cwd, target) {
	const root = repoRoot(cwd);
	const details =
		target.mode === "branch"
			? branchDetails(root, target)
			: workingTreeDetails(root);
	const fingerprint = targetFingerprint(root, target);
	const guidance =
		"Use the runner-collected immutable target evidence below as the complete change set. Do not invoke external tools or collect the target yourself.";
	return {
		repoRoot: root,
		branch: currentBranch(root),
		target,
		fingerprint,
		guidance,
		...details,
	};
}
