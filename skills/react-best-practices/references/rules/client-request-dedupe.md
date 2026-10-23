---
title: Read Server Data Through a Query Cache
impact: MEDIUM-HIGH
impactDescription: shared cache, request deduplication, and owned loading states
tags: client, tanstack-query, swr, deduplication, data-fetching
---

## Read Server Data Through a Query Cache

Components read server data through the repository's query cache library, such
as TanStack Query or SWR, never through a hand-rolled `useEffect` fetch. Every
instance that reads the same key shares one request, one cache entry, and one
loading state. Wrap each data source in query options owned by its feature.
Query keys include every owning id so cache entries cannot bleed across
accounts, records, or sessions.

**Direct request from a component:**

```tsx
export function OrderPage({ orderId }: { orderId: string }) {
  const [order, setOrder] = useState<Order>();
  useEffect(() => {
    getOrder(orderId).then(setOrder);
  }, [orderId]);
  return <OrderSummary order={order} />;
}
```

**Query-owned request:**

```tsx
export function OrderPage({ orderId }: { orderId: string }) {
  const { data: order } = useSuspenseQuery(orderQueries.detail(orderId));
  return <OrderSummary order={order} />;
}
```

With SWR the same component reads `useSWR(["orders", orderId], fetchOrder)`.

Narrow a required id before rendering the component that owns the query. For a
component that must remain mounted while an id is absent, accept the owning
contract's optional form and use `skipToken` (a `null` key in SWR):

```tsx
import { skipToken, useQuery } from "@tanstack/react-query";

export function useOrder(orderId?: string) {
  return useQuery({
    queryKey: ["orders", "detail", orderId],
    queryFn: orderId ? () => getOrder(orderId) : skipToken,
  });
}
```

Never pass `id ?? ""`, a sentinel UUID, or a non-null assertion to manufacture
a query key. Preserve an intentional `null` contract at its boundary, but
normalize it before an API that accepts only `string | undefined`.

Mutations invalidate the affected key by default. Use optimistic writes only
when the interaction requires them and rollback behavior is proved.
