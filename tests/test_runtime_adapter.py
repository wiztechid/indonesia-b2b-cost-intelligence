import unittest
from runtime.adapter import compare_request
from tests.fixtures.quotes import quote

def complete(q):
    q["commercial"]["taxState"]="included"
    q["commercial"]["travelState"]="not_applicable"
    return q

class RuntimeAdapterTests(unittest.TestCase):
    def test_success_is_presenter_safe(self):
        result=compare_request({"comparisonDate":"2026-10-04","quotes":[complete(quote("A","v1")),complete(quote("B","v2"))]})
        self.assertTrue(result["ok"])
        pair=result["data"]["pairs"][0]
        self.assertEqual(pair["costState"],"COMPARABLE")
        self.assertIn("commonDeliverables",pair)
        self.assertNotIn("freshnessComparable",pair)
        self.assertNotIn("contractCosts",pair)

    def test_unknown_envelope_field_fails_closed(self):
        result=compare_request({"comparisonDate":"2026-10-04","quotes":[],"debug":True})
        self.assertEqual(result["error"]["code"],"INVALID_REQUEST")

    def test_invalid_date_fails_closed(self):
        result=compare_request({"comparisonDate":"04-10-2026","quotes":[complete(quote("A","v1")),complete(quote("B","v2"))]})
        self.assertEqual(result["error"]["code"],"INVALID_REQUEST")

    def test_invalid_quote_maps_without_internal_details(self):
        bad=complete(quote("A","v1")); bad["currency"]="idr"
        result=compare_request({"comparisonDate":"2026-10-04","quotes":[bad,complete(quote("B","v2"))]})
        self.assertEqual(result["error"]["code"],"INVALID_QUOTE")
        self.assertNotIn("trace",str(result).lower())
        self.assertNotIn("idr",result["error"]["message"])

    def test_duplicate_id_is_comparison_set_error(self):
        result=compare_request({"comparisonDate":"2026-10-04","quotes":[complete(quote("A","v1")),complete(quote("A","v2"))]})
        self.assertEqual(result["error"]["code"],"INVALID_COMPARISON_SET")

    def test_missing_comparison_date_is_allowed_but_numbers_blocked(self):
        result=compare_request({"quotes":[complete(quote("A","v1")),complete(quote("B","v2"))]})
        self.assertTrue(result["ok"])
        pair=result["data"]["pairs"][0]
        self.assertEqual(pair["freshnessState"],"UNKNOWN")
        self.assertEqual(pair["costState"],"BLOCKED")
        self.assertIsNone(pair["costs"])
        self.assertIsNone(pair["annualizedRunRates"])

if __name__=="__main__":
    unittest.main()
