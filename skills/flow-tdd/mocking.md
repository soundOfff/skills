# Test doubles

Use test doubles at system boundaries:

- external APIs;
- time and randomness;
- filesystem or databases when a deterministic local implementation is not
  available;
- network, email, payment, and other irreversible effects.

Use real repository modules between the public seam and those boundaries.
Mocking internal collaborators couples the test to the current implementation
and can let broken integration pass.

## Boundary shape

Prefer a narrow, operation-specific interface:

```typescript
type PaymentClient = {
	charge(input: ChargeInput): Promise<ChargeResult>;
};

async function processPayment(order: Order, paymentClient: PaymentClient) {
	return paymentClient.charge({ amount: order.total });
}
```

The test double returns one known shape. A generic fetcher that branches on URLs
inside the mock recreates production routing in the test and becomes a second
implementation.

## Double rules

- Inject the boundary instead of constructing it inside domain behavior.
- Return independent known values, including the failure being tested.
- Assert the seam's result; assert boundary calls only when that interaction is
  itself the public contract.
- Keep mock setup branch-free and specific to one behavior.
- Prefer the repository's existing test factory or fake over a new bespoke mock.
