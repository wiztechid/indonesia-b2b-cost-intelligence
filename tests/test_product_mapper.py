import unittest
from engine.quote_compare import compare
from product.mapper import map_pair
from tests.fixtures.quotes import quote

def complete(q):
    q["commercial"]["taxState"]="included"
    q["commercial"]["travelState"]="not_applicable"
    return q

class ProductMapperTests(unittest.TestCase):
    def test_missing_date_blocks_and_suppresses(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        out=map_pair(a,b,compare(a,b),None)
        self.assertEqual(out["costState"],"BLOCKED")
        self.assertTrue(out["suppressPairwiseNumbers"])
        self.assertIn("COMPARISON_DATE_MISSING",out["reasonCodes"])

    def test_current_comparable_allows_numbers(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(out["costState"],"COMPARABLE")
        self.assertFalse(out["suppressPairwiseNumbers"])
        self.assertEqual(out["freshnessState"],"CURRENT")

    def test_tax_unknown_reason(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        b["commercial"]["taxState"]="unknown"
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertIn("TAX_UNKNOWN",out["reasonCodes"])
        self.assertTrue(out["suppressPairwiseNumbers"])

    def test_exclusions_partial_reason(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        b["scope"]["deliverablesExcluded"]=["incident_response"]
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(out["scopeState"],"PARTIALLY_COMPARABLE")
        self.assertIn("EXCLUSIONS_DIFFER",out["reasonCodes"])

    def test_sla_partial_reason(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["scope"]["sla"]={"responseHours":4}; b["scope"]["sla"]={"responseHours":24}
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertIn("SLA_DIFFERS",out["reasonCodes"])

    def test_stale_reason_and_suppression(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["validUntil"]="2026-09-30"
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(out["freshnessState"],"STALE")
        self.assertIn("QUOTE_STALE",out["reasonCodes"])
        self.assertTrue(out["suppressPairwiseNumbers"])

    def test_blocked_never_has_zero_reasons(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        b["commercial"]["totalAmount"]=None
        out=map_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(out["costState"],"BLOCKED")
        self.assertGreater(len(out["reasonCodes"]),0)

    def test_affiliate_does_not_change_math(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["commercialRelationship"]="affiliate"
        before=compare(a,b,"2026-10-04")
        out=map_pair(a,b,before,"2026-10-04")
        self.assertEqual(out["costState"],"COMPARABLE")

if __name__=="__main__":
    unittest.main()
