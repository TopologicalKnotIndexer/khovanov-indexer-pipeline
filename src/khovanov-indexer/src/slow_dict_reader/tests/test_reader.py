from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from knotname_reg import knotname_reg  # noqa: E402
from slow_dict_reader import slow_dict_reader, slow_dict_reader_raw  # noqa: E402


class SlowDictionaryReaderTests(unittest.TestCase):
    def test_normalizes_and_deduplicates_names(self):
        content = """# catalog
[value|mk6a3,mk4a1]
[value|MK6A3,MK4A1]
[other|k7a7]
"""
        self.assertEqual(
            slow_dict_reader_raw(content),
            {"value": ["K4a1,K6a3"], "other": ["mK7a7"]},
        )

    def test_composite_multiplicity_is_preserved(self):
        self.assertEqual(knotname_reg("K3a1,K3a1"), "K3a1,K3a1")

    def test_reports_line_number_for_malformed_records(self):
        for content in ("not-a-record", "[missing separator]", "[|K3a1]", "[x|bad]"):
            with self.subTest(content=content), self.assertRaisesRegex(ValueError, "line 1"):
                slow_dict_reader_raw(content)

    def test_file_reader_accepts_utf8_bom(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.txt"
            path.write_text("\ufeff[1|K3a1]\n", encoding="utf-8")
            self.assertEqual(slow_dict_reader(str(path)), {"1": ["K3a1"]})
        with self.assertRaises(FileNotFoundError):
            slow_dict_reader("missing-catalog.txt")

    def test_cli_outputs_json_and_rejects_invalid_input(self):
        valid = subprocess.run(
            [sys.executable, str(SRC / "slow_dict_reader.py")],
            input="[1|K3a1]\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(valid.returncode, 0)
        self.assertEqual(json.loads(valid.stdout), {"1": ["K3a1"]})
        invalid = subprocess.run(
            [sys.executable, str(SRC / "slow_dict_reader.py")],
            input="bad\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("line 1", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
