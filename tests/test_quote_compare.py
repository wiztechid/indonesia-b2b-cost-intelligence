import unittest
from engine.quote_compare import normalized_total, compare
from tests.fixtures.quotes import quote

class QuoteEngineTests(unittest.TestCase):
    def test_all_in_not_double_counted(self):
        q=quote("A","v1",total=100,recurring=10,cadence="monthly",semantics="total_is_all_in")
        self.assertEqual(normalized_total(q),100)

    def test_unknown_semantics_blocks_total(self):
        q=quote("A","v1",total=100,semantics="unknown")
        self.assertIsNone(normalized_total(q))

    def test_different_service_non_comparable(self):
        self.assertEqual(compare(quote("A","v1"),quote("B","v2",service="dpia"))["state"],"NON_COMPARABLE")

    def test_scope_difference_is_partial(self):
        a=quote("A","v1",included=["policy_review","monthly_advice"])
        b=quote("B","v2",included=["policy_review"])
        self.assertEqual(compare(a,b)["state"],"PARTIALLY_COMPARABLE")

    def test_pairwise_symmetry(self):
        a,b=quote("A","v1"),quote("B","v2")
        self.assertEqual(compare(a,b)["state"],compare(b,a)["state"])

if __name__=="__main__": unittest.main()
