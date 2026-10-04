from product.mapper import map_pair

def present_pair(a,b,engine_result,comparison_date=None):
    mapped=map_pair(a,b,engine_result,comparison_date)
    view={
      "quoteIds":[a["quoteId"],b["quoteId"]],
      "scopeState":mapped["scopeState"],
      "costState":mapped["costState"],
      "freshnessState":mapped["freshnessState"],
      "reasonCodes":mapped["reasonCodes"],
      "missingInformationPrompts":mapped["missingInformationPrompts"],
      "costs":None,
      "annualizedRunRates":None
    }
    if not mapped["suppressPairwiseNumbers"]:
        view["costs"]=engine_result.get("contractCosts")
        view["annualizedRunRates"]=engine_result.get("annualizedRunRates")
    return view

def present_matrix(quotes, compare_fn, comparison_date=None):
    if len(quotes)<2 or len(quotes)>5:
        raise ValueError("comparison requires 2 to 5 quotes")
    pairs=[]
    for i in range(len(quotes)):
        for j in range(i+1,len(quotes)):
            a,b=quotes[i],quotes[j]
            pairs.append(present_pair(a,b,compare_fn(a,b,comparison_date),comparison_date))
    return {"quoteCount":len(quotes),"pairCount":len(pairs),"pairs":pairs}
