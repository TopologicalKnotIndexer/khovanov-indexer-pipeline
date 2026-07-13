"""Compatibility API for the bundled PD-code simplifier."""

from pd_code_de_r1_k8.src.pd_simplify import simplify_pd_code


def de_k8_r1(pd_code: list[list[int]]) -> list[list[int]]:
    """Remove all Reidemeister-I and verified nugatory crossings."""

    return simplify_pd_code(pd_code)
