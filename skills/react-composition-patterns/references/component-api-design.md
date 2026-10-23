# Component API Design

## Distinguish attributes from modes

Boolean props are appropriate when they represent independent attributes such
as `disabled`, `required`, or `readOnly`. They are a design smell when several
booleans choose mutually exclusive experiences, layouts, or action sets.

Avoid APIs that admit contradictory combinations:

```tsx
<ItemEditor creating editing readOnly />
```

Give materially different experiences explicit names:

```tsx
<CreateItemEditor collectionId={collectionId} />
<EditItemEditor itemId={itemId} />
<ReadOnlyItemView itemId={itemId} />
```

Each variant should own its required inputs and assemble shared internal parts.
Do not copy entire implementations merely to avoid a boolean; extract a shared
part only when it has a coherent responsibility.

Use a discriminated union when one component remains the clearest public API
but its modes require different data:

```tsx
type ItemEditorProps =
  | { mode: 'create'; collectionId: string }
  | { mode: 'edit'; itemId: string }
```

This keeps impossible prop combinations out of the type system. If rendering
still becomes a long mode switch, move the branches into named variant
components.

## Prefer children for caller-owned structure

Use `children` or named child components when the caller owns static structure:

```tsx
function EditorFooter({ children }: { children: React.ReactNode }) {
  return <footer>{children}</footer>
}

function EditItemEditor() {
  return (
    <EditorFrame>
      <EditorInput />
      <EditorFooter>
        <CancelButton />
        <SaveButton />
      </EditorFooter>
    </EditorFrame>
  )
}
```

Use a render callback when the component must provide scoped data or behavior
to the caller:

```tsx
<ResultList
  items={results}
  renderItem={(result) => <ResultRow result={result} />}
/>
```

Do not convert a useful data-bearing callback into context merely to eliminate
a render prop.

## Review checks

- Can the API represent contradictory modes?
- Does a prop control structure that the caller could compose directly?
- Does each explicit variant reveal its required inputs and available actions?
- Is shared code extracted around a stable responsibility rather than visual
  coincidence?
- Are native boolean attributes still passed to the underlying element?
