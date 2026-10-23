---
title: Memoize Only for Evidence or Identity Contracts
impact: MEDIUM
impactDescription: avoids speculative caches while preserving required stable identities
tags: rerender, useMemo, useCallback, memoization, profiler
---

## Memoize Only for Evidence or Identity Contracts

Derive values and define event handlers directly during render by default.
`useMemo` and `useCallback` add a cache contract, dependency maintenance, and
stale-closure risk; they earn that cost in two cases:

1. profiler evidence shows a materially expensive calculation on the actual
   workload; or
2. a real consumer requires stable identity, such as a memoized child or a Hook
   whose subscription depends on the callback.

Record the consumer or measurement in the change. Referential equality used as
application semantics is a design smell; move that state or identity contract
to a clearer owner.

**Speculative memoization:**

```tsx
const visibleProducts = useMemo(
  () => products.filter((product) => product.name.includes(query)),
  [products, query],
);
const handleSelect = useCallback((product: Product) => selectProduct(product.id), []);
```

**Default derivation:**

```tsx
const visibleProducts = products.filter((product) => product.name.includes(query));
function handleSelect(product: Product) {
  selectProduct(product.id);
}
```

If logic runs only from an Effect and must read the latest props or state, use
`useEffectEvent` instead of memoizing it. For expensive initialization needed
once per mount, use lazy `useState`.

## Review smells

- A new memo has no named consumer or profiler result.
- Memoization compensates for a component owning unrelated responsibilities.
- Dependency arrays restate a large calculation or hide stale values.
- `useCallback` exists only to satisfy an Effect dependency that should use an
  Effect Event or a different subscription boundary.
