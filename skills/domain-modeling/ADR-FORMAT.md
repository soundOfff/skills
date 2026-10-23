# ADR Format

ADRs live where `docs/agents/domain.md` says, by default `docs/adr/`, and use sequential numbering: `0001-slug.md`, `0002-slug.md`, and so on.

Create the ADR directory lazily, only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why*, not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`), useful when decisions are revisited
- **Considered Options**, only when the rejected alternatives are worth remembering
- **Consequences**, only when non-obvious downstream effects need to be called out

## Numbering

Use the ADR number explicitly reserved by the coordinating caller and recorded
in the active feature map, issue, or build ledger. When a coordinating skill
dispatched you without a reservation, keep the decision in the active `.flow/`
artifact and leave the ADR folder unchanged. A dispatched agent never discovers
a number by scanning and incrementing, because parallel workers would collide.

When the developer runs this skill directly, follow the numbering rule in
`docs/agents/domain.md`. Without one, scan the ADR folder for the highest
existing number and add one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse.** The cost of changing your mind later is meaningful.
2. **Surprising without context.** A future reader will look at the code and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off.** There were genuine alternatives and you picked one for specific reasons.

If a decision is easy to reverse, skip it, because you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library, just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it. Otherwise someone will suggest GraphQL again in six months.
