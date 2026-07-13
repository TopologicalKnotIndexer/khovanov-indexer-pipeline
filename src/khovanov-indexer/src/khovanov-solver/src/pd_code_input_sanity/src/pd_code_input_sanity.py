"""Safely parse and perform weak structural validation of a PD code."""

from ast import literal_eval
from collections import Counter
from copy import deepcopy


def input_sanity(value: str | list[list[int]]) -> list[list[int]]:
    """Return a validated PD code without executing input as Python code.

    This is intentionally a *weak* validator: it checks the container shape,
    integer label type, and the rule that every arc label occurs exactly twice.
    It does not prove that the code has a planar realization.
    """

    if isinstance(value, str):
        try:
            parsed = literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError("input is not a Python literal representing a PD code") from exc
    elif isinstance(value, list):
        parsed = deepcopy(value)
    else:
        raise TypeError("PD code input must be a string or a list")

    if not isinstance(parsed, list):
        raise TypeError("a PD code must be a list of crossings")

    labels: list[int] = []
    for crossing in parsed:
        if not isinstance(crossing, list):
            raise TypeError("every crossing must be a list")
        if len(crossing) != 4:
            raise ValueError("every crossing must contain exactly four labels")
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int):
                raise TypeError("arc labels must be integers, not booleans or other values")
            labels.append(label)

    invalid_counts = {label: count for label, count in Counter(labels).items() if count != 2}
    if invalid_counts:
        details = ", ".join(f"{label}: {count}" for label, count in sorted(invalid_counts.items()))
        raise ValueError(f"every arc label must occur exactly twice; observed {details}")
    return parsed


if __name__ == "__main__":
    print(input_sanity("[[1, 2, 2, 1]]"))
