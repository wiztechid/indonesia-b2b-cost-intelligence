# MVP Comparison Interface v0.8

## Flow
1. Capture RFQ context.
2. Add 2–5 quote records.
3. Validate records before comparison.
4. Run deterministic pairwise engine.
5. Map engine output through product mapper.
6. Render only presenter output.
7. Show missing-information actions for blocked states.

## Sacred boundary
Public UI MUST NOT consume raw engine contractCosts or annualizedRunRates.
It consumes product/presenter.py output only. Presenter emits numeric pairwise values only when the mapper permits comparison.

## Matrix
For N quotes, render N*(N-1)/2 pairwise results. Do not collapse them into a universal vendor score.

## No-winner policy
No best/recommended/cheapest/safest/compliant vendor badges. Scope, freshness, evidence and cost states remain separate.

## Input limit
MVP accepts 2–5 quotes. Fewer or more fail closed.
