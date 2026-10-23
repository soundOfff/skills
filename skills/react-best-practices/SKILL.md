---
name: react-best-practices
description: React and Next.js performance and code-quality rules, built on Vercel Engineering's performance set and extended with component structure, testing, and type-safety rules. Use when writing, reviewing, or refactoring React or Next.js components, hooks, data fetching, bundles, or frontend tests, or when optimizing rendering or load performance.
---

# React Best Practices

## Overview

Routing and priority guide for React and Next.js performance and quality, containing 58 rules across 11 categories. Rule files hold the detailed explanations, examples, review smells, and impact metrics.

When reviewing, these rules are evidence sources for defects that already meet the reviewer's finding bar, never a checklist to report against. A rule match without a demonstrated cost stays out of the report.

The repository's own rules and decision records win when a rule here conflicts with them.

## When to Apply

Reference these guidelines when:

- Writing new React components or Next.js pages
- Implementing data fetching, on the client or the server
- Reviewing code for performance issues
- Refactoring existing React code
- Optimizing bundle size or load times
- Writing or reviewing frontend tests

## Priority-Ordered Guidelines

Rules are prioritized by impact:

| Priority | Category                  | Impact                        | Prefix       |
| -------- | ------------------------- | ----------------------------- | ------------ |
| 1        | Eliminating Waterfalls    | CRITICAL                      | `async-`     |
| 2        | Bundle Size Optimization  | CRITICAL                      | `bundle-`    |
| 3        | Server-Side Performance   | HIGH                          | `server-`    |
| 4        | Client-Side Data Fetching | MEDIUM-HIGH                   | `client-`    |
| 5        | Re-render Optimization    | MEDIUM                        | `rerender-`  |
| 6        | Rendering Performance     | MEDIUM                        | `rendering-` |
| 7        | JavaScript Performance    | LOW-MEDIUM                    | `js-`        |
| 8        | Advanced Patterns         | LOW                           | `advanced-`  |
| 9        | Component Structure       | MEDIUM-HIGH (maintainability) | `structure-` |
| 10       | Testing                   | MEDIUM-HIGH (correctness)     | `testing-`   |
| 11       | Type Safety               | HIGH                          | `types-`     |

## Quick Reference

### Critical Patterns (Apply First)

**Eliminate Waterfalls:**

- Use `Promise.all()` for independent async operations (`async-parallel`)
- Move `await` into the branches that use the result (`async-defer-await`)
- Start independent work early in API routes and Server Actions, and await it late (`async-api-routes`)
- Use `better-all` for operations with partial dependencies (`async-dependencies`)
- Use Suspense boundaries to stream content instead of awaiting before render (`async-suspense-boundaries`)

**Reduce Bundle Size:**

- Avoid barrel file imports, import directly from source (`bundle-barrel-imports`)
- Defer optional heavy UI and third-party features. Keep error tracking and
  boot-critical integrations eager (`bundle-defer-third-party`)
- Lazy-load heavy components with `next/dynamic` (`bundle-dynamic-imports`)
- Load large data or modules only when a feature activates (`bundle-conditional`)
- Preload heavy bundles on user intent (`bundle-preload`)

### High-Impact Server Patterns

- Use `React.cache()` for per-request deduplication (`server-cache-react`)
- Use an LRU cache for cross-request caching (`server-cache-lru`)
- Pass only the fields the client uses across RSC boundaries (`server-serialization`)
- Parallelize server data fetching with component composition (`server-parallel-fetching`)

### Medium-Impact Patterns

**Client-Side Data Fetching:**

- Read server data through a query cache such as TanStack Query or SWR for
  automatic request deduplication (`client-request-dedupe`)
- Narrow dependent query params at the caller or use `skipToken`. Never invent a
  fake id to satisfy a query (`client-request-dedupe`)
- Share global event listeners across component instances (`client-event-listeners`)

**Re-render Optimization:**

- Use lazy state initialization for expensive values (`rerender-lazy-state-init`)
- Apply `startTransition` for non-urgent updates (`rerender-transitions`)
- Keep UI handlers plain. Use Effect Events only for effect-fired logic (`rerender-useeffect-function-calls`)
- Never reset state with `useEffect`. Lift the discriminant and remount the branch (`rerender-no-useeffect-state-reset`)
- Add `useMemo` or `useCallback` only for measured expensive work or a consumer
  that requires stable identity (`rerender-evidence-based-memoization`)
- Never call `setState` during render or inside `useEffect`. Derive during render or move state ownership to an intermediate component (`rerender-no-setstate-in-render-or-effect`)
- Read search params or storage inside the callback that uses them instead of subscribing (`rerender-defer-reads`)
- Use primitive effect dependencies instead of objects (`rerender-dependencies`)
- Subscribe to derived booleans instead of continuous values (`rerender-derived-state`)
- Extract expensive work into a child component so an early return skips it (`rerender-memo`)

