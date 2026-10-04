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

    def test_cross_currency_engine_true_still_hides_numbers(self):
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

if __name__=="__main__":
    unittest.main()
