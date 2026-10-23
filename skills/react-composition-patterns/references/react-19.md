# React 19 Composition APIs

## Accept refs as props

In React 19, new function components can accept `ref` directly. Do not add a
`forwardRef` wrapper solely to pass a ref through.

```tsx
type EditorInputProps = React.ComponentPropsWithRef<'input'>

function EditorInput({ ref, ...props }: EditorInputProps) {
  return <input ref={ref} {...props} />
}
```

Keep an existing `forwardRef` component when changing it would create needless
API churn. Convert it when already editing that boundary and preserve the
ref target and imperative behavior.

## Read context with `use`

React 19 supports reading context with `use`:

```tsx
function useEditor() {
  const value = React.use(EditorContext)

  if (value === undefined) {
    throw new Error('Editor parts must be rendered inside Editor.Root')
  }

  return value
}
```

`use(Context)` can appear after an early return or inside a conditional branch.
`useContext(Context)` remains valid; do not rewrite working code unless the
change improves the surrounding API or matches an established local convention.

React 19 also permits rendering the context object itself as the provider:

```tsx
<EditorContext value={value}>{children}</EditorContext>
```

Do not apply these APIs to a codebase that has not adopted React 19.
