import unittest
from engine.quote_compare import normalized_total, normalized_costs, compare
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

if __name__=="__main__":
    unittest.main()
