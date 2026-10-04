# Quote Engine Reference v0.6

Deterministic reference model for the v0.5 contract.

This is not a production pricing engine. It exists to make core invariants executable before UI work.

Current implemented invariants:
- no double counting when total is all-in
- unknown amount semantics blocks derived total
- different service types are non-comparable
- differing included scope becomes partial comparison
- pairwise state symmetry

Next gate: expand fixtures until the v0.5 adversarial suite is represented, then freeze the model before UI.
