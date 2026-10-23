## Classification contract

This contract is the single source of truth for reuse classes. The Reuse Auditor applies it, and `/flow-create` and `/flow-build` enforce it.

- `REUSE`: name the existing interface, the invariant, and the test evidence.
- `EXTEND`: name the owning interface, the affected callers, and the tests that must change.
- `NEW`: record both searches, the rejected candidates, why none owns the behavior, and a destination consistent with the repository's structure.
- `REMOVE`: name the callers, the migration impact, and the obsolete tests or docs.

Similarity is not proof. A class holds only when the evidence shows matching semantics, invariants, and lifecycle.
