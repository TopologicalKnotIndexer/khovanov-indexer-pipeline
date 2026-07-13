"""Look up knot names in the bundled Khovanov-homology catalog."""

from functools import lru_cache
from pathlib import Path

from slow_dict_reader.src.slow_dict_reader import slow_dict_reader


SOURCE_DIR = Path(__file__).resolve().parent
KHODMP = SOURCE_DIR / "khovanov-homology-list" / "data" / "sorted_khovanov.txt"


@lru_cache(maxsize=1)
def load_khovanov_index() -> dict[str, list[str]]:
    """Load and normalize the committed homology/name records once."""

    if not KHODMP.is_file():
        raise FileNotFoundError(KHODMP)
    return slow_dict_reader(str(KHODMP))


def get_knotname_by_khovanov(khovanov: str) -> list[str]:
    """Return independent copies of all catalog names matching *khovanov*."""

    if not isinstance(khovanov, str):
        raise TypeError("khovanov must be a string")
    key = khovanov.strip()
    if not key:
        return []
    return list(load_khovanov_index().get(key, ()))


if __name__ == "__main__":
    print(
        get_knotname_by_khovanov(
            "q^1*t^0*Z[0] + q^3*t^0*Z[0] + q^5*t^2*Z[0] + "
            "q^7*t^3*Z[2] + q^9*t^3*Z[0]"
        )
    )
