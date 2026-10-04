# Quote Normalizer Contract v0.4

Goal: compare vendor quotes on equivalent scope, not merely headline price.

## Capture
For each quote record:
- vendor/source identity
- quote date and validity
- service type
- total quoted amount
- currency
- tax included/excluded
- setup/onboarding fee
- recurring fee and cadence
- contract term
- travel/on-site costs
- included deliverables
- explicit exclusions
- quantity limits
- response/SLA commitments
- remediation/retest/follow-up
- optional items
- assumptions

## Normalized outputs
- comparable base scope
- one-time cost
- recurring annualized cost
- known add-ons
- excluded-cost flags
- 12-month comparable cost when contract permits
- scope completeness score
- comparability status: comparable | partially_comparable | non_comparable

## Guardrails
- Never annualize a project-only DPIA as DPO recurring service.
- Never compare training-only or consultation-only price with end-to-end implementation.
- Never impute missing tax/travel/add-on values as zero.
- Missing material fields lower comparability; they do not become assumptions.
- Vendor ranking cannot be based on price alone.
