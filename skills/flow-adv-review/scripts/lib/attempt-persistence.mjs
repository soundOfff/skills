import { existsSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import process from "node:process";

export function persistRawAttempt(
	jobDir,
	attempt,
	harness,
	result,
	codexOutputPath,
) {
	const output = existsSync(codexOutputPath)
		? readFileSync(codexOutputPath, "utf8")
		: null;
	const path = join(
		jobDir,
		`attempt-${String(attempt).padStart(2, "0")}-${harness}-raw.json`,
	);
	const temporary = `${path}.${process.pid}.tmp`;
	const raw = { harness, ...result, structured_output: output };
	writeFileSync(temporary, `${JSON.stringify(raw)}\n`, { mode: 0o600 });
	renameSync(temporary, path);
}
