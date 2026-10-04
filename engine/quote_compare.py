from dataclasses import dataclass
from typing import Optional

VALID_STATES={"COMPARABLE","PARTIALLY_COMPARABLE","NON_COMPARABLE","INSUFFICIENT_DATA"}

def annualize(amount: Optional[float], cadence: str, term_months: Optional[int]):
    if amount is None: return None
    if cadence=="monthly" and term_months is not None: return amount*12
    if cadence=="quarterly" and term_months is not None: return amount*4
    if cadence=="annual": return amount
    return None

def normalized_total(q):
    c=q["commercial"]
    sem=c["amountSemantics"]
    total=c["totalAmount"]
    setup=c["setupAmount"]
    recurring=annualize(c["recurringAmount"],c["recurringCadence"],c["termMonths"])
    if sem=="unknown": return None
    if sem=="total_is_all_in": return total
    if sem=="total_excludes_setup":
        return None if total is None or setup is None else total+setup
    if sem=="total_excludes_recurring":
        return None if total is None or recurring is None else total+recurring
    if sem=="components_only":
        if setup is None or recurring is None: return None
        return setup+recurring
    return None

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
    ta,tb=normalized_total(a),normalized_total(b)
    state="COMPARABLE" if same_scope else "PARTIALLY_COMPARABLE"
    return {"state":state,"commonDeliverables":sorted(common),"costComparable":ta is not None and tb is not None,"normalized12m":[ta,tb]}
