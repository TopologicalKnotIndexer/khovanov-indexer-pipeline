"""Normalize Hoste-Thistlethwaite-style knot names."""

from pathlib import Path
import re


_PRIME_NAME = re.compile(r"^(m?)k(\d+)([an])(\d+)$", re.IGNORECASE)


class AmphichiralChecker:
    """Apply writhe corrections and remove redundant mirrors of amphichiral knots."""

    def __init__(self) -> None:
        data_dir = Path(__file__).resolve().parent / "data"
        self.name1_to_name2 = self._load_name_pairs(data_dir / "name_pair.txt")
        self.amphichiral_names = self._load_lines(data_dir / "amphichiral_list.txt")
        self.need_mirror = {
            self._canonical_prime_name(name).removeprefix("m")
            for name in self._load_lines(data_dir / "need_mirror.txt")
        }

    @staticmethod
    def _load_lines(path: Path) -> set[str]:
        return {
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    @classmethod
    def _load_name_pairs(cls, path: Path) -> dict[str, str]:
        result: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
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

    def is_prime_knot_name_format(self, knotname: str) -> bool:
        try:
            self._canonical_prime_name(knotname)
            return True
        except (TypeError, ValueError):
            return False

    def simplify_prime_name(self, prime_name: str) -> str:
        canonical = self._canonical_prime_name(prime_name)
        raw_name = canonical.removeprefix("m")
        return raw_name if self.is_amphichiral_prime(raw_name) else canonical

    def simplify_knot_name(self, knot_name: str) -> str:
        parts = [self.simplify_prime_name(part) for part in self._split_composite(knot_name)]
        return ",".join(sorted(parts))

    def erase_m_if_possible(self, knot_name_list: list[str]) -> list[str]:
        if not isinstance(knot_name_list, list):
            raise TypeError("knot_name_list must be a list")
        return sorted({self.simplify_knot_name(name) for name in knot_name_list})

    def get_mirror_for_prime(self, knot_name: str) -> str:
        canonical = self._canonical_prime_name(knot_name)
        return canonical[1:] if canonical.startswith("m") else "m" + canonical

    def regularfy_prime_name(self, knot_name: str) -> str:
        canonical = self._canonical_prime_name(knot_name)
        base_name = canonical.removeprefix("m")
        return self.get_mirror_for_prime(canonical) if base_name in self.need_mirror else canonical

    def regularfy_knot_name(self, knot_name: str) -> str:
        parts = [self.regularfy_prime_name(part) for part in self._split_composite(knot_name)]
        return ",".join(sorted(parts))


def knotname_reg(knot_name: str) -> str:
    """Return the canonical organization-wide spelling of a knot name."""

    checker = AmphichiralChecker()
    corrected = checker.regularfy_knot_name(knot_name)
    return checker.simplify_knot_name(corrected)


if __name__ == "__main__":
    print(knotname_reg("mk6a3,mk4a1"))
    print(knotname_reg("k7a7"))
