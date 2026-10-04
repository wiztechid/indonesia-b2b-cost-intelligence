from typing import Optional

VALID_STATES={"COMPARABLE","PARTIALLY_COMPARABLE","NON_COMPARABLE","INSUFFICIENT_DATA"}

def annualized_run_rate(amount: Optional[float], cadence: str):
    if amount is None: return None
    if cadence=="monthly": return amount*12
    if cadence=="quarterly": return amount*4
    if cadence=="annual": return amount
    return None

def contract_recurring_cost(amount: Optional[float], cadence: str, term_months: Optional[int]):
    if amount is None or term_months is None: return None
    if cadence=="monthly": return amount*term_months
    if cadence=="quarterly":
        return amount*(term_months/3) if term_months % 3 == 0 else None
    if cadence=="annual":
        return amount*(term_months/12) if term_months % 12 == 0 else None
    if cadence=="none": return 0
    return None

def normalized_costs(q):
    c=q["commercial"]
    sem=c["amountSemantics"]
    total=c["totalAmount"]
    setup=c["setupAmount"]
    recurring_contract=contract_recurring_cost(c["recurringAmount"],c["recurringCadence"],c["termMonths"])
    run_rate=annualized_run_rate(c["recurringAmount"],c["recurringCadence"])
    if sem=="unknown":
        derived=None
    elif sem=="total_is_all_in":
        derived=total
    elif sem=="total_excludes_setup":
        derived=None if total is None or setup is None else total+setup
    elif sem=="total_excludes_recurring":
        derived=None if total is None or recurring_contract is None else total+recurring_contract
    elif sem=="components_only":
        derived=None if setup is None or recurring_contract is None else setup+recurring_contract
    else:
        derived=None
    return {"contractCost":derived,"annualizedRunRate":run_rate}

def normalized_total(q):
    return normalized_costs(q)["contractCost"]

def compare(a,b):
    if a["serviceType"]!=b["serviceType"]:
        return {"state":"NON_COMPARABLE","reason":"different_service_type"}
    ai=set(a["scope"]["deliverablesIncluded"])
    bi=set(b["scope"]["deliverablesIncluded"])
    if not ai or not bi:
        return {"state":"INSUFFICIENT_DATA","reason":"empty_scope"}
    common=ai & bi
    if not common:
        return {"state":"NON_COMPARABLE","reason":"no_common_deliverables"}
    same_scope=ai==bi and a["scope"]["quantityLimits"]==b["scope"]["quantityLimits"]
    ca,cb=normalized_costs(a),normalized_costs(b)
    commercial_ok=commercial_terms_complete(a) and commercial_terms_complete(b)
    state="COMPARABLE" if same_scope else "PARTIALLY_COMPARABLE"
    return {
        "state":state,
        "commonDeliverables":sorted(common),
        "costComparable":ca["contractCost"] is not None and cb["contractCost"] is not None and commercial_ok,
        "contractCosts":[ca["contractCost"],cb["contractCost"]],
        "annualizedRunRates":[ca["annualizedRunRate"],cb["annualizedRunRate"]]
    }


def is_stale(q, comparison_date):
    valid=q.get("validUntil")
    return valid is not None and valid < comparison_date

def provider_independent(a,b):
    return a.get("providerKey") != b.get("providerKey")

def same_revision(a,b):
    ra=a.get("evidenceRevisionId")
    rb=b.get("evidenceRevisionId")
    return ra is not None and ra==rb

def fx_amount(amount, source_currency, fx):
    if amount is None: return None
    if fx is None: return amount
    target=fx["targetCurrency"]
    if source_currency==target:
        return amount
    if not fx.get("source") or not fx.get("rateDate") or not fx.get("rate"):
        return None
    return amount*fx["rate"]


def commercial_disclosure(q):
    return q.get("commercialRelationship","unknown")

def commercial_terms_complete(q):
    c=q["commercial"]
    return c.get("taxState") not in (None,"unknown") and c.get("travelState") not in (None,"unknown")

def comparable_cost_allowed(q):
    return normalized_total(q) is not None and commercial_terms_complete(q)

def component_cost(bundle, component):
    components=bundle.get("componentPrices") or {}
    return components.get(component)

def bundled_component_separable(bundle, component):
    return component_cost(bundle, component) is not None
