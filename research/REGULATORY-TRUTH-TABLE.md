# Regulatory Truth Table v0.2

Checked: 2026-10-04

| ID | Instrument / event | State | Issued / decided | Effective / binding | Product implication |
|---|---|---|---|---|---|
| REG-UU27 | UU 27/2022 Pelindungan Data Pribadi | effective baseline | 2022 | effective | Primary statutory baseline; individual claims still require provision-level evidence. |
| REG-MK151 | MK 151/PUU-XXII/2024 | judicially_modified | 2025-07-30 | binding from pronouncement 2025-07-30 | Pasal 53(1)(b) conjunction is read "dan/atau"; reject old cumulative-only DPO trigger logic. |
| REG-PP33 | PP 33/2026 implementing regulation | issued_not_effective | primary-source issue/promulgation metadata still to bind | 2027-01-16 (corroborated secondary metadata; primary effective clause still required before automated obligation logic) | Do not apply PP 33/2026 as current law before effective date. Prepare future-state content separately. |

## Evidence binding

### REG-MK151 — authoritative
Official Constitutional Court record confirms:
- Case: 151/PUU-XXII/2024.
- Decision date: 2025-07-30.
- Petition granted in full.
- The word "dan" in Article 53(1)(b) has no conditional binding force unless read "dan/atau".
- Constitutional Court decisions bind from pronouncement.

Authority: Mahkamah Konstitusi RI decision record / decision copy.

### REG-PP33 — partially bound
Multiple current legal metadata sources consistently report an effective date of 2027-01-16. Secondary metadata is inconsistent on the issue/signing date (15 vs 16 July 2026), so that field is deliberately NOT normalized yet.

Product rule:
- effective_at may be stored as a corroborated candidate;
- no PP-derived automated legal-obligation rule may activate until the official promulgated instrument/effective clause is captured;
- pages written before 2027-01-16 must distinguish current UU/MK obligations from future PP implementation requirements.

## Source hierarchy
1. Official promulgated instrument / JDIH / official government regulation database.
2. Constitutional Court decision for judicial modification.
3. Regulator/ministry official guidance.
4. Secondary legal metadata/commentary for discovery and corroboration only; never override levels 1–3.

## Machine rule
A calculator rule may become active only when:
- authority evidence is bound;
- provision/decision scope is identified;
- effective state is known from authoritative evidence;
- no later amendment/judicial modification conflicts;
- checked_at is current under the freshness policy.

## Temporal states
Never collapse:
- issued/published
- effective
- amended
- judicially_modified
- superseded

Future-effective rules may be shown as preparation guidance, but must not be represented as current legal obligations.

## Fail closed
If authoritative evidence and secondary metadata disagree or authoritative evidence is absent, preserve the disagreement and disable the affected automated legal conclusion.
