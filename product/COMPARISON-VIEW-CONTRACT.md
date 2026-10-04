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


## Numeric suppression boundary
Engine numeric fields are raw/derived quote facts, not permission to compare them.
- If cost state is BLOCKED, pairwise cells MUST NOT render side-by-side contract cost, delta, percentage difference, rank, or cheaper/more-expensive language.
- Individual quote detail may show its own stated amount with tax/travel/term/freshness context.
- Pairwise numeric display is permitted only when costComparable=true.
- Annualized run-rate must be labelled separately from contract commitment and must never substitute for blocked contract cost.

## Reason-code completeness gate
Every non-COMPARABLE scope state, BLOCKED cost state, STALE/UNKNOWN freshness state, and material difference must have at least one deterministic reason code. Empty reason-code output in any such state is a product error and must fail closed.


## Mapper evidence boundary
The deterministic mapper may emit a reason code only when the supplied quote records or engine result prove that condition. It must not infer FX failure, provider independence, revision identity, or bundled-component state when those facts are absent from its input contract. Unsupported reasons remain reserved until their evidence is wired into the mapper.
