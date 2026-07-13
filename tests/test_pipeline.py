from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from from_file_to_pd_code import from_file_to_pd_code  # noqa: E402
from from_pd_code_to_knot_name import from_pd_code_to_knot_name  # noqa: E402
from khovanov_indexer_pipeline import khovanov_indexer_pipeline  # noqa: E402


TRIANGLE_DATA = """LAMMPS data file

3 atoms
3 bonds

Atoms

1 0 0 0
2 1 0 0
3 0 1 0

Bonds

1 1 1 2
2 1 2 3
3 1 3 1
"""


class KhovanovPipelineTests(unittest.TestCase):
    def test_stage_process_contracts(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "triangle.data"
            path.write_text(TRIANGLE_DATA, encoding="utf-8")
            converted = subprocess.CompletedProcess([], 0, "[]\n", "")
            with patch("from_file_to_pd_code.subprocess.run", return_value=converted):
                self.assertEqual(from_file_to_pd_code(str(path)), [])

        indexed = subprocess.CompletedProcess([], 0, "K0a1\n", "")
        with patch("from_pd_code_to_knot_name.subprocess.run", return_value=indexed) as run:
            self.assertEqual(from_pd_code_to_knot_name([], max_heap="1g"), ["K0a1"])
        self.assertEqual(run.call_args.kwargs["input"], "[]")

    def test_pipeline_composes_both_stages(self):
        with (
            patch("khovanov_indexer_pipeline.from_file_to_pd_code", return_value=[]) as convert,
            patch("khovanov_indexer_pipeline.from_pd_code_to_knot_name", return_value=["K0a1"]) as index,
        ):
            self.assertEqual(khovanov_indexer_pipeline("molecule.data"), ["K0a1"])
        convert.assert_called_once()
        index.assert_called_once()

    def test_stage_failures_are_not_silenced(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "triangle.data"
            path.write_text(TRIANGLE_DATA, encoding="utf-8")
            failed = subprocess.CompletedProcess([], 2, "", "bad molecular data")
            with patch("from_file_to_pd_code.subprocess.run", return_value=failed):
                with self.assertRaisesRegex(RuntimeError, "bad molecular data"):
                    from_file_to_pd_code(str(path))

    def test_real_end_to_end_triangle_is_unknot(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "triangle.data"
            path.write_text(TRIANGLE_DATA, encoding="utf-8")
            self.assertEqual(
                khovanov_indexer_pipeline(
                    str(path), projection_timeout=60, index_timeout=60, max_heap="1g"
                ),
                ["K0a1"],
            )

    def test_cli_missing_file(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py"), "missing.data"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("missing.data", completed.stderr)


if __name__ == "__main__":
    unittest.main()
