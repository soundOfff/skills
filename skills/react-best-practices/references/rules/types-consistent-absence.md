---
title: Keep Absence Contracts Consistent
impact: MEDIUM
impactDescription: prevents mixed sentinels and fake fallback values
tags: types, null, undefined, optional, boundaries
---

## Keep Absence Contracts Consistent

Use the absence value owned by the domain or API contract. Optional parameters
and properties normally use `?`/`undefined`; persisted schemas and state machines
may intentionally use `null` when absence is a real, serializable state. React's
`return null` remains the standard no-render result.

Normalize once when two boundaries disagree. Do not widen every layer to
`T | null | undefined`, and do not manufacture a fake string, object, or id to
avoid narrowing.

Keep leaf components strict when their UI requires a value. The caller owns the
missing-value branch and renders the leaf only after the value is present.

**Mixed sentinels leaking through layers:**

```tsx
type ProductCardProps = { product?: Product | null };
const selected = products.find((product) => product.id === selectedId) ?? null;
return <ProductCard product={selected ?? undefined} />;
```

**One owner, one contract:**

```tsx
type ProductCardProps = { product: Product };
const selected = products.find((product) => product.id === selectedId);
return selected ? <ProductCard product={selected} /> : <EmptySelection />;
```

When a validation schema, database column, or external API defines `null`, keep that
meaning explicit or convert it in a named adapter:

```ts
function optionalPhotoUrl(value: string | null): string | undefined {
  return value ?? undefined;
}
```

## Review smells

- One value travels through both `null` and `undefined` without distinct meaning.
- A fake fallback makes an invalid query, route, or mutation look valid.
- A leaf component accepts absence only to render a generic fallback owned by
  its caller.
- A change rewrites an established public sentinel without updating its schema,
  callers, persistence, and tests.
