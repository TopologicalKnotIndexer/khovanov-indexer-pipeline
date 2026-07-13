"""Compatibility wrapper for the bundled coordinate extractor."""

from che_data_to_spatial_coord.src.che_data_to_spatial_coord import (
    che_data_to_spatial_coord,
)


def to_spatial_coord(che_data_filename: str) -> list[list[float]]:
    """Extract an ordered coordinate cycle from a LAMMPS data file."""

    return che_data_to_spatial_coord(che_data_filename)
