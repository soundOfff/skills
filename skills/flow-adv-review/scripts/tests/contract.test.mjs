import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it, mock } from "node:test";
import { runReviewCandidates, validateReview } from "../lib/contract.mjs";

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

const outputSchema = JSON.parse(
	readFileSync(
		new URL("../../schemas/review-output.schema.json", import.meta.url),
		"utf8",
	),
);

const copy = (value) => structuredClone(value);

function expectRuntimeRejection(value) {
	assert.notDeepEqual(validateReview(value), []);
}

function normalizeVerdictBranch(schema) {
	const normalized = copy(schema);
	normalized.properties.verdict.const = "verdict";
	delete normalized.properties.findings.minItems;
	delete normalized.properties.findings.maxItems;
	return normalized;
}

function outcomes(...queue) {
	return mock.fn(async () => {
		const next = queue.shift();
		if (next instanceof Error) throw next;
		return next;
	});
}

describe("adversarial review contract parity", () => {
	it("keeps provider field constraints aligned with runtime validation", () => {
		const [approveSchema, attentionSchema] =
			outputSchema.properties.review.anyOf;
		const findingSchema = attentionSchema.properties.findings.items;
		assert.deepEqual(
			normalizeVerdictBranch(approveSchema),
			normalizeVerdictBranch(attentionSchema),
		);
		assert.equal(outputSchema.additionalProperties, false);
		assert.deepEqual(outputSchema.required, ["review"]);
		assert.equal(approveSchema.additionalProperties, false);
		assert.equal(attentionSchema.additionalProperties, false);
		assert.deepEqual(attentionSchema.required, [
			"verdict",
			"summary",
			"findings",
			"next_steps",
		]);
		assert.equal(findingSchema.additionalProperties, false);
		assert.deepEqual(findingSchema.required, [
			"severity",
			"title",
			"body",
			"file",
			"line_start",
			"line_end",
			"confidence",
			"recommendation",
		]);
		assert.deepEqual(findingSchema.properties.severity.enum, [
			"critical",
			"high",
			"medium",
			"low",
		]);
		const textSchemas = [
			attentionSchema.properties.summary,
			attentionSchema.properties.next_steps.items,
			...["title", "body", "file", "recommendation"].map(
				(key) => findingSchema.properties[key],
			),
		];
		for (const schema of textSchemas) {
			assert.equal(schema.minLength, 1);
			assert.equal(new RegExp(schema.pattern).test("   "), false);
		}
		assert.equal(findingSchema.properties.line_start.type, "integer");
		assert.equal(findingSchema.properties.line_start.minimum, 1);
		assert.equal(findingSchema.properties.confidence.type, "number");
		assert.equal(findingSchema.properties.confidence.minimum, 0);
		assert.equal(findingSchema.properties.confidence.maximum, 1);
		const blankSummary = copy(blocked);
		blankSummary.summary = "   ";
		expectRuntimeRejection(blankSummary);
		for (const key of ["title", "body", "file", "recommendation"]) {
			const candidate = copy(blocked);
			candidate.findings[0][key] = "   ";
			expectRuntimeRejection(candidate);
		}
		expectRuntimeRejection({ ...blocked, verdict: "unknown" });
		expectRuntimeRejection({ ...blocked, findings: [null] });
		expectRuntimeRejection({
			...blocked,
			findings: [{ ...blocked.findings[0], line_start: 0 }],
		});
	});

	it("keeps verdict and findings invariants aligned in schema and runtime", () => {
		const [approveSchema, attentionSchema] =
			outputSchema.properties.review.anyOf;
		assert.equal(approveSchema.properties.verdict.const, "approve");
		assert.equal(approveSchema.properties.findings.maxItems, 0);
		assert.equal(attentionSchema.properties.verdict.const, "needs-attention");
		assert.equal(attentionSchema.properties.findings.minItems, 1);
		expectRuntimeRejection({ ...approved, findings: blocked.findings });
		expectRuntimeRejection({ ...blocked, findings: [] });
	});
});

describe("review candidate selection", () => {
	it("falls back after an unavailable process lane", async () => {
		const execute = outcomes(new Error("unavailable"), approved);
		const result = await runReviewCandidates({
			candidates: ["codex", "claude"],
			isAvailable: async () => true,
			execute,
		});
		assert.equal(result.harness, "claude");
		assert.equal(execute.mock.callCount(), 2);
	});

	it("accepts a schema-valid blocking verdict without fallback", async () => {
		const execute = outcomes(blocked, approved);
		const result = await runReviewCandidates({
			candidates: ["codex", "claude"],
			isAvailable: async () => true,
			execute,
		});
		assert.equal(result.review.verdict, "needs-attention");
		assert.equal(execute.mock.callCount(), 1);
	});

	it("fails closed for every parseable review-shaped schema violation", async () => {
		for (const invalid of [
			{ ...blocked, findings: [{ ...blocked.findings[0], line_end: 1 }] },
			{ ...blocked, verdict: "needs_attention" },
			{ ...approved, findings: blocked.findings },
		]) {
			const execute = outcomes(invalid, approved);
			await assert.rejects(
				runReviewCandidates({
					candidates: ["codex", "claude"],
					isAvailable: async () => true,
					execute,
				}),
				/Invalid review-shaped output/,
			);
			assert.equal(execute.mock.callCount(), 1);
		}
	});
});
