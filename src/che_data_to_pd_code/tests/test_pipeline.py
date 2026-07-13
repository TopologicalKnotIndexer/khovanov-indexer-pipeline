from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from che_data_to_pd_code import che_data_to_pd_code  # noqa: E402
from to_pd_code import to_pd_code  # noqa: E402
from to_spatial_coord import to_spatial_coord  # noqa: E402


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


class MolecularPipelineTests(unittest.TestCase):
    def test_pipeline_orders_extraction_before_projection(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "molecule.data"
            source.write_text(TRIANGLE_DATA, encoding="utf-8")
            with (
                patch("che_data_to_pd_code.to_spatial_coord", return_value=[[0.0, 0.0, 0.0]]) as extract,
                patch("che_data_to_pd_code.to_pd_code", return_value=[]) as project,
            ):
                self.assertEqual(che_data_to_pd_code(str(source)), [])
            extract.assert_called_once_with(str(source))
            project.assert_called_once_with([[0.0, 0.0, 0.0]])

    def test_missing_file_is_an_explicit_error(self):
        with self.assertRaises(FileNotFoundError):
            che_data_to_pd_code("does-not-exist.data")

    def test_static_wrappers_use_bundled_sources(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "triangle.data"
            source.write_text(TRIANGLE_DATA, encoding="utf-8")
            self.assertEqual(len(to_spatial_coord(str(source))), 3)
        self.assertEqual(to_pd_code([[0, 0, 0], [1, 0, 0], [0, 1, 0]]), [])

    def test_cli_reports_missing_input(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "che_data_to_pd_code.py"), "missing.data"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("missing.data", completed.stderr)


if __name__ == "__main__":
    unittest.main()
