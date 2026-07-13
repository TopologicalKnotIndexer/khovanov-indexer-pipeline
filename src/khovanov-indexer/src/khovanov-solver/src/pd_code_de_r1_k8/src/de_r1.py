"""Compatibility wrapper for Reidemeister-I simplification."""

from pd_simplify import remove_reidemeister_one


def de_r1(pd_code: list[list[int]]) -> list[list[int]]:
    return remove_reidemeister_one(pd_code)
