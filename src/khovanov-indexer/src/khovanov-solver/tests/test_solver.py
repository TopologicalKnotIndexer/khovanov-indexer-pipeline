from pathlib import Path
from unittest.mock import patch
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from kho_solver import (  # noqa: E402
    UNKNOT_HOMOLOGY,
    _parse_javakh_output,
    _pd_code_wrapper,
    kho_solver,
)


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


class KhovanovSolverTests(unittest.TestCase):
    def test_pd_wrapper(self):
        self.assertEqual(
            _pd_code_wrapper([[1, 2, 2, 1]]),
            "PD[X[1, 2, 2, 1]]",
        )

    def test_output_parser_uses_last_homology_value(self):
        stdout = 'diagnostic "not a result"\n"q^-1*t^0*Z[0] + q^1*t^0*Z[0]"\n'
        self.assertEqual(_parse_javakh_output(stdout), UNKNOT_HOMOLOGY)
        with self.assertRaisesRegex(RuntimeError, "no quoted homology"):
            _parse_javakh_output("diagnostic only")

    def test_unknot_and_r1_unknot_avoid_java(self):
        with patch("kho_solver.run_javakh_with_shell") as run:
            self.assertEqual(kho_solver([]), UNKNOT_HOMOLOGY)
            self.assertEqual(kho_solver([[1, 2, 2, 1]]), UNKNOT_HOMOLOGY)
        run.assert_not_called()

    def test_backend_controls_are_forwarded(self):
        with patch("kho_solver.run_javakh_with_shell", return_value="q^3*t^0*Z[0]") as run:
            result = kho_solver(TREFOIL, java_path="custom-java", timeout=2, max_heap="512m")
        self.assertEqual(result, "q^3*t^0*Z[0]")
        run.assert_called_once_with(
            TREFOIL, java_path="custom-java", timeout=2, max_heap="512m"
        )

    def test_malicious_input_is_not_executed(self):
        with self.assertRaises(ValueError):
            kho_solver("__import__('os').getcwd()")

    @unittest.skipUnless(shutil.which("java"), "Java runtime is unavailable")
    def test_bundled_javakh_trefoil(self):
        result = kho_solver(TREFOIL, timeout=30, max_heap="1g")
        self.assertTrue(result.startswith("q^"), result)
        self.assertIn("t^", result)

    def test_cli_rejects_empty_stdin(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("expected a PD-code literal", completed.stderr)


if __name__ == "__main__":
    unittest.main()
