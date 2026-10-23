---
name: domain-modeling
description: Build and sharpen a project's domain model. Challenge ambiguous terms against scenarios and code, settle vocabulary in the repository's glossary, and record a settled architectural decision. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model.
---

# Domain Modeling

Actively sharpen the model. Challenge ambiguous language, test it against
concrete scenarios and current code, then capture only settled outcomes in the
repository's existing authorities.

## 1. Open the domain authority

Read `docs/agents/domain.md` when it exists. It names where domain language
lives (a `CONTEXT.md` or a glossary file), where decision records live, the ADR
threshold, and how ADR numbers are assigned. Without it, use the default layout
in [`CONTEXT-FORMAT.md`](CONTEXT-FORMAT.md): a root `CONTEXT.md`, or a
`CONTEXT-MAP.md` that points to one `CONTEXT.md` per context, with ADRs in
`docs/adr/`.

Read the vocabulary owner, the relevant ADRs, and the code and tests that
implement the discussed concepts. Keep exactly one vocabulary owner. When the
repository already has a glossary file, never add a `CONTEXT.md` beside it.

Completion: every term and decision in scope has an identified authority or is
explicitly marked unresolved.

## 2. Stress the model

For each ambiguous or conflicting term:

- name the competing meanings and their practical consequence;
- propose one precise project term;
- walk through concrete normal and edge-case scenarios;
- check whether current models, schemas, flows, and tests agree;
- distinguish a vocabulary gap from an implementation defect.

Ask the human only for the domain decision that evidence cannot make. Resolve
discoverable code and documentation facts first.

Completion: each in-scope term has one meaning, boundary, relationship, and
relevant avoided synonym, or one bounded human decision remains.

## 3. Capture settled vocabulary

Update the vocabulary owner as soon as a term settles. Do not batch the updates
to the end of the session. Follow the owner's existing structure, or
[`CONTEXT-FORMAT.md`](CONTEXT-FORMAT.md) for a `CONTEXT.md`. Create the file
only when the first term settles. Record domain meaning rather than
implementation detail. Update affected terms together so relationships and
avoided synonyms cannot drift across entries.

Completion: every settled vocabulary change appears once in the vocabulary
owner and agrees with the session's examples and boundaries.

## 4. Capture architectural decisions sparingly

An ADR is warranted only when the decision is hard to reverse, surprising
without context, and the result of a real tradeoff. The threshold in
`docs/agents/domain.md` wins when it differs. Use [`ADR-FORMAT.md`](ADR-FORMAT.md).

A coordinating caller supplies a reserved ADR number. When a coordinating skill
dispatched you without one, record the candidate decision and rationale in the
active `.flow/` artifact and return `ADR reservation required`. Leave the ADR
folder unchanged. When the developer invoked this skill directly, you are the
coordinator and assign the number per [`ADR-FORMAT.md`](ADR-FORMAT.md). A
changed accepted decision creates a new superseding ADR.

Completion: the decision remains in the active artifact, or one correctly
numbered, threshold-qualified ADR captures the settled tradeoff and
supersession effects.
