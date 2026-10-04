def quote(qid, provider, service="dpo_service", included=None, total=12000000, recurring=None, cadence="none", term=12, semantics="total_is_all_in", limits=None, currency="IDR", revision=None, fx=None):
    if included is None:
        included=["policy_review","monthly_advice"]
    if limits is None:
        limits={}
    return {
      "quoteId":qid,"providerKey":provider,"serviceType":service,
      "quoteDate":"2026-10-01","validUntil":"2026-12-31","currency":currency,
      "evidenceRevisionId":revision or ("rev-"+qid),
      "commercialRelationship":"none",
      "fxNormalization":fx,
      "commercial":{"totalAmount":total,"taxState":"unknown","travelState":"unknown","setupAmount":0,"recurringAmount":recurring,"recurringCadence":cadence,"termMonths":term,"amountSemantics":semantics},
      "scope":{"deliverablesIncluded":included,"deliverablesExcluded":[],"quantityLimits":limits,"sla":None,"assumptions":[]}
    }
