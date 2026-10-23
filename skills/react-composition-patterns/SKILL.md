---
name: react-composition-patterns
description: Design React 19 component APIs with composition, explicit variants, and compound components. Use when boolean props or modes multiply, or related components need one context contract.
---

# React Composition Patterns

Use the smallest composition pattern that makes valid component states obvious.
Do not introduce a compound-component API when ordinary props and `children`
already express the design clearly.

## Workflow

1. List the distinct user-facing variants and the state each one needs.
2. Separate true attributes such as `disabled` from booleans that select a
   component mode or layout.
3. Choose the narrowest suitable API:
   - ordinary props for values and independent attributes;
   - `children` and named slots for caller-owned structure;
   - explicit variant components for materially different experiences;
   - compound components plus context when several related parts share one
     stateful contract.
4. Keep state at the lowest owner that serves every consumer. Expose domain
   capabilities through context, not the storage mechanism.
5. Add tests for supported compositions and provider-boundary failures.

## Load Only What the Task Needs

- API shape, boolean-prop smells, explicit variants, and render callbacks:
  [`references/component-api-design.md`](references/component-api-design.md)
- Compound components, context contracts, state ownership, and provider
  guards: [`references/compound-components.md`](references/compound-components.md)
- Ref props and context reads in React 19:
  [`references/react-19.md`](references/react-19.md)

## Constraints

- Preserve semantic HTML, accessibility, focus behavior, and form behavior
  while changing composition.
- Prefer named components with narrow props. Do not replace one oversized API
  with a large untyped context value.
- Keep variants explicit at the feature boundary while sharing small internal
  parts where that removes real duplication.
- Treat render callbacks as a data-scoping tool, not as a default slot syntax.
- Do not mirror or synchronize the same state in multiple owners.
- Apply only React 19 behavior from this skill; routing, data fetching, styling,
  and build-system decisions belong to their own project guidance.
