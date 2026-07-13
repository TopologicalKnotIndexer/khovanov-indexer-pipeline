from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import de_r1_k8
from pd_simplify import get_nugatory_index, validate_pd_code


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


def diagram_with_nugatory_join():
    first = [[1, 5, 2, 4], [3, 7, 4, 6], [5, 3, 6, 2]]
    second = [[8, 12, 9, 11], [10, 14, 11, 13], [12, 10, 13, 9]]
    return [[1, 7, 8, 14], *first, *second]


class SimplificationTests(unittest.TestCase):
    def test_removes_r1_without_mutating_input(self):
        pd_code = [[1, 1, 2, 2]]
        original = deepcopy(pd_code)
        self.assertEqual(de_r1_k8(pd_code), [])
        self.assertEqual(pd_code, original)

    def test_reduced_prime_diagram_is_unchanged(self):
        self.assertEqual(de_r1_k8(TREFOIL), TREFOIL)

    def test_removes_label_independent_nugatory_crossing(self):
        pd_code = diagram_with_nugatory_join()
        self.assertEqual(get_nugatory_index(pd_code), 0)
        reduced = de_r1_k8(pd_code)
        self.assertEqual(len(reduced), 6)
        validate_pd_code(reduced)

    def test_accepts_multiple_strand_components(self):
        pd_code = [
            [2, 9, 3, 10],
            [4, 7, 1, 8],
            [6, 11, 7, 12],
            [8, 3, 5, 4],
            [9, 2, 10, 1],
            [12, 5, 11, 6],
        ]
        self.assertEqual(len(de_r1_k8(pd_code)), 6)

    def test_rejects_invalid_label_counts(self):
        with self.assertRaisesRegex(ValueError, "exactly twice"):
            de_r1_k8([[1, 2, 3, 4]])


class CommandLineTests(unittest.TestCase):
    def test_standard_input_is_not_executed(self):
        script = Path(__file__).resolve().parents[1] / "src" / "main.py"
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            expression = f"__import__('pathlib').Path({str(marker)!r}).touch()"
            result = subprocess.run(
                [sys.executable, str(script)],
                input=expression,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
