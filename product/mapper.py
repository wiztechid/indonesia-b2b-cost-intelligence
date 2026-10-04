PROMPTS={
"TAX_UNKNOWN":"Ask vendor whether the quoted amount includes applicable tax.",
"TRAVEL_UNKNOWN":"Ask whether travel/on-site expenses are included.",
"COMPARISON_DATE_MISSING":"Set the comparison date before treating prices as current.",
"QUOTE_STALE":"Request an updated quotation or validity confirmation.",
"AMOUNT_SEMANTICS_UNKNOWN":"Confirm whether total includes setup and recurring components.",
"FX_PROVENANCE_MISSING":"Record exchange-rate source and date before normalization.",
"COMPONENT_PRICE_MISSING":"Request component-level pricing before separating a bundled service.",
"QUANTITY_LIMITS_DIFFER":"Confirm comparable request/system/entity limits.",
"COST_AMOUNT_MISSING":"Request the missing commercial amount before comparing cost.",
"SETUP_AMOUNT_MISSING":"Confirm the setup amount before deriving component-only contract cost.",
"RECURRING_AMOUNT_MISSING":"Confirm the recurring amount before deriving component-only contract cost.",
"IRREGULAR_RECURRING_TERM":"Confirm billing cadence and contract term before deriving contract cost.",
"COMMERCIAL_TERMS_INCOMPLETE":"Complete material commercial terms before comparing cost."
}

def _scope_reasons(a,b):
    reasons=[]
    if a["serviceType"]!=b["serviceType"]: return ["DIFFERENT_SERVICE_TYPE"]
    ai=set(a["scope"]["deliverablesIncluded"]); bi=set(b["scope"]["deliverablesIncluded"])
    if not ai or not bi: return ["EMPTY_SCOPE"]
    if not ai & bi: return ["NO_COMMON_DELIVERABLES"]
    if ai!=bi: reasons.append("INCLUDED_SCOPE_DIFFERS")
    if set(a["scope"].get("deliverablesExcluded",[]))!=set(b["scope"].get("deliverablesExcluded",[])): reasons.append("EXCLUSIONS_DIFFER")
    if a["scope"].get("quantityLimits")!=b["scope"].get("quantityLimits"): reasons.append("QUANTITY_LIMITS_DIFFER")
    if a["scope"].get("sla")!=b["scope"].get("sla"): reasons.append("SLA_DIFFERS")
    return reasons

def _cost_reasons(q):
    c=q["commercial"]; reasons=[]
    if c.get("amountSemantics")=="unknown": reasons.append("AMOUNT_SEMANTICS_UNKNOWN")
    if c.get("totalAmount") is None and c.get("amountSemantics")!="components_only": reasons.append("COST_AMOUNT_MISSING")
    if c.get("amountSemantics")=="components_only":
        if c.get("setupAmount") is None: reasons.append("SETUP_AMOUNT_MISSING")
        if c.get("recurringCadence")!="none" and c.get("recurringAmount") is None: reasons.append("RECURRING_AMOUNT_MISSING")
    if c.get("taxState")=="unknown": reasons.append("TAX_UNKNOWN")
    if c.get("travelState")=="unknown": reasons.append("TRAVEL_UNKNOWN")
    cadence=c.get("recurringCadence"); term=c.get("termMonths")
    if cadence=="quarterly" and term is not None and term%3: reasons.append("IRREGULAR_RECURRING_TERM")
    if cadence=="annual" and term is not None and term%12: reasons.append("IRREGULAR_RECURRING_TERM")
    return reasons

def _identity_fx_reasons(a,b):
    reasons=[]
    if a.get("providerKey")==b.get("providerKey"): reasons.append("SAME_PROVIDER")
    if a.get("evidenceRevisionId") and a.get("evidenceRevisionId")==b.get("evidenceRevisionId"): reasons.append("SAME_EVIDENCE_REVISION")
    currencies={a.get("currency"),b.get("currency")}
    if len(currencies)>1:
        for q in (a,b):
            fx=q.get("fxNormalization")
            if fx is None or not fx.get("source") or not fx.get("rateDate") or not fx.get("rate") or not fx.get("targetCurrency"):
                reasons.append("FX_PROVENANCE_MISSING"); break
    return reasons

def map_pair(a,b,engine_result,comparison_date=None):
    reasons=_scope_reasons(a,b)
    reasons.extend(_identity_fx_reasons(a,b))
    for q in (a,b):
        reasons.extend(_cost_reasons(q))
    freshness="UNKNOWN"
    if comparison_date is None:
        reasons.append("COMPARISON_DATE_MISSING")
    elif "freshnessComparable" not in engine_result or engine_result.get("freshnessComparable") is None:
        reasons.append("FRESHNESS_NOT_EVALUATED")
    elif engine_result.get("freshnessComparable") is False:
        freshness="STALE"; reasons.append("QUOTE_STALE")
    else:
        freshness="CURRENT"
    if not engine_result.get("costComparable",False) and not any(r in reasons for r in (
        "COST_AMOUNT_MISSING","AMOUNT_SEMANTICS_UNKNOWN","TAX_UNKNOWN","TRAVEL_UNKNOWN",
        "IRREGULAR_RECURRING_TERM","COMPARISON_DATE_MISSING","QUOTE_STALE",
        "SETUP_AMOUNT_MISSING","RECURRING_AMOUNT_MISSING","FRESHNESS_NOT_EVALUATED",
        "FX_PROVENANCE_MISSING")):
        reasons.append("COMMERCIAL_TERMS_INCOMPLETE")
    reasons=list(dict.fromkeys(reasons))
    prompts=[PROMPTS[r] for r in reasons if r in PROMPTS]
    return {
      "scopeState":engine_result["state"],
      "costState":"COMPARABLE" if engine_result.get("costComparable") else "BLOCKED",
      "freshnessState":freshness,
      "reasonCodes":reasons,
      "suppressPairwiseNumbers":not engine_result.get("costComparable",False),
      "missingInformationPrompts":prompts
    }
