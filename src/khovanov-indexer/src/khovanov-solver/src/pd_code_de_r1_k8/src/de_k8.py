"""Compatibility wrapper for nugatory-crossing simplification."""

from pd_simplify import (
    get_nugatory_index,
    is_nugatory,
    remove_nugatory_crossing,
    remove_nugatory_crossings,
)


def get_8_core_index(pd_code: list[list[int]]) -> int:
    index = get_nugatory_index(pd_code)
    return -1 if index is None else index


def check_8_core(
    pd_code: list[list[int]], cross: object, index: int, n: int
) -> bool:
    """Retain the legacy signature while using label-independent detection."""

    del cross, n
    return is_nugatory(pd_code, index)


def del_8_core_by_index(
    pd_code: list[list[int]], cross_index: int
) -> list[list[int]]:
    return remove_nugatory_crossing(pd_code, cross_index)


def de_k8(pd_code: list[list[int]]) -> list[list[int]]:
    return remove_nugatory_crossings(pd_code)
