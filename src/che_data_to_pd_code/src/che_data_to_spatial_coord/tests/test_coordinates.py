from pathlib import Path
import unittest

from src.file_checker import content_check
from src.file_zip import content_pos_list, get_loop, get_pos_list, zip_pos_list


class CoordinateExtractionTests(unittest.TestCase):
    def test_committed_sample(self):
        sample = Path(__file__).resolve().parents[1] / "src" / "data.random_knot_widened_L1000_K0_melt_limit_1"
        points = get_pos_list(str(sample))
        self.assertEqual(len(points), 1000)
        self.assertEqual(len(zip_pos_list(points)), 24_000)

    def test_cycle_order_is_deterministic_without_atom_one(self):
        graph = {10: {20, 30}, 20: {10, 30}, 30: {10, 20}}
        self.assertEqual(get_loop(graph), [10, 20, 30])

    def test_rejects_paths_and_disconnected_cycles(self):
        with self.assertRaises(ValueError):
            get_loop({1: {2}, 2: {1}})
        with self.assertRaises(ValueError):
            get_loop(
                {
                    1: {2, 3}, 2: {1, 3}, 3: {1, 2},
                    4: {5, 6}, 5: {4, 6}, 6: {4, 5},
                }
            )

    def test_rejects_missing_atom_coordinates(self):
        atoms = [["1", "0", "0", "0"], ["2", "1", "0", "0"]]
        bonds = [["1", "1", "1", "3"], ["2", "1", "3", "1"]]
        with self.assertRaises(ValueError):
            content_pos_list(atoms, bonds)

    def test_content_check_reports_missing_sections(self):
        error, atoms, bonds = content_check(["LAMMPS data", "1 atoms"])
        self.assertTrue(error)
        self.assertIsNone(atoms)
        self.assertIsNone(bonds)


if __name__ == "__main__":
    unittest.main()
