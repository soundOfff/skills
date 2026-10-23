# Compound Components and Shared State

Use compound components when a family of related parts must be rearranged or
selected by the caller while sharing one stateful contract. A fixed component
with a few ordinary props does not need this pattern.

## Define a narrow domain contract

Context should expose what descendants can do, not whether the implementation
uses local state, an external store, or another source.

```tsx
type EditorContextValue = {
  value: string
  setValue: (value: string) => void
  submit: () => void
  inputRef: React.RefObject<HTMLInputElement | null>
}

const EditorContext = React.createContext<EditorContextValue | undefined>(
  undefined,
)

function useEditor() {
  const context = React.use(EditorContext)

  if (context === undefined) {
    throw new Error('Editor parts must be rendered inside Editor.Root')
  }

  return context
}
```

Failing at the boundary produces a useful error instead of a later null access.
Keep the hook and context private unless consumers truly need the raw contract.

## Put shared ownership above every consumer

```tsx
function EditorRoot({ children }: { children: React.ReactNode }) {
  const [value, setValue] = React.useState('')
  const inputRef = React.useRef<HTMLInputElement>(null)

  const submit = () => {
    // Invoke the feature's submit capability with the current value.
  }

  return (
    <EditorContext value={{ value, setValue, submit, inputRef }}>
      {children}
    </EditorContext>
  )
}

function EditorFrame({ children }: { children: React.ReactNode }) {
  const { submit } = useEditor()

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault()
        submit()
      }}
    >
      {children}
    </form>
  )
}

function EditorInput() {
  const { value, setValue, inputRef } = useEditor()

  return (
    <input
      ref={inputRef}
      value={value}
      onChange={(event) => setValue(event.currentTarget.value)}
    />
  )
}

function EditorSubmit() {
  return <button type="submit">Save</button>
}

export const Editor = {
  Root: EditorRoot,
  Frame: EditorFrame,
  Input: EditorInput,
  Submit: EditorSubmit,
}
```

The provider may wrap a larger feature surface than the visible editor. That
is useful when a preview or dialog action needs the same value. It should not
wrap unrelated application regions or become a general-purpose state bucket.

If the owner receives state and capabilities from above, keep the same context
contract and adapt them once in `EditorRoot`. Descendants should not import
the storage-specific hook themselves.

## Preserve platform behavior

The structural root should carry the correct native semantics. If composition
represents a form, use a form and its submit event instead of replacing it with
click-only behavior. Preserve labels, keyboard operation, focus order, disabled
states, and error relationships as parts move.

## Verification

Test behavior through representative public compositions:

- each supported variant renders its intended parts;
- shared actions observe the current state;
- keyboard and form submission still work;
- a part outside the provider fails with the deliberate boundary error;
- two provider instances do not leak state into each other.
