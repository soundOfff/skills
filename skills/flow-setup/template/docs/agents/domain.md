# Domain docs

Where this repository's domain language and decision records live, and how agents use them.

## Sources

The `Domain language` and `Decisions` rows of `## Sources of truth` in `AGENTS.md` name the files. A row that reads `none` means the source does not exist yet.

- Domain language is the glossary of terms the code and the team use. When none exists, `domain-modeling` creates `CONTEXT.md` at the repository root once the first term settles. A repository with several bounded contexts keeps a root `CONTEXT-MAP.md` that points at one `CONTEXT.md` per context.
- Decisions are architectural decision records. When none exist, `domain-modeling` creates `docs/adr/` with the first record.

When a new source appears, re-run `/flow-setup` or edit its row by hand.

Before naming a domain concept in an issue, feature map, test, model, or explanation, read the glossary and the decision records that touch the area. When a source is missing, proceed without flagging it.

## Vocabulary

Use the glossary's terms, and do not drift to synonyms it avoids. A missing term is evidence to investigate, not permission to invent one. Update the glossary when a term's meaning, boundary, relationship, or avoided synonym settles. Keep implementation detail out of it.

Surface a conflict between the conversation, the code, the glossary, and the decision records. Never normalize it silently.

## ADR threshold

Record a decision only when all three hold:

1. It is hard to reverse.
2. A future reader would find it surprising without context.
3. It came from a real tradeoff between genuine alternatives.

Accepted records are append-only. A changed decision gets a new record that names the one it supersedes. When your output contradicts an accepted record, say so explicitly, as in "contradicts ADR 0007, worth reopening because ...".

## ADR numbering

Records are numbered in sequence with four digits, as in `0007-<slug>.md`. The coordinating agent reserves the next number, the highest existing number plus one, and records it in the active `.flow/` ledger before it dispatches an agent to write the record. A dispatched agent never picks a number by scanning and incrementing, because parallel agents would pick the same one.

When a decision meets the threshold and no number is reserved, capture the decision and its rationale in the active ledger, return `ADR reservation required`, and leave the decisions folder unchanged.
