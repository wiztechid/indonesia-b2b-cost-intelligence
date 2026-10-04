def quote(qid, provider, service="dpo_service", included=None, total=12000000, recurring=None, cadence="none", term=12, semantics="total_is_all_in"):
    return {
      "quoteId":qid,"providerKey":provider,"serviceType":service,
      "commercial":{"totalAmount":total,"setupAmount":0,"recurringAmount":recurring,"recurringCadence":cadence,"termMonths":term,"amountSemantics":semantics},
      "scope":{"deliverablesIncluded":included or ["policy_review","monthly_advice"],"deliverablesExcluded":[],"quantityLimits":{},"sla":None,"assumptions":[]}
    }
