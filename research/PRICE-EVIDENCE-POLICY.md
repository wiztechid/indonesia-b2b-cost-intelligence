# Price Evidence Policy v0.2

## Objective
Estimate buyer budgeting ranges without fabricating a "market price".

## Evidence classes
A. public advertised price
B. attributable vendor quotation
C. procurement/tender/contract value with comparable scope
D. independent published estimate
E. derived TCO from A-C inputs
F. anecdotal/unverifiable — discovery only, excluded from calculation

## Minimum range rule
No public "market range" from one provider.

A numeric service range requires either:
- >=3 independent comparable observations from >=3 providers/sources; or
- >=2 provider observations plus >=1 comparable procurement/contract observation.

If this threshold fails, output: INSUFFICIENT_EVIDENCE.

## Comparability dimensions
Normalize at minimum:
- service definition
- one-time vs recurring
- organization/users/assets/data subjects
- systems/apps/endpoints
- duration
- included deliverables
- retest/remediation
- tax
- travel/on-site
- certification/accreditation where relevant
- observation date

## Outliers
Never silently delete. Flag and document exclusion reason.

## Freshness
Prices older than 18 months cannot anchor a current range without corroboration. Preserve them for historical trend only.

## Independence
Multiple pages owned by one provider count as one provider observation.

## Commercial separation
Affiliate/sponsor/lead status cannot increase evidence weight.
