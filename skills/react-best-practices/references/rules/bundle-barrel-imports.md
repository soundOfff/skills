---
title: Avoid Barrel File Imports
impact: CRITICAL
impactDescription: limits module-graph work and preserves direct ownership
tags: bundle, imports, tree-shaking, barrel-files, performance
---

## Avoid Barrel File Imports

Import repository modules from their owning file. Local barrel files obscure
ownership, invite circular dependencies, and pull unrelated modules into the
graph. Follow the repository's structure rules when they already ban or allow
them.

For packages that expose supported per-module entrypoints, prefer those paths
when bundle or development measurements show the root entrypoint expands a
large graph. Use only package-exported paths. Never reach into an undocumented
`dist/` layout. In Next.js, `experimental.optimizePackageImports` rewrites
barrel imports from the listed packages at build time, so those imports can
stay.

**Repository barrel:**

```tsx
import { OrderSummary, useOrder } from "@/features/orders";
```

**Direct owners:**

```tsx
import { OrderSummary } from "@/features/orders/ui/order-summary";
import { useOrder } from "@/features/orders/api/order-queries";
```

A package-root import is not automatically a defect. Require an exported
subpath and measured or documented module-graph cost before changing it.
