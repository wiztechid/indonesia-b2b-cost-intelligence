import unittest
from engine.quote_compare import normalized_total, normalized_costs, compare, is_stale, provider_independent, same_revision, fx_amount, commercial_disclosure, commercial_terms_complete, comparable_cost_allowed, component_cost, bundled_component_separable
from tests.fixtures.quotes import quote

class QuoteEngineTests(unittest.TestCase):
    def test_all_in_not_double_counted(self):
        q=quote("A","v1",total=100,recurring=10,cadence="monthly",semantics="total_is_all_in")
        self.assertEqual(normalized_total(q),100)

    def test_unknown_semantics_blocks_total(self):
        self.assertIsNone(normalized_total(quote("A","v1",total=100,semantics="unknown")))

    def test_three_month_contract_differs_from_annual_run_rate(self):
        q=quote("A","v1",total=None,recurring=10,cadence="monthly",term=3,semantics="components_only")
        c=normalized_costs(q)
        self.assertEqual(c["contractCost"],30)
        self.assertEqual(c["annualizedRunRate"],120)

    def test_irregular_quarter_term_fails_closed(self):
        q=quote("A","v1",total=None,recurring=30,cadence="quarterly",term=4,semantics="components_only")
        self.assertIsNone(normalized_total(q))

    def test_different_service_non_comparable(self):
        self.assertEqual(compare(quote("A","v1"),quote("B","v2",service="dpia"))["state"],"NON_COMPARABLE")

    def test_scope_difference_partial(self):
        a=quote("A","v1",included=["policy_review","monthly_advice"])
        b=quote("B","v2",included=["policy_review"])
        self.assertEqual(compare(a,b)["state"],"PARTIALLY_COMPARABLE")

    def test_quantity_limit_difference_partial(self):
        a=quote("A","v1",limits={"requests":10})
        b=quote("B","v2",limits={"requests":20})
        self.assertEqual(compare(a,b)["state"],"PARTIALLY_COMPARABLE")

    def test_explicit_empty_scope_insufficient(self):
        self.assertEqual(compare(quote("A","v1",included=[]),quote("B","v2"))["state"],"INSUFFICIENT_DATA")

    def test_no_common_scope_non_comparable(self):
        a=quote("A","v1",included=["policy_review"])
        b=quote("B","v2",included=["incident_response"])
        self.assertEqual(compare(a,b)["state"],"NON_COMPARABLE")

    def test_pairwise_state_symmetry(self):
        a=quote("A","v1",included=["policy_review","monthly_advice"])
        b=quote("B","v2",included=["policy_review"])
        self.assertEqual(compare(a,b)["state"],compare(b,a)["state"])

    def test_pairwise_cost_flag_symmetry(self):
        a,b=quote("A","v1",total=100),quote("B","v2",total=200)
        self.assertEqual(compare(a,b)["costComparable"],compare(b,a)["costComparable"])

    def test_stale_quote(self):
        self.assertTrue(is_stale({"validUntil":"2026-09-30"},"2026-10-04"))

    def test_same_provider_not_independent(self):
        self.assertFalse(provider_independent({"providerKey":"v1"},{"providerKey":"v1"}))

    def test_same_revision_detected(self):
        self.assertTrue(same_revision({"evidenceRevisionId":"r1"},{"evidenceRevisionId":"r1"}))

    def test_fx_same_currency_is_idempotent(self):
        fx={"targetCurrency":"IDR","rate":17000,"rateDate":"2026-10-04","source":"reference"}
        self.assertEqual(fx_amount(100,"IDR",fx),100)

    def test_fx_requires_provenance(self):
        fx={"targetCurrency":"IDR","rate":17000,"rateDate":"2026-10-04","source":""}
        self.assertIsNone(fx_amount(100,"USD",fx))

    def test_fx_converts_once(self):
        fx={"targetCurrency":"IDR","rate":17000,"rateDate":"2026-10-04","source":"reference"}
        converted=fx_amount(100,"USD",fx)
        self.assertEqual(converted,1700000)
        self.assertEqual(fx_amount(converted,"IDR",fx),1700000)

    def test_unknown_tax_blocks_cost_comparison(self):
        q=quote("A","v1",total=100)
        q["commercial"]["taxState"]="unknown"
        q["commercial"]["travelState"]="included"
        self.assertFalse(comparable_cost_allowed(q))

    def test_known_tax_and_travel_allow_cost(self):
        q=quote("A","v1",total=100)
        q["commercial"]["taxState"]="included"
        q["commercial"]["travelState"]="not_applicable"
        self.assertTrue(comparable_cost_allowed(q))

    def test_commercial_relationship_is_disclosure_only(self):
        q=quote("A","v1")
        q["commercialRelationship"]="affiliate"
        self.assertEqual(commercial_disclosure(q),"affiliate")
        self.assertEqual(normalized_total(q),12000000)

    def test_bundle_component_not_invented(self):
        bundle={"componentPrices":None}
        self.assertIsNone(component_cost(bundle,"pentest"))
        self.assertFalse(bundled_component_separable(bundle,"pentest"))

    def test_bundle_component_separable_only_when_explicit(self):
        bundle={"componentPrices":{"pentest":5000000}}
        self.assertEqual(component_cost(bundle,"pentest"),5000000)
        self.assertTrue(bundled_component_separable(bundle,"pentest"))

    def test_pairwise_unknown_tax_blocks_cost_flag(self):
        a,b=quote("A","v1",total=100),quote("B","v2",total=200)
        for q in (a,b):
            q["commercial"]["taxState"]="included"
            q["commercial"]["travelState"]="not_applicable"
        b["commercial"]["taxState"]="unknown"
        self.assertFalse(compare(a,b)["costComparable"])

    def test_exclusion_difference_is_partial(self):
        a,b=quote("A","v1"),quote("B","v2")
        b["scope"]["deliverablesExcluded"]=["incident_response"]
        self.assertEqual(compare(a,b)["state"],"PARTIALLY_COMPARABLE")

    def test_sla_difference_is_partial(self):
        a,b=quote("A","v1"),quote("B","v2")
        a["scope"]["sla"]={"responseHours":4}
        b["scope"]["sla"]={"responseHours":24}
        self.assertEqual(compare(a,b)["state"],"PARTIALLY_COMPARABLE")

    def test_expired_quote_blocks_current_cost_comparison(self):
        a,b=quote("A","v1"),quote("B","v2")
        for q in (a,b):
            q["commercial"]["taxState"]="included"
            q["commercial"]["travelState"]="not_applicable"
        a["validUntil"]="2026-09-30"
        b["validUntil"]="2026-12-31"
        r=compare(a,b,comparison_date="2026-10-04")
        self.assertFalse(r["costComparable"])
        self.assertFalse(r["freshnessComparable"])

    def test_missing_comparison_date_blocks_current_cost(self):
        a,b=quote("A","v1",total=100),quote("B","v2",total=200)
        for q in (a,b):
            q["commercial"]["taxState"]="included"
            q["commercial"]["travelState"]="not_applicable"
        r=compare(a,b)
        self.assertFalse(r["costComparable"])
        self.assertIsNone(r["freshnessComparable"])

if __name__=="__main__":
    unittest.main()
