"""Compatibility wrapper for the bundled spatial projection engine."""

from spatial_coord_to_pd_code.src.spatial_coord_to_pd_code import (
    spatial_coord_to_pd_code,
)


def to_pd_code(spatial_coord: list[list[float]]) -> list[list[int]]:
    """Project a closed spatial polygon and return a validated PD code."""

    return spatial_coord_to_pd_code(spatial_coord)
