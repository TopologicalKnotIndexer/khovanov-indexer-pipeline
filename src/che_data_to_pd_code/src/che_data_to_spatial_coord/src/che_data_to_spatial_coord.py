"""Public entry point for extracting spatial coordinates from LAMMPS data."""

from pathlib import Path

try:
    from .file_zip import get_pos_list
except ImportError:  # Direct execution from the src directory.
    from file_zip import get_pos_list
SAMPLE_FILE = Path(__file__).resolve().parent / "data.random_knot_widened_L1000_K0_melt_limit_1"

def che_data_to_spatial_coord(filepath: str) -> list[list[float]]:
    """Return the closed-cycle coordinates stored in *filepath*."""
    return get_pos_list(filepath)

if __name__ == "__main__":
    points = che_data_to_spatial_coord(str(SAMPLE_FILE))
    if len(points) != 1000:
        raise AssertionError(f"expected 1000 sample points, received {len(points)}")
    print(len(points))
