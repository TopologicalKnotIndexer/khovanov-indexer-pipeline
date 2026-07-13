"""Normalize organization knot names using the bundled reference tables."""

from pathlib import Path
import re


_DATA_DIR = Path(__file__).resolve().parent / "knotname-reg" / "src" / "data"
_PRIME_NAME = re.compile(r"^(m?)k(\d+)([an])(\d+)$", re.IGNORECASE)


class AmphichiralChecker:
    """Apply writhe corrections and remove redundant amphichiral mirrors."""

    def __init__(self) -> None:
        self.name1_to_name2 = self._load_name_pairs(_DATA_DIR / "name_pair.txt")
        self.amphichiral_names = self._load_lines(_DATA_DIR / "amphichiral_list.txt")
        self.need_mirror = {
            self._canonical_prime_name(name).removeprefix("m")
            for name in self._load_lines(_DATA_DIR / "need_mirror.txt")
        }

    @staticmethod
    def _load_lines(path: Path) -> set[str]:
        return {
            line.strip()
            for line in path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        }

    @classmethod
    def _load_name_pairs(cls, path: Path) -> dict[str, str]:
        result: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            tabulated_name, canonical_name = line.split()
            result[cls._canonical_prime_name(canonical_name)] = tabulated_name
        return result

    @staticmethod
    def _canonical_prime_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("a prime knot name must be a string")
        match = _PRIME_NAME.fullmatch(name.strip().lstrip("\ufeff"))
        if not match:
            raise ValueError(f"invalid prime knot name: {name!r}")
        mirror, crossings, family, index = match.groups()
        return f"{mirror.lower()}K{crossings}{family.lower()}{index}"

    @staticmethod
    def _split_composite(name: str) -> list[str]:
        if not isinstance(name, str):
            raise TypeError("a knot name must be a string")
        parts = [part.strip() for part in name.split(",")]
        if not parts or any(not part for part in parts):
            raise ValueError("a composite name must contain non-empty prime names")
        return parts

    def is_amphichiral_prime(self, raw_prime_name: str) -> bool:
        canonical = self._canonical_prime_name(raw_prime_name).removeprefix("m")
        tabulated = self.name1_to_name2.get(canonical)
        return tabulated in self.amphichiral_names if tabulated is not None else False

    def simplify_prime_name(self, prime_name: str) -> str:
        canonical = self._canonical_prime_name(prime_name)
        raw_name = canonical.removeprefix("m")
        return raw_name if self.is_amphichiral_prime(raw_name) else canonical

    @staticmethod
    def get_mirror_for_prime(canonical: str) -> str:
        return canonical[1:] if canonical.startswith("m") else "m" + canonical

    def regularfy_prime_name(self, knot_name: str) -> str:
        canonical = self._canonical_prime_name(knot_name)
        base_name = canonical.removeprefix("m")
        return self.get_mirror_for_prime(canonical) if base_name in self.need_mirror else canonical

    def regularfy_knot_name(self, knot_name: str) -> str:
        parts = [self.regularfy_prime_name(part) for part in self._split_composite(knot_name)]
        return ",".join(sorted(parts))

    def simplify_knot_name(self, knot_name: str) -> str:
        parts = [self.simplify_prime_name(part) for part in self._split_composite(knot_name)]
        return ",".join(sorted(parts))

    def normalize(self, knot_name: str) -> str:
        return self.simplify_knot_name(self.regularfy_knot_name(knot_name))


_CHECKER = AmphichiralChecker()


def knotname_reg(knot_name: str) -> str:
    """Return the canonical organization-wide spelling of *knot_name*."""

    return _CHECKER.normalize(knot_name)


if __name__ == "__main__":
    print(knotname_reg("mk4a1,mk6a1,mk6a3"))
