---
title: Prove Type Assertions at Boundaries
impact: HIGH
impactDescription: prevents unchecked domain-shape claims while allowing narrow framework adapters
tags: types, typescript, assertions, schemas, type-guards, test-quality
---

## Prove Type Assertions at Boundaries

An `as` assertion does not validate runtime data. Untrusted JSON, model output,
storage, URL state, and external API payloads must cross a schema or a guard
that proves the fields the code uses.

Prefer:

- schema parsing (Zod, Valibot, or the repository's validator) for domain payloads;
- type guards for small discriminated shapes;
- generic DOM/query APIs such as `getByRole<HTMLTextAreaElement>`;
- typed factories or annotated locals for fixtures;
- `satisfies` when a value should retain inference;
- `implements` for test doubles.

An assertion is acceptable at a narrow framework boundary when TypeScript
cannot express a fact the runtime or test setup establishes. Keep it local,
avoid double assertions, and attach proof through a preceding runtime check or
a focused adapter test. `as const` is narrowing and remains appropriate.

**Unchecked domain claim:**

```ts
const order = JSON.parse(payload) as Order;
```

**Validated domain boundary:**

```ts
const order = OrderSchema.parse(JSON.parse(payload));
```

**Typed test surfaces:**

```tsx
const title = screen.getByRole<HTMLInputElement>("textbox", {
  name: "Order title",
});

const fixture = {
  id: "order-1",
  status: "draft",
} satisfies Pick<Order, "id" | "status">;
```

## Review smells

- `as unknown as T`, `as any`, or an assertion directly after parsing untrusted
  data.
- A domain predicate checks only that the value is a non-null object.
- A fixture assertion hides missing required fields.
- An assertion spans multiple layers instead of living in one tested adapter.
- A cast replaces a schema that already owns the type.
