# Quote Comparison Engine Contract v0.5

Status: CONTRACT ONLY

## Purpose
Compare 2–5 PDP service quotations on normalized scope without declaring a universal "best vendor".

## Inputs
- validated RFQ
- 2–5 quote records
- quote evidence revision IDs
- comparison date

## Pipeline
1. validate RFQ and quote identity
2. classify service type
3. normalize commercial terms
4. map included/excluded deliverables
5. identify quantity/term/SLA differences
6. calculate evidence coverage
7. determine pairwise comparability
8. expose trade-offs and missing information
9. optionally compute comparable 12-month cost only where contract semantics permit

## Output states
- COMPARABLE
- PARTIALLY_COMPARABLE
- NON_COMPARABLE
- INSUFFICIENT_DATA

## Output
For every quote:
- service identity
- normalized one-time amount
- normalized recurring amount where valid
- known add-ons
- unknown-cost flags
- included deliverables
- excluded deliverables
- SLA/response terms
- evidence coverage
- comparability explanation

Across quotes:
- common scope
- material scope differences
- commercial differences
- missing-information requests
- cost comparison only for comparable components

## Prohibited
- "best vendor" badge
- quality/compliance score inferred from quote
- filling missing fields with market assumptions
- comparing training price to managed DPO service
- hiding taxes/add-ons/exclusions
- converting PARTIALLY_COMPARABLE into a single winner score
