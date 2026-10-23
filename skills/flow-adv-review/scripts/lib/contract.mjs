export function validateReview(review) {
	const errors = [];
	const exactKeys = (value, expected, label) => {
		if (!value || typeof value !== "object" || Array.isArray(value)) {
			errors.push(`${label} must be an object`);
			return;
		}
		const actual = Object.keys(value).sort();
		if (actual.join("|") !== [...expected].sort().join("|")) {
			errors.push(`${label} has invalid fields`);
		}
	};
	exactKeys(
		review,
		["verdict", "summary", "findings", "next_steps"],
		"review",
	);
	if (!review || typeof review !== "object") return errors;
	if (!["approve", "needs-attention"].includes(review.verdict)) {
		errors.push("invalid verdict");
	}
	if (typeof review.summary !== "string" || !review.summary.trim()) {
		errors.push("summary is required");
	}
	if (!Array.isArray(review.findings)) errors.push("findings must be an array");
	if (
		!Array.isArray(review.next_steps) ||
		review.next_steps.some(
			(step) => typeof step !== "string" || !step.trim(),
		)
	) {
		errors.push("next_steps must contain non-empty strings");
	}
	const findings = Array.isArray(review.findings) ? review.findings : [];
	for (const [index, finding] of findings.entries()) {
		exactKeys(
			finding,
			[
				"severity",
				"title",
				"body",
				"file",
				"line_start",
				"line_end",
				"confidence",
				"recommendation",
			],
			`finding ${index}`,
		);
		if (!finding || typeof finding !== "object" || Array.isArray(finding)) {
			continue;
		}
		if (!["critical", "high", "medium", "low"].includes(finding.severity)) {
			errors.push(`finding ${index}: invalid severity`);
		}
		for (const key of ["title", "body", "file", "recommendation"]) {
			if (typeof finding[key] !== "string" || !finding[key].trim()) {
				errors.push(`finding ${index}: ${key} is required`);
			}
		}
		if (!Number.isInteger(finding.line_start) || finding.line_start < 1) {
			errors.push(`finding ${index}: invalid line_start`);
		}
		if (
			!Number.isInteger(finding.line_end) ||
			finding.line_end < finding.line_start
		) {
			errors.push(`finding ${index}: invalid line_end`);
		}
		if (
			typeof finding.confidence !== "number" ||
			finding.confidence < 0 ||
			finding.confidence > 1
		) {
			errors.push(`finding ${index}: invalid confidence`);
		}
	}
	if (review.verdict === "approve" && findings.length > 0) {
		errors.push("approve cannot contain findings");
	}
	if (review.verdict === "needs-attention" && findings.length === 0) {
		errors.push("needs-attention requires a finding");
	}
	return errors;
}

export const attemptError = (error) =>
	String(error?.message ?? error).replace(/\s+/g, " ").slice(0, 1000);

function isReviewShaped(value) {
	return (
		value &&
		typeof value === "object" &&
		!Array.isArray(value) &&
		["verdict", "summary", "findings", "next_steps"].some((key) =>
			Object.hasOwn(value, key),
		)
	);
}

export async function runReviewCandidates(options) {
	const attempts = [];
	for (const harness of options.candidates) {
		if (!(await options.isAvailable(harness))) {
			attempts.push({ harness, status: "unavailable" });
			continue;
		}
		let review;
		try {
			review = await options.execute(harness, attempts.length + 1);
		} catch (error) {
			attempts.push({
				harness,
				status: "failed",
				error: attemptError(error),
			});
			continue;
		}
		const errors = validateReview(review);
		if (errors.length) {
			const error = `Invalid structured review: ${errors.join("; ")}`;
			attempts.push({ harness, status: "failed", error });
			if (isReviewShaped(review)) {
				throw Object.assign(
					new Error(
						`Invalid review-shaped output from ${harness}: ${errors.join("; ")}`,
					),
					{ attempts },
				);
			}
			continue;
		}
		attempts.push({ harness, status: "completed" });
		return { harness, review, attempts };
	}
	throw Object.assign(
		new Error("No review harness produced a valid result."),
		{ attempts },
	);
}
