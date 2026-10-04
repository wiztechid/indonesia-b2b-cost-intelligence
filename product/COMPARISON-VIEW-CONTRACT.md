# Comparison View Contract v0.7

## Purpose
Translate deterministic engine output into buyer-facing information without inventing a winner.

## Required layers
1. Quote identity and freshness
2. Scope comparability
3. Cost comparability
4. Material differences
5. Missing information
6. Commercial relationship disclosure

## Pairwise matrix
Every pair must expose:
- scope state: COMPARABLE | PARTIALLY_COMPARABLE | NON_COMPARABLE | INSUFFICIENT_DATA
- cost state: COMPARABLE | BLOCKED
- freshness: CURRENT | STALE | UNKNOWN
- common deliverables
- material differences
- reason codes

## Display rules
- Never collapse scope state and cost state into one score.
- Never label a vendor best, recommended, cheapest, safest, or most compliant from quote data alone.
- A lower displayed cost must retain scope/exclusion/term context.
- STALE or UNKNOWN freshness blocks current-cost comparison.
- Missing information is shown as an action request, not silently imputed.
- Affiliate/sponsor/lead relationships are disclosed but do not alter comparison math.
