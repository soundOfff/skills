export const HARNESSES = new Set(["codex", "claude"]);
export const CALLERS = new Set([...HARNESSES, "unknown"]);

export function candidateOrder(caller, requested = "auto") {
	if (!CALLERS.has(caller)) throw new Error(`Unsupported caller: ${caller}`);
	if (requested !== "auto") {
		if (!HARNESSES.has(requested)) {
			throw new Error(`Unsupported harness: ${requested}`);
		}
		return requested === caller || !HARNESSES.has(caller)
			? [requested]
			: [requested, caller];
	}
	if (caller === "claude") return ["codex", "claude"];
	if (caller === "codex") return ["claude", "codex"];
	return ["codex", "claude"];
}

export function reviewIndependence(caller, reviewer, preferred) {
	if (caller === "unknown") {
		return {
			cross_harness: null,
			same_harness_fallback: null,
			model_independence: "unverified",
		};
	}
	const crossHarness = reviewer !== caller;
	return {
		cross_harness: crossHarness,
		same_harness_fallback: !crossHarness && preferred !== caller,
		model_independence: crossHarness ? "cross-harness" : "same-harness",
	};
}
