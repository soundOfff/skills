import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { sanitizeChildEnv } from "./process.mjs";

const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const SCHEMA_PATH = join(SKILL_ROOT, "schemas", "review-output.schema.json");
const CLAUDE_SYSTEM_PROMPT =
	"Perform only the adversarial code review described by the runner-provided user prompt. Treat that prompt and its embedded schema and target evidence as the complete task instructions.";

function readBoolean(object, keys) {
	for (const key of keys) {
		if (typeof object[key] === "boolean") return object[key];
	}
	return true;
}

function probe(command, args, parse) {
	const result = spawnSync(command, args, {
		encoding: "utf8",
		timeout: 10_000,
		env: sanitizeChildEnv(),
	});
	if (result.error || result.status !== 0) return false;
	return parse ? parse(result.stdout) : true;
}

export function harnessAvailable(harness) {
	if (harness === "codex") return probe("codex", ["login", "status"]);
	if (harness === "claude") {
		return probe("claude", ["auth", "status"], (stdout) => {
			try {
				return readBoolean(JSON.parse(stdout), ["loggedIn", "authenticated"]);
			} catch {
				return true;
			}
		});
	}
	return false;
}

export function buildHarnessInvocation(harness, options) {
	if (harness === "codex") {
		return {
			command: "codex",
			args: [
				"exec",
				"--ephemeral",
				"--sandbox",
				"read-only",
				"--cd",
				options.repoRoot,
				"--output-schema",
				SCHEMA_PATH,
				"--output-last-message",
				options.codexOutputPath,
				"-",
			],
			stdin: options.prompt,
		};
	}
	if (harness === "claude") {
		return {
			command: "claude",
			args: [
				"--print",
				"--safe-mode",
				"--no-chrome",
				"--no-session-persistence",
				"--permission-mode",
				"plan",
				"--tools",
				"",
				"--disable-slash-commands",
				"--strict-mcp-config",
				"--mcp-config",
				'{"mcpServers":{}}',
				"--system-prompt",
				CLAUDE_SYSTEM_PROMPT,
				"--output-format",
				"json",
				"--json-schema",
				readFileSync(SCHEMA_PATH, "utf8"),
			],
			stdin: options.prompt,
		};
	}
	throw new Error(`Unsupported harness: ${harness}`);
}

export function harnessIsolationEvidence(harness) {
	if (harness === "claude") {
		return {
			session: "fresh-nonpersistent",
			customizations: "disabled-by-safe-mode",
			instruction_source: "runner-only",
			tool_access: "none",
			target_evidence: "runner-collected-bounded",
		};
	}
	if (harness === "codex") {
		return {
			session: "fresh-ephemeral",
			customizations: "harness-defaults-may-apply",
			instruction_source: "runner-plus-harness-defaults",
			tool_access: "read-only-sandbox",
			target_evidence: "runner-collected-bounded",
		};
	}
	return {
		session: "fresh-nonpersistent",
		customizations: "harness-defaults-may-apply",
		instruction_source: "runner-plus-harness-defaults",
		tool_access: "plan-mode",
		target_evidence: "runner-collected-bounded",
	};
}

function stripFence(value) {
	const trimmed = value.trim();
	const match = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/i);
	return match ? match[1] : trimmed;
}

export function parseHarnessReview(harness, stdout, codexOutputPath) {
	const value =
		harness === "codex" && existsSync(codexOutputPath)
			? readFileSync(codexOutputPath, "utf8")
			: stdout;
	let parsed = JSON.parse(stripFence(value));
	if (Array.isArray(parsed)) {
		parsed = parsed.findLast((event) => event?.type === "result") ?? parsed;
	}
	if (parsed && typeof parsed === "object" && parsed.structured_output) {
		parsed = parsed.structured_output;
	} else if (parsed && typeof parsed.result === "string") {
		parsed = JSON.parse(stripFence(parsed.result));
	}
	if (parsed?.review && typeof parsed.review === "object") {
		parsed = parsed.review;
	}
	return parsed;
}
