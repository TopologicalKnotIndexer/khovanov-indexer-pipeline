import unittest

from src.AmphichiralChecker import AmphichiralChecker, knotname_reg


class KnotNameNormalizationTests(unittest.TestCase):
    def test_documented_examples(self):
        self.assertEqual(knotname_reg("mk6a3,mk4a1"), "K4a1,K6a3")
        self.assertEqual(knotname_reg("k7a7"), "mK7a7")

    def test_casing_is_canonicalized_before_mirror_logic(self):
        self.assertEqual(knotname_reg("K7A7"), "mK7a7")
        self.assertEqual(knotname_reg("MK7A7"), "K7a7")

    def test_composite_multiplicity_is_preserved(self):
        self.assertEqual(knotname_reg("K3a1,K3a1"), "K3a1,K3a1")

    def test_mirror_toggle_and_format_validation(self):
        checker = AmphichiralChecker()
        self.assertEqual(checker.get_mirror_for_prime("K3A1"), "mK3a1")
        self.assertEqual(checker.get_mirror_for_prime("MK3A1"), "K3a1")
        self.assertFalse(checker.is_prime_knot_name_format("not-a-knot"))

    def test_invalid_names_raise_explicit_errors(self):
        for value in ("", "K3x1", "K3a1,", 42):
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                knotname_reg(value)


if __name__ == "__main__":
    unittest.main()
