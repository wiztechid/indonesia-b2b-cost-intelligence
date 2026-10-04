# Quote Engine Reference v0.6

Deterministic reference model for the v0.5 contract. This is not a production pricing engine.

## Executable now
- all-in total is not double-counted
- contract commitment cost is distinct from annualized recurring run-rate
- irregular recurring terms fail closed
- unknown amount semantics blocks derived total
- explicit empty scope remains empty and yields INSUFFICIENT_DATA
- different service types are NON_COMPARABLE
- no common deliverables are NON_COMPARABLE
- scope or quantity-limit differences are PARTIALLY_COMPARABLE
- pairwise state and cost-comparability flags are symmetric

## Still blocked before freeze
- expiry/staleness
- evidence revision lineage and provider independence
- commercial-relationship handling
- FX conversion/provenance/idempotence
- tax/travel/add-on presentation
- bundled-component handling

Freeze condition: remaining v0.5 invariants must become executable before any public comparison UI.
