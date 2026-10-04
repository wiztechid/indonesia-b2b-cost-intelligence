# Runtime/API Contract v0.9

## Purpose
Expose the frozen comparison product through a transport-neutral runtime boundary without duplicating engine, mapper, validation, or presenter logic.

## Request
A comparison request contains exactly:
- `comparisonDate`: optional ISO date string. Omitted or null is permitted but must fail closed for current-cost comparison.
- `quotes`: array of 2–5 canonical Quote Record objects.

Unknown top-level request fields are rejected.

## Processing
The runtime adapter MUST call:
`present_matrix(quotes, compare, comparisonDate)`

It MUST NOT:
- read or expose raw `contractCosts` or `annualizedRunRates` except through presenter output;
- recalculate cost, freshness, FX, scope, reason codes, or commercial relationship effects;
- rank vendors or add best/recommended/cheapest/safest/compliant labels;
- impute missing values.

## Success response
A success response contains:
- `ok: true`
- `data`: exactly the presenter-safe matrix result.

## Error response
A rejected request contains:
- `ok: false`
- `error.code`: stable machine-readable code
- `error.message`: safe human-readable message

Initial codes:
- `INVALID_REQUEST`: malformed envelope or unknown top-level field.
- `INVALID_QUOTE`: canonical quote validation failure.
- `INVALID_COMPARISON_SET`: quote count, duplicate quoteId, or pair identity failure.

Errors MUST NOT include stack traces or raw internal exception objects.

## Deployment neutrality
v0.9 defines behavior, not hosting. A Python HTTP adapter may reuse the reference implementation directly. A future static/JavaScript implementation requires parity against the same golden fixtures before it can be considered equivalent.
