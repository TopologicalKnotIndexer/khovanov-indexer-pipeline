"""Identify catalogued knots by integral Khovanov homology."""

from os import PathLike

from get_khovanov_by_pd_code import get_khovanov_by_pd_code
from get_knotname_by_khovanov import get_knotname_by_khovanov


def khovanov_indexer(
    pd_code: list[list[int]],
    *,
    java_path: str | PathLike[str] | None = None,
    timeout: float | None = None,
    max_heap: str = "16g",
) -> list[str]:
    """Return all catalog names sharing the input diagram's homology."""

    homology = get_khovanov_by_pd_code(
        pd_code, java_path=java_path, timeout=timeout, max_heap=max_heap
    )
    return get_knotname_by_khovanov(homology)


if __name__ == "__main__":
    print(
        khovanov_indexer(
            [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
        )
    )
