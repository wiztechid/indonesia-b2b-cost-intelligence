from datetime import date
from jsonschema import ValidationError
from engine.quote_compare import compare
from product.presenter import present_matrix

_ALLOWED_KEYS={"comparisonDate","quotes"}

def _error(code,message):
    return {"ok":False,"error":{"code":code,"message":message}}

def _valid_date(value):
    if value is None:
        return True
    if not isinstance(value,str):
        return False
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False

def compare_request(payload):
    if not isinstance(payload,dict):
        return _error("INVALID_REQUEST","Request body must be an object.")
    if set(payload)-_ALLOWED_KEYS or "quotes" not in payload:
        return _error("INVALID_REQUEST","Request contains unsupported or missing top-level fields.")
    comparison_date=payload.get("comparisonDate")
    if not _valid_date(comparison_date):
        return _error("INVALID_REQUEST","comparisonDate must be an ISO date or null.")
    quotes=payload["quotes"]
    if not isinstance(quotes,list):
        return _error("INVALID_REQUEST","quotes must be an array.")
    if len(quotes)<2 or len(quotes)>5:
        return _error("INVALID_COMPARISON_SET","Comparison requires 2 to 5 quotes.")
    ids=[q.get("quoteId") for q in quotes if isinstance(q,dict)]
    if len(ids)==len(quotes) and len(ids)!=len(set(ids)):
        return _error("INVALID_COMPARISON_SET","quoteId values must be unique.")
    try:
        data=present_matrix(quotes,compare,comparison_date)
    except ValidationError:
        return _error("INVALID_QUOTE","One or more quotes fail canonical validation.")
    except ValueError as exc:
        message=str(exc)
        if "quoteId" in message or "comparison requires" in message or "same quoteId" in message:
            return _error("INVALID_COMPARISON_SET","Comparison set is invalid.")
        return _error("INVALID_QUOTE","One or more quotes are invalid.")
    return {"ok":True,"data":data}
