import json
from pathlib import Path

_SCHEMA_PATH=Path(__file__).resolve().parents[1]/"buyer-intelligence"/"QUOTE-RECORD-SCHEMA.json"

def load_quote_schema():
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))

def validate_quote_record(q):
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError("jsonschema dependency required for quote validation") from exc
    jsonschema.Draft202012Validator(load_quote_schema(),format_checker=jsonschema.FormatChecker()).validate(q)
    return True
