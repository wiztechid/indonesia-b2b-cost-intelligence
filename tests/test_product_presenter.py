import unittest
from engine.quote_compare import compare
from product.presenter import present_pair,present_matrix
from tests.fixtures.quotes import quote

def complete(q):
    q["commercial"]["taxState"]="included"
    q["commercial"]["travelState"]="not_applicable"
    return q

class PresenterTests(unittest.TestCase):
    def test_blocked_pair_never_exposes_numbers(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        view=present_pair(a,b,compare(a,b),None)
        self.assertEqual(view["costState"],"BLOCKED")
        self.assertIsNone(view["costs"])
        self.assertIsNone(view["annualizedRunRates"])

    def test_allowed_pair_exposes_numbers(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        view=present_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(view["costState"],"COMPARABLE")
        self.assertEqual(view["costs"],[12000000,12000000])

    def test_cross_currency_is_blocked_and_hides_numbers(self):
        fx1={"targetCurrency":"IDR","rate":1,"rateDate":"2026-10-04","source":"ref"}
        fx2={"targetCurrency":"IDR","rate":16000,"rateDate":"2026-10-04","source":"ref"}
        a=complete(quote("A","v1",currency="IDR",fx=fx1))
        b=complete(quote("B","v2",currency="USD",fx=fx2))
        raw=compare(a,b,"2026-10-04")
        self.assertTrue(raw["costComparable"])
        view=present_pair(a,b,raw,"2026-10-04")
        self.assertEqual(view["costState"],"BLOCKED")
        self.assertIsNone(view["costs"])

    def test_matrix_pair_count(self):
        qs=[complete(quote(str(i),f"v{i}")) for i in range(4)]
        view=present_matrix(qs,compare,"2026-10-04")
        self.assertEqual(view["quoteCount"],4)
        self.assertEqual(view["pairCount"],6)

    def test_matrix_rejects_outside_2_to_5(self):
        with self.assertRaises(ValueError): present_matrix([complete(quote("A","v1"))],compare,"2026-10-04")
        qs=[complete(quote(str(i),f"v{i}")) for i in range(6)]
        with self.assertRaises(ValueError): present_matrix(qs,compare,"2026-10-04")

    def test_duplicate_quote_ids_rejected_before_pairing(self):
        a=complete(quote("A","v1")); b=complete(quote("A","v2"))
        with self.assertRaises(ValueError): present_matrix([a,b],compare,"2026-10-04")

    def test_direct_self_id_pair_rejected(self):
        a=complete(quote("A","v1")); b=complete(quote("A","v2"))
        with self.assertRaises(ValueError): present_pair(a,b,{"state":"COMPARABLE","costComparable":True},"2026-10-04")

    def test_malformed_quote_rejected_before_engine(self):
        calls=[]
        def spy(a,b,d):
            calls.append(1); return compare(a,b,d)
        bad=complete(quote("A","v1")); del bad["scope"]
        good=complete(quote("B","v2"))
        with self.assertRaises(ValueError): present_matrix([bad,good],spy,"2026-10-04")
        self.assertEqual(calls,[])

    def test_pair_order_is_deterministic_input_order(self):
        qs=[complete(quote(x,"v"+x)) for x in ["C","A","B"]]
        view=present_matrix(qs,compare,"2026-10-04")
        self.assertEqual([p["quoteIds"] for p in view["pairs"]],[["C","A"],["C","B"],["A","B"]])

    def test_one_blocked_pair_does_not_hide_other_pairs(self):
        qs=[complete(quote("A","v1")),complete(quote("B","v2")),complete(quote("C","v3"))]
        qs[2]["commercial"]["taxState"]="unknown"
        view=present_matrix(qs,compare,"2026-10-04")
        by_pair={tuple(p["quoteIds"]):p for p in view["pairs"]}
        self.assertEqual(by_pair[("A","B")]["costState"],"COMPARABLE")
        self.assertIsNotNone(by_pair[("A","B")]["costs"])
        self.assertEqual(by_pair[("A","C")]["costState"],"BLOCKED")
        self.assertIsNone(by_pair[("A","C")]["costs"])

    def test_invalid_currency_rejected_by_canonical_schema(self):
        calls=[]
        def spy(a,b,d):
            calls.append(1); return compare(a,b,d)
        bad=complete(quote("A","v1",currency="idr"))
        good=complete(quote("B","v2"))
        with self.assertRaises(Exception): present_matrix([bad,good],spy,"2026-10-04")
        self.assertEqual(calls,[])

    def test_empty_deliverables_rejected_by_canonical_schema(self):
        bad=complete(quote("A","v1",included=[]))
        good=complete(quote("B","v2"))
        with self.assertRaises(Exception): present_matrix([bad,good],compare,"2026-10-04")

    def test_extra_root_field_rejected_by_canonical_schema(self):
        bad=complete(quote("A","v1")); bad["inventedField"]=True
        good=complete(quote("B","v2"))
        with self.assertRaises(Exception): present_matrix([bad,good],compare,"2026-10-04")

    def test_unknown_validity_flows_to_unknown_blocked_without_numbers(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["validUntil"]=None
        b["validUntil"]="2026-12-31"
        raw=compare(a,b,"2026-10-04")
        view=present_pair(a,b,raw,"2026-10-04")
        self.assertEqual(view["freshnessState"],"UNKNOWN")
        self.assertEqual(view["costState"],"BLOCKED")
        self.assertIn("FRESHNESS_NOT_EVALUATED",view["reasonCodes"])
        self.assertIsNone(view["costs"])
        self.assertIsNone(view["annualizedRunRates"])

    def test_presenter_exposes_required_v07_layers_without_inference(self):
        a=complete(quote("A","v1",included=["policy_review","monthly_advice"]))
        b=complete(quote("B","v2",included=["monthly_advice","incident_support"]))
        a["commercialRelationship"]="affiliate"
        raw=compare(a,b,"2026-10-04")
        view=present_pair(a,b,raw,"2026-10-04")
        self.assertEqual(view["commonDeliverables"],["monthly_advice"])
        self.assertIn("INCLUDED_SCOPE_DIFFERS",view["materialDifferences"])
        self.assertEqual(view["commercialRelationships"],[
            {"quoteId":"A","relationship":"affiliate"},
            {"quoteId":"B","relationship":"none"}
        ])

    def test_no_material_difference_is_empty_not_invented(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        view=present_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(view["materialDifferences"],[])
        self.assertEqual(view["commonDeliverables"],["monthly_advice","policy_review"])

    def test_relationship_disclosure_does_not_change_cost_math(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["commercialRelationship"]="sponsor"
        raw=compare(a,b,"2026-10-04")
        view=present_pair(a,b,raw,"2026-10-04")
        self.assertTrue(raw["costComparable"])
        self.assertEqual(view["costState"],"COMPARABLE")
        self.assertEqual(view["costs"],[12000000,12000000])
        self.assertEqual(view["commercialRelationships"][0]["relationship"],"sponsor")

    def test_new_layers_do_not_bypass_numeric_suppression(self):
        a,b=complete(quote("A","v1")),complete(quote("B","v2"))
        a["commercial"]["taxState"]="unknown"
        view=present_pair(a,b,compare(a,b,"2026-10-04"),"2026-10-04")
        self.assertEqual(view["costState"],"BLOCKED")
        self.assertIsNone(view["costs"])
        self.assertIsNone(view["annualizedRunRates"])
        self.assertIn("commonDeliverables",view)
        self.assertIn("commercialRelationships",view)

if __name__=="__main__":
    unittest.main()
