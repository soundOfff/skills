import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
	buildHarnessInvocation,
	harnessIsolationEvidence,
	parseHarnessReview,
} from "../lib/adapters.mjs";
import { sanitizeChildEnv } from "../lib/process.mjs";
import { candidateOrder, reviewIndependence } from "../lib/routing.mjs";

const approved = {
	verdict: "approve",
	summary: "No material risk found.",
	findings: [],
	next_steps: [],
};

const blocked = {
	verdict: "needs-attention",
	summary: "Do not ship.",
	findings: [
		{
			severity: "high",
			title: "Retry duplicates writes",
			body: "The retry path repeats the mutation without an idempotency guard.",
			file: "src/write.ts",
			line_start: 10,
			line_end: 12,
			confidence: 0.9,
			recommendation: "Add an idempotency key.",
		},
	],
	next_steps: ["Repair and rerun the review."],
};

const invocationOptions = {
	repoRoot: "/repo",
	prompt: "review",
	codexOutputPath: "/tmp/result.json",
};

function assertIncludesAll(values, expected) {
	for (const value of expected) {
		assert.ok(values.includes(value), `missing ${JSON.stringify(value)}`);
	}
}

describe("adversarial harness routing", () => {
	it("prefers the opposite harness and falls back to a fresh caller", () => {
		assert.deepEqual(candidateOrder("claude"), ["codex", "claude"]);
		assert.deepEqual(candidateOrder("codex"), ["claude", "codex"]);
	});

	it("honors an explicit reviewer before caller fallback", () => {
		assert.deepEqual(candidateOrder("claude", "codex"), ["codex", "claude"]);
		assert.deepEqual(candidateOrder("codex", "codex"), ["codex"]);
	});

	it("rejects unsupported callers and marks unknown independence unverified", () => {
		assert.throws(() => candidateOrder("vim"), /Unsupported caller: vim/);
		assert.throws(() => candidateOrder("cursor"), /Unsupported caller: cursor/);
		assert.throws(() => candidateOrder("claude", "cursor"), /Unsupported harness: cursor/);
		assert.deepEqual(candidateOrder("unknown"), ["codex", "claude"]);
		assert.deepEqual(reviewIndependence("unknown", "codex", "codex"), {
			cross_harness: null,
			same_harness_fallback: null,
			model_independence: "unverified",
		});
	});

	it("removes parent-session identifiers without removing auth homes", () => {
		const env = sanitizeChildEnv({
			CLAUDECODE: "1",
			CODEX_THREAD_ID: "thread",
			CODEX_HOME: "/codex",
			ANTHROPIC_API_KEY: "secret",
		});
		assert.equal(env.CLAUDECODE, undefined);
		assert.equal(env.CODEX_THREAD_ID, undefined);
		assert.equal(env.CODEX_HOME, "/codex");
		assert.equal(env.ANTHROPIC_API_KEY, "secret");
	});
});

describe("fresh review adapters", () => {
	it("starts Codex ephemerally in a read-only sandbox", () => {
		const invocation = buildHarnessInvocation("codex", invocationOptions);
		assertIncludesAll(invocation.args, ["--ephemeral", "--sandbox", "read-only"]);
		assert.ok(!invocation.args.includes("resume"));
	});

	it("keeps the reviewed repository's instructions out of the Codex reviewer", () => {
		const invocation = buildHarnessInvocation("codex", invocationOptions);
		assertIncludesAll(invocation.args, ["--ignore-user-config", "--ignore-rules", "project_doc_max_bytes=0"]);
		const isolation = harnessIsolationEvidence("codex");
		assert.equal(isolation.customizations, "user-config-rules-and-project-docs-ignored");
		assert.equal(isolation.instruction_source, "runner-plus-codex-defaults");
		assert.throws(() => harnessIsolationEvidence("cursor"), /Unsupported harness: cursor/);
	});

	it("starts Claude with only runner instructions and no tool access", () => {
		const invocation = buildHarnessInvocation("claude", invocationOptions);
		assertIncludesAll(invocation.args, [
			"--safe-mode",
			"--no-session-persistence",
			"--permission-mode",
			"plan",
			"--disable-slash-commands",
			"--system-prompt",
		]);
		const toolsIndex = invocation.args.indexOf("--tools");
		const mcpIndex = invocation.args.indexOf("--mcp-config");
		assert.ok(toolsIndex > -1);
		assert.equal(invocation.args[toolsIndex + 1], "");
		assert.deepEqual(JSON.parse(invocation.args[mcpIndex + 1]), {
			mcpServers: {},
		});
		assert.ok(!invocation.args.includes("--setting-sources"));
		assert.ok(!invocation.args.join(" ").includes("Bash"));
		assert.ok(!invocation.args.includes("--continue"));
		assert.ok(!invocation.args.includes("--resume"));
		const isolation = harnessIsolationEvidence("claude");
		assert.equal(isolation.customizations, "disabled-by-safe-mode");
		assert.equal(isolation.instruction_source, "runner-only");
		assert.equal(isolation.tool_access, "none");
		assert.equal(isolation.target_evidence, "runner-collected-bounded");
	});

	it("uses the same Claude-compatible schema across the prompt and adapter", () => {
		const invocation = buildHarnessInvocation("claude", invocationOptions);
		const schemaIndex = invocation.args.indexOf("--json-schema") + 1;
		assert.ok(schemaIndex > 0);
		const schema = JSON.parse(invocation.args[schemaIndex]);
		assert.ok(!Object.hasOwn(schema, "$schema"));
		assert.deepEqual(schema.required, ["review"]);
		assert.equal(schema.properties.review.anyOf.length, 2);
	});

	it("parses direct and wrapped harness responses", () => {
		assert.deepEqual(
			parseHarnessReview("codex", JSON.stringify(approved), "/missing"),
			approved,
		);
		assert.deepEqual(
			parseHarnessReview(
				"claude",
				JSON.stringify({ structured_output: { review: blocked } }),
				"/missing",
			),
			blocked,
		);
		assert.deepEqual(
			parseHarnessReview(
				"claude",
				JSON.stringify([
					{ type: "system", subtype: "init" },
					{ type: "assistant", message: { content: [] } },
					{
						type: "result",
						subtype: "success",
						result: JSON.stringify({ review: approved }),
						structured_output: { review: blocked },
					},
				]),
				"/missing",
			),
			blocked,
		);
		assert.deepEqual(
			parseHarnessReview(
				"claude",
				JSON.stringify({ result: JSON.stringify({ review: approved }) }),
				"/missing",
			),
			approved,
		);
	});
});
