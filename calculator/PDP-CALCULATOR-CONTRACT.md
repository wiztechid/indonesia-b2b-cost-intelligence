# PDP Compliance Cost Calculator Contract v0.1

Status: SPEC ONLY — formulas not approved.

## Goal
Produce an educational budgeting range, not a compliance determination, legal opinion, or vendor quotation.

## Candidate inputs
- organization size
- approximate data-subject scale
- data categories/risk characteristics
- number of systems
- number of material processors/vendors
- processing complexity
- DPO operating model: internal | outsourced | undecided
- DPIA workload estimate
- technical assessment needs
- training scope
- optional certification target

## Outputs
- one-time implementation estimate
- recurring annual estimate
- 3-year TCO
- component breakdown
- evidence coverage/confidence
- assumptions
- freshness date

## Prohibited v0.1 behavior
- determining legal compliance
- automatically declaring DPO legally mandatory
- presenting PP 33/2026 as currently effective before its effective state
- using a single vendor price as a market range
- outputting a number when minimum evidence coverage fails

## Formula gate
No numeric formula enters production until:
1. evidence classes and minimum sample rules are frozen;
2. regulatory-state tests pass;
3. article/calculator parity tests exist;
4. uncertainty/range methodology is documented.
