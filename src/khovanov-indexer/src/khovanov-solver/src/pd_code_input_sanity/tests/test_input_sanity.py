import unittest

from src.pd_code_input_sanity import input_sanity


class InputSanityTests(unittest.TestCase):
    def test_accepts_text_and_list_inputs(self):
        expected = [[1, 2, 2, 1]]
        self.assertEqual(input_sanity("[[1, 2, 2, 1]]"), expected)
        source = [[1, 2, 2, 1]]
        result = input_sanity(source)
        self.assertEqual(result, source)
        self.assertIsNot(result, source)
        self.assertIsNot(result[0], source[0])

    def test_empty_code_represents_the_zero_crossing_case(self):
        self.assertEqual(input_sanity([]), [])

    def test_does_not_execute_expressions(self):
        with self.assertRaises(ValueError):
            input_sanity("__import__('pathlib').Path('unexpected').touch()")

    def test_rejects_bad_shapes_and_types(self):
        invalid_values = (
            [[1, 2, 1]],
            [(1, 2, 2, 1)],
            [[True, 1, True, 1]],
            [[1, 2, 3, 1]],
        )
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                input_sanity(value)


if __name__ == "__main__":
    unittest.main()
