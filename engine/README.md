# Quote Engine Reference v0.6

Deterministic reference model for the v0.5 contract. This is not a production pricing engine.

## Executable coverage
- double-count protection via amount semantics
- contract commitment vs annualized run-rate separation
- irregular recurring-term fail-closed behavior
- empty/no-common scope handling
- service-type and quantity-limit comparability
- pairwise state/cost symmetry
- quote staleness
- provider independence and evidence-revision identity
- FX provenance and same-currency idempotence
- tax/travel completeness gate on pairwise cost comparison
- commercial relationship as disclosure only
- bundled component price only when explicitly supplied

## Freeze boundary
v0.6 is a deterministic reference model, not production pricing and not a vendor-ranking system. Public UI must not infer missing costs, legal compliance, service quality, or a universal winner.

Status: READY FOR FREEZE after PR audit/merge.
