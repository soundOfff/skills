---
title: Defer Optional Heavy Features
impact: CRITICAL
impactDescription: keeps optional code out of the initial chunk
tags: bundle, third-party, dynamic-import, code-splitting
---

## Defer Optional Heavy Features

Use a dynamic import for code the first screen does not need: document editors,
export renderers, optional analytics, and other heavy interactions that begin
after a route or user action. In a client-rendered app, the useful boundary is a
route, component, or event. In a server-rendered app, optional client-only
widgets can also load after hydration (`next/dynamic` with `ssr: false`, see
`bundle-dynamic-imports`).

Keep boot-critical integrations eager. Error tracking initializes before the
application so startup failures are captured. Authentication, route
construction, and the application shell also belong to the initial path.

**Eager optional feature:**

```tsx
import { RichSectionEditor } from "./rich-section-editor";

export function DocumentSection() {
  return <RichSectionEditor />;
}
```

**Deferred optional feature with a named export:**

```tsx
import { lazy, Suspense } from "react";

const RichSectionEditor = lazy(() =>
  import("./rich-section-editor").then((module) => ({
    default: module.RichSectionEditor,
  })),
);

export function DocumentSection() {
  return (
    <Suspense fallback={<EditorSkeleton />}>
      <RichSectionEditor />
    </Suspense>
  );
}
```

Confirm that the import creates a separate production chunk and that its
fallback preserves the established loading design. Deferral is a failure when
the feature is above the fold, creates a request waterfall, or delays error
capture.
