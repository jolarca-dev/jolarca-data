"""Unit tests for the pseudonymizer — mandatory coverage (README §Hard
requirements). Run: python3 -m unittest test_pseudonymizer
"""

import unittest
from pathlib import Path

from pseudonymizer import apply_rules, hash_value, load_rules

SALT = "unit-test-salt"


class PseudonymizerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(Path(__file__).with_name("rules.yml"))

    def test_fail_closed_default_drops_unlisted_fields(self):
        record = {"id": 1, "email": "should-never-land@example.test"}
        out = apply_rules("orders", record, self.rules, SALT)
        self.assertNotIn("email", out)
        self.assertIn("id", out)  # listed -> hashed, not raw

    def test_hash_rules_are_deterministic_and_not_cleartext(self):
        record = {"id": 42}
        first = apply_rules("orders", record, self.rules, SALT)
        second = apply_rules("orders", record, self.rules, SALT)
        self.assertEqual(first, second)
        self.assertNotEqual(first["id"], 42)
        self.assertNotEqual(first["id"], "42")
        self.assertEqual(first["id"], hash_value(42, SALT))

    def test_hash_changes_with_salt(self):
        self.assertNotEqual(
            hash_value(42, "salt-a"), hash_value(42, "salt-b")
        )

    def test_drop_rules_produce_absent_fields(self):
        record = {"id": 1, "buyer_name": "X", "phone": "5550000"}
        out = apply_rules("users", record, self.rules, SALT)
        self.assertNotIn("buyer_name", out)
        self.assertNotIn("phone", out)

    def test_generalize_reduces_timestamp_precision(self):
        record = {"id": 1, "created_at": "2026-08-15T10:30:00+00:00"}
        out = apply_rules("users", record, self.rules, SALT)
        self.assertEqual(out["created_at"], "2026-08-15")

    def test_unknown_source_table_fails_closed(self):
        with self.assertRaises(KeyError):
            apply_rules("payments", {"id": 1}, self.rules, SALT)


if __name__ == "__main__":
    unittest.main()
