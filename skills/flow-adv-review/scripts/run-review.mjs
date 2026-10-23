#!/usr/bin/env node

import { resolve } from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { attemptError } from "./lib/contract.mjs";
import { outputJob, startJob } from "./lib/job-lifecycle.mjs";
import { runJob } from "./lib/job-runner.mjs";

const SCRIPT_PATH = fileURLToPath(import.meta.url);

function parseOptions(args) {
	const options = { positionals: [] };
	for (let index = 0; index < args.length; index++) {
		const token = args[index];
		if (!token.startsWith("--")) {
			options.positionals.push(token);
			continue;
		}
		const key = token
			.slice(2)
			.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
		const value = args[index + 1];
		if (value == null) throw new Error(`${token} requires a value`);
		options[key] = value;
		index++;
	}
	return options;
}

const print = (value) =>
	process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);

async function main() {
	const [command, ...rest] = process.argv.slice(2);
	const options = parseOptions(rest);
	if (command === "start") {
		print(startJob(options, SCRIPT_PATH));
		return;
	}
	if (command === "worker") {
		await runJob(options.jobDir);
		return;
	}
	if (command === "status" || command === "result") {
		print(outputJob(command, options));
		return;
	}
	throw new Error(
		"Usage: run-review.mjs start|status|result [--caller <harness>] [--harness <harness>] [--scope <scope>] [--base <ref>] [--focus <text>]",
	);
}

if (resolve(process.argv[1] ?? "") === SCRIPT_PATH) {
	main().catch((error) => {
		process.stderr.write(`${attemptError(error)}\n`);
		process.exitCode = 1;
	});
}
