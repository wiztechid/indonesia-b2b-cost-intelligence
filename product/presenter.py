from product.mapper import map_pair

REQUIRED_RECORD_KEYS={"quoteId","providerKey","serviceType","quoteDate","currency","commercial","scope","evidenceRevisionId","commercialRelationship"}

def _validate_quote_shape(q):
    if not isinstance(q,dict): raise ValueError("quote must be an object")
    missing=REQUIRED_RECORD_KEYS-set(q)
    if missing: raise ValueError("quote missing required fields: "+",".join(sorted(missing)))
    if not q["quoteId"]: raise ValueError("quoteId must be non-empty")
    if not isinstance(q["commercial"],dict) or not isinstance(q["scope"],dict):
        raise ValueError("commercial and scope must be objects")

def _validate_pair(a,b):
    _validate_quote_shape(a); _validate_quote_shape(b)
    if a["quoteId"]==b["quoteId"]: raise ValueError("cannot compare the same quoteId")

def present_pair(a,b,engine_result,comparison_date=None):
    _validate_pair(a,b)
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
    if not isinstance(quotes,list): raise ValueError("quotes must be a list")
    if len(quotes)<2 or len(quotes)>5: raise ValueError("comparison requires 2 to 5 quotes")
    for q in quotes: _validate_quote_shape(q)
    ids=[q["quoteId"] for q in quotes]
    if len(ids)!=len(set(ids)): raise ValueError("quoteId values must be unique")
    pairs=[]
    for i in range(len(quotes)):
        for j in range(i+1,len(quotes)):
            a,b=quotes[i],quotes[j]
            pairs.append(present_pair(a,b,compare_fn(a,b,comparison_date),comparison_date))
    return {"quoteCount":len(quotes),"pairCount":len(pairs),"pairs":pairs}
