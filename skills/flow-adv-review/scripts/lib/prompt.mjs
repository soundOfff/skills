import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const SKILL_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const PROMPT_PATH = join(SKILL_ROOT, "prompts", "adversarial-review.md");
const SCHEMA_PATH = join(SKILL_ROOT, "schemas", "review-output.schema.json");

function interpolate(template, values) {
	return template.replace(
		/\{\{([A-Z_]+)\}\}/g,
		(_, key) => values[key] ?? "",
	);
}

export function buildPrompt(context, focus) {
	return interpolate(readFileSync(PROMPT_PATH, "utf8"), {
		TARGET_LABEL: context.target.label,
		USER_FOCUS: focus.trim() || "No extra focus provided.",
		REVIEW_COLLECTION_GUIDANCE: context.guidance,
		OUTPUT_SCHEMA: readFileSync(SCHEMA_PATH, "utf8"),
		REVIEW_INPUT: [
			`Repository root: ${context.repoRoot}`,
			`Branch: ${context.branch}`,
			`Input mode: ${context.inputMode}`,
			context.content,
		].join("\n"),
	});
}
