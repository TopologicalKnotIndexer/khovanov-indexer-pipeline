import math
import unittest

from src.spatial_coord_to_pd_code import (
    _serialize_coordinates,
    _validate_coordinates,
    _validate_pd_output,
)


class SpatialCoordinateWrapperTests(unittest.TestCase):
    def test_serialization(self):
        self.assertEqual(
            _serialize_coordinates([[1, 2, 3]]),
            "1\n1.00000000000000000000 2.00000000000000000000 3.00000000000000000000\n",
        )

    def test_coordinate_validation(self):
        _validate_coordinates([])
        for value in ([[1, 2]], [[1, 2, True]], [[1, 2, math.inf]], "bad"):
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                _validate_coordinates(value)

    def test_pd_output_validation(self):
        self.assertEqual(_validate_pd_output([[1, 2, 2, 1]]), [[1, 2, 2, 1]])
        with self.assertRaises(ValueError):
            _validate_pd_output([[1, 2, 3, 1]])


if __name__ == "__main__":
    unittest.main()
