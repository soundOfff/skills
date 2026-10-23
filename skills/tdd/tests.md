# Behavioral tests

## Durable seam test

```typescript
it("confirms a valid cart", async () => {
	const cart = createCart([{ price: 10 }, { price: 5 }]);
	const result = await checkout(cart, paymentMethod);

	expect(result.status).toBe("confirmed");
});
```

The test enters through a public capability, states observable behavior, and
uses a known expected result. Internal refactoring does not change the test.

## Implementation-coupled test

```typescript
it("calls the payment processor once", async () => {
	const process = vi.spyOn(paymentService, "process");
	await checkout(cart, paymentMethod);

	expect(process).toHaveBeenCalledOnce();
});
```

The call is an implementation choice. The test breaks when orchestration moves
even if checkout behavior stays correct.

## Side-channel test

```typescript
it("creates a retrievable user", async () => {
	const created = await createUser({ name: "Alice" });
	const retrieved = await getUser(created.id);

	expect(retrieved.name).toBe("Alice");
});
```

Observe through the same public system instead of reaching into its database or
private state.

## Independent expectation

```typescript
it("totals the cart", () => {
	expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

The literal comes from a worked example. Recomputing the total inside the test
would repeat the implementation and make the assertion tautological.

## Selection rules

- Prefer the nearest public seam that expresses the acceptance criterion.
- Use one logical assertion; multiple assertions are valid when they describe
  one observable result.
- Exercise the negative path when the criterion defines rejection or failure.
- Test names describe what the caller can do or observe, never which helper ran.
