# Diagnosis branch

Read the complete [`diagnose`](../diagnose/SKILL.md) skill and use its
tight-loop discipline to make the bug understandable.

Begin with the reported symptom, what the current evidence establishes, and
the first repository seam to inspect. Gather available logs, tests, code paths,
and reproduction signals before requesting developer input. Ask for a runtime
observation only when it exists solely in the developer's environment and is
required for the next probe.

Tracked repository paths remain read-only. Temporary probes use an OS temporary
directory. When the developer requested a persistent session, durable fixtures
and harnesses may live under `.flow/help/<slug>/scratch/`. A regression test or
implementation edit belongs in the delivery handoff.

At every checkpoint, explain:

- the symptom and the signal that detects it;
- what new evidence changed the working model;
- which hypotheses remain and why;
- the next most informative probe.

A confirmed cause requires the red-capable loop, minimized reproduction,
falsifiable hypothesis, and probe evidence required by `diagnose`. Until all
four exist, label the cause `unconfirmed`.

Completion: the developer receives the current causal model, its evidence, and
the next proof required. Developer input is awaited only when that proof cannot
be gathered from the repository or local environment.
