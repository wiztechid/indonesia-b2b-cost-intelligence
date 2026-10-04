# Missing Information Prompts v0.7

Prompts must be generated from deterministic missing fields/reason codes.

Examples:
- TAX_UNKNOWN -> Ask vendor whether quoted amount includes applicable tax.
- TRAVEL_UNKNOWN -> Ask whether travel/on-site expenses are included.
- COMPARISON_DATE_MISSING -> Set the comparison date before treating prices as current.
- QUOTE_STALE -> Request an updated quotation or validity confirmation.
- AMOUNT_SEMANTICS_UNKNOWN -> Confirm whether total includes setup and recurring components.
- FX_PROVENANCE_MISSING -> Record exchange-rate source and date before normalization.
- COMPONENT_PRICE_MISSING -> Request component-level pricing before separating a bundled service.
- QUANTITY_LIMITS_DIFFER -> Confirm comparable request/system/entity limits.

Boundary: prompts request facts. They do not recommend a vendor or infer missing values.
