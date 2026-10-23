import assert from "node:assert/strict";
import { EventEmitter } from "node:events";
import { PassThrough } from "node:stream";
import { describe, it } from "node:test";
import { assertSuccessfulProcess } from "../lib/harness-execution.mjs";
import { runProcess } from "../lib/process.mjs";

class FakeChild extends EventEmitter {
	stdout = new PassThrough();
	stderr = new PassThrough();
	stdin = new PassThrough();
	signals = [];

	kill(signal) {
		this.signals.push(signal);
		return true;
	}
}

describe("review process deadline", () => {
	it("captures an early stdin close without crashing the runner", async () => {
		const child = new FakeChild();
		const resultPromise = runProcess("reviewer", [], {
			spawnChild: () => child,
		});
		child.stdin.emit(
			"error",
			Object.assign(new Error("write EPIPE"), { code: "EPIPE" }),
		);
		child.stderr.end("reviewer rejected its invocation");
		await new Promise((resolve) => setImmediate(resolve));
		child.emit("close", 1, null);

		const result = await resultPromise;
		assert.equal(result.code, 1);
		assert.equal(result.stdinError, "write EPIPE");
		assert.equal(result.stderr, "reviewer rejected its invocation");
	});

	it("rejects a zero-exit review when prompt delivery failed", () => {
		assert.throws(
			() =>
				assertSuccessfulProcess("claude", {
					code: 0,
					signal: null,
					overflow: false,
					stdinError: "write EPIPE",
					stdout: '{"review":{"verdict":"approve"}}',
					stderr: "",
				}),
			/claude prompt delivery failed: write EPIPE/,
		);
	});

	it("escalates a timed-out child from SIGTERM to SIGKILL", async (t) => {
		t.mock.timers.enable({ apis: ["setTimeout"] });
		const child = new FakeChild();
		const resultPromise = runProcess("reviewer", [], {
			timeout: 100,
			killGrace: 25,
			spawnChild: () => child,
		});
		t.mock.timers.tick(100);
		assert.deepEqual(child.signals, ["SIGTERM"]);
		t.mock.timers.tick(25);
		assert.deepEqual(child.signals, ["SIGTERM", "SIGKILL"]);
		child.emit("close", null, "SIGKILL");
		const result = await resultPromise;
		assert.equal(result.signal, "SIGKILL");
	});
});
