from pathlib import Path
from unittest.mock import patch
import shutil
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from get_khovanov_by_pd_code import get_khovanov_by_pd_code  # noqa: E402
from get_knotname_by_khovanov import (  # noqa: E402
    get_knotname_by_khovanov,
    load_khovanov_index,
)
from khovanov_indexer import khovanov_indexer  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
TREFOIL_HOMOLOGY = (
    "q^1*t^0*Z[0] + q^3*t^0*Z[0] + q^5*t^2*Z[0] + "
    "q^7*t^3*Z[2] + q^9*t^3*Z[0]"
)
UNKNOT_HOMOLOGY = "q^-1*t^0*Z[0] + q^1*t^0*Z[0]"


class KhovanovIndexerTests(unittest.TestCase):
    def test_complete_catalog_load_and_known_lookups(self):
        index = load_khovanov_index()
        self.assertEqual(len(index), 1549)
        self.assertEqual(sum(map(len, index.values())), 1783)
        self.assertEqual(get_knotname_by_khovanov(UNKNOT_HOMOLOGY), ["K0a1"])
        self.assertEqual(get_knotname_by_khovanov(TREFOIL_HOMOLOGY), ["K3a1"])
        self.assertEqual(get_knotname_by_khovanov("not in catalog"), [])

    def test_local_solver_process_contract(self):
        completed = subprocess.CompletedProcess(
            args=["python"], returncode=0, stdout=" q^3*t^0*Z[0]\n", stderr=""
        )
        with patch("get_khovanov_by_pd_code.subprocess.run", return_value=completed) as run:
            result = get_khovanov_by_pd_code(
                TREFOIL, java_path="custom-java", timeout=4, max_heap="512m"
            )
        self.assertEqual(result, "q^3*t^0*Z[0]")
        command = run.call_args.args[0]
        self.assertIn("--java", command)
        self.assertIn("custom-java", command)
        self.assertIn("--max-heap", command)
        self.assertIn("512m", command)
        self.assertEqual(run.call_args.kwargs["input"], repr(TREFOIL))

    def test_local_solver_failure_is_not_silenced(self):
        completed = subprocess.CompletedProcess(
            args=["python"], returncode=2, stdout="", stderr="bad PD code"
        )
        with patch("get_khovanov_by_pd_code.subprocess.run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "bad PD code"):
                get_khovanov_by_pd_code(TREFOIL)

    def test_indexer_composes_solver_and_lookup(self):
        with (
            patch("khovanov_indexer.get_khovanov_by_pd_code", return_value=TREFOIL_HOMOLOGY),
            patch("khovanov_indexer.get_knotname_by_khovanov", return_value=["K3a1"]) as lookup,
        ):
            self.assertEqual(khovanov_indexer(TREFOIL), ["K3a1"])
        lookup.assert_called_once_with(TREFOIL_HOMOLOGY)

    def test_end_to_end_unknot_without_java(self):
        self.assertEqual(khovanov_indexer([]), ["K0a1"])

    @unittest.skipUnless(shutil.which("java"), "Java runtime is unavailable")
    def test_end_to_end_trefoil(self):
        self.assertEqual(
            khovanov_indexer(TREFOIL, timeout=30, max_heap="1g"),
            ["K3a1"],
        )
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py"), "--timeout", "30", "--max-heap", "1g"],
            input=repr(TREFOIL),
            text=True,
            capture_output=True,
            check=False,
            timeout=45,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "K3a1")

    def test_cli_does_not_execute_input(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="__import__('os').getcwd()",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("malformed node", completed.stderr)


if __name__ == "__main__":
    unittest.main()
