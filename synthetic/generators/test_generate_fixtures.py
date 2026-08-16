# Determinism & divergence tests for the fixture generator.
# Run: python3 -m unittest test_generate_fixtures
import tempfile
import unittest
from pathlib import Path

import generate_fixtures as gen


class GeneratorTest(unittest.TestCase):
    def test_same_seed_same_output(self):
        self.assertEqual(gen.generate(1234), gen.generate(1234))

    def test_new_seed_yields_new_identities(self):
        a, b = gen.generate(1), gen.generate(2)
        # buyers are randomized per order; identity sets must differ
        buyers_a = {o["buyer_key"] for o in a["orders"]}
        buyers_b = {o["buyer_key"] for o in b["orders"]}
        self.assertNotEqual(buyers_a, buyers_b)

    def test_keys_and_currency_invariants(self):
        data = gen.generate(7)
        for s in data["sellers"]:
            self.assertTrue(s["seller_key"].startswith("SYN-SLR-"))
        for o in data["orders"]:
            self.assertEqual(o["currency"], "EUR")
            self.assertGreaterEqual(o["vat_rate_pct"], 0)

    def test_write_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            gen.write(gen.generate(9), Path(tmp))
            self.assertTrue((Path(tmp) / "sellers.yml").exists())
            self.assertTrue((Path(tmp) / "products.yml").exists())
            self.assertTrue((Path(tmp) / "orders.yml").exists())


if __name__ == "__main__":
    unittest.main()
