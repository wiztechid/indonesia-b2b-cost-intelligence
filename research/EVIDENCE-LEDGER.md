# Evidence Ledger Contract v0.1

This file defines the minimum record. Actual evidence entries should be structured data later.

Required fields:
- evidence_id
- topic
- claim
- source_url
- source_name
- source_authority: official | court | regulator | vendor | consultancy | publisher | other
- evidence_class: law | judicial_decision | advertised_price | vendor_quote | estimate | methodology | market_context
- observed_value
- currency
- unit
- scope
- published_at
- issued_at
- effective_at
- checked_at
- status
- notes

Rules:
1. Never convert a single vendor advertised price into a market range.
2. Preserve tax, setup, recurring, user/asset, scope and term assumptions.
3. Historical observations remain immutable; corrections append a new revision.
4. Regulatory evidence records issuance/publication and effectiveness separately.
5. Calculator inputs may reference only evidence IDs that pass the applicable gate.