**Component Structure:**

- One domain component or hook per file, one responsibility each. Split bloated components (`structure-single-responsibility`)
- Keep component, hook, function, and utility APIs narrow. Split oversized props, arguments, and return objects into focused units composed at the component level. Wrapping the same values in one object is not a fix (`structure-narrow-apis`)
- Use PascalCase components for JSX-returning helpers. Keep lowercase helpers for non-JSX values (`structure-component-naming`)
- Derive props and params instead of accepting a value computable from another argument (`structure-derive-dont-duplicate`)
- Extract complex derived logic into named locals plus predicates or pure helpers with early returns. Oversized conditions, nested ternaries, fallback chains, and `let`-based render prep are code smells (`structure-complex-derived-logic`)
- Pick the view with early `if` guards but keep the layout wrapper in one place. Branch a body component instead of a ternary or a duplicated shell (`structure-early-return-render-branches`)
- For a fixed set of items, write one component per item with explicit props that owns its data and loading. Don't map a config-object array onto a component shape (`structure-composition-over-config`)

**Testing:**

- Test public behavior through the repository's real module seams. Render
  components with their real providers, call the real data-access surface and
  server operations, and use end-to-end tests for critical full-stack journeys.
  Mock only the boundary the test deliberately excludes (`testing-public-seams`)
- Avoid class-name assertions for visual behavior. Prefer computed styles, user-visible behavior, or browser validation, and prefer no test over a className-only implementation mirror (`testing-no-classname-assertions`)

**Type Safety:**

- Validate untrusted data before asserting a domain type. Prefer schemas, guards,
  generics, typed factories, `satisfies`, or `implements`. Assertions require a
  narrow, evidenced boundary (`types-proven-assertions`)
- Preserve the owning contract's absence sentinel. Use optional or `undefined` for
  optional inputs, retain intentional `null` in schemas or domain state, and
  normalize once at a mismatched boundary (`types-consistent-absence`)

### Rendering Patterns

- Animate SVG wrappers, not SVG elements directly (`rendering-animate-svg-wrapper`)
- Use `content-visibility: auto` for long lists (`rendering-content-visibility`)
- Hoist static JSX out of components (`rendering-hoist-jsx`)
- Reduce SVG coordinate precision (`rendering-svg-precision`)
- Prevent hydration mismatch without flicker by running an inline script before hydration (`rendering-hydration-no-flicker`)
- Use `<Activity>` to preserve state and DOM for frequently toggled UI (`rendering-activity`)
- Use an explicit ternary instead of `&&` when the condition can render a falsy value such as `0` (`rendering-conditional-render`)

### JavaScript Patterns

- Use Set/Map for repeated lookups (`js-set-map-lookups`)
- Build index maps instead of repeated `.find()` calls by the same key (`js-index-maps`)
- Use `toSorted()` instead of `sort()` for immutability (`js-tosorted-immutable`)
- Early length check for array comparisons (`js-length-check-first`)
- Return early once the result is known (`js-early-exit`)
- Batch DOM CSS changes through classes or `cssText` (`js-batch-dom-css`)
- Cache repeated function calls, property access in loops, and storage reads (`js-cache-function-results`, `js-cache-property-access`, `js-cache-storage`)
- Combine multiple array iterations into one loop (`js-combine-iterations`)
- Hoist RegExp creation out of render (`js-hoist-regexp`)
- Use a single loop, not a sort, for min and max (`js-min-max-loop`)

### Advanced Patterns

- On React versions without `useEffectEvent`, keep effect-fired callbacks in refs so subscriptions stay stable (`advanced-event-handler-refs`, `advanced-use-latest`)

## References

Rule files are the canonical source for detailed guidance and examples:

- `references/rules/` - Canonical individual rule files organized by category

Load only the relevant rule file when implementing or reviewing a specific
pattern. The quick reference above is the rule index.

To look up a specific pattern, search the rules directory:

```
rg -l "Promise.all" references/rules/
rg -l "barrel" references/rules/
rg -l "skipToken" references/rules/
```

## Rule Categories in `references/rules/`

- `async-*` - Waterfall elimination (5 rules)
- `bundle-*` - Bundle size optimization (5 rules)
- `server-*` - Server-side performance (4 rules)
- `client-*` - Client-side data fetching (2 rules)
- `rerender-*` - Re-render optimization (10 rules)
- `rendering-*` - DOM rendering performance (7 rules)
- `js-*` - JavaScript micro-optimizations (12 rules)
- `advanced-*` - Ref patterns for React versions without Effect Events (2 rules)
- `structure-*` - Component, hook, function, and utility structure (7 rules)
- `testing-*` - Public-seam tests and no className implementation-mirror assertions (2 rules)
- `types-*` - Type safety at assertion and absence boundaries (2 rules)
