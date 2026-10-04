def quote(qid, provider, service="dpo_service", included=None, total=12000000, recurring=None, cadence="none", term=12, semantics="total_is_all_in", limits=None):
    if included is None:
        included=["policy_review","monthly_advice"]
    if limits is None:
        limits={}
    return {
      "quoteId":qid,"providerKey":provider,"serviceType":service,
      "commercial":{"totalAmount":total,"setupAmount":0,"recurringAmount":recurring,"recurringCadence":cadence,"termMonths":term,"amountSemantics":semantics},
      "scope":{"deliverablesIncluded":included,"deliverablesExcluded":[],"quantityLimits":limits,"sla":None,"assumptions":[]}
    }
