import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { buildPrompt } from "../lib/prompt.mjs";

describe("adversarial review prompt", () => {
	it("embeds the complete schema, target evidence, and verdict invariants", () => {
		const prompt = buildPrompt(
			{
				repoRoot: "/repo",
				branch: "feature",
				inputMode: "bounded-diff",
				content: "immutable diff",
				guidance: "inspect only the supplied evidence",
				target: { label: "working tree" },
			},
			"focus",
		);
		assert.ok(prompt.includes('"severity"'));
		assert.ok(prompt.includes('"next_steps"'));
		assert.ok(prompt.includes('"review"'));
		assert.ok(prompt.includes("immutable diff"));
		assert.ok(prompt.includes("`approve` requires an empty `findings` array"));
		assert.ok(
			prompt.includes("`needs-attention` requires at least one finding"),
		);
	});
});
