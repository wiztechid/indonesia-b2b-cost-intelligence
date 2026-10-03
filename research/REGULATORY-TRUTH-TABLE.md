# Regulatory Truth Table v0.2

Checked: 2026-10-04

| ID | Instrument / event | State | Date | Product implication |
|---|---|---|---|---|
| REG-UU27 | UU 27/2022 Pelindungan Data Pribadi | effective baseline | 2022 | Primary statutory baseline; individual claims still require provision-level evidence. |
| REG-MK151 | MK 151/PUU-XXII/2024 | judicially_modified / binding | 2025-07-30 | Pasal 53(1) conjunction is read "dan/atau"; do not use the old cumulative-only DPO trigger logic. |
| REG-PP33 | PP 33/2026 implementing regulation | issued; effective-state requires official instrument-level binding before automated logic | 2026 | Never infer current applicability merely from publication. Exact effective date must be bound to authoritative text before calculator logic uses it. |

## Source hierarchy
1. Official promulgated instrument / JDIH / peraturan database.
2. Constitutional Court decision for judicial modification.
3. Regulator/ministry official guidance.
4. Secondary legal commentary only for discovery/context, never to override levels 1–3.

## Machine rule
A calculator rule may become active only when:
- authority evidence is bound;
- provision/decision scope is identified;
- effective state is known;
- no later amendment/judicial modification conflicts;
- checked_at is current under the freshness policy.

## MK 151 binding fact
Official MK decision record: decision delivered 2025-07-30; petition granted in full; the word "dan" in Article 53(1)(b) is conditionally unconstitutional unless read "dan/atau". MK decisions bind from pronouncement.

## Fail closed
REG-PP33 remains unavailable to automated obligation logic until the official instrument text and effective clause are captured as primary evidence.
