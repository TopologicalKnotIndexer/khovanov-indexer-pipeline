"""Read and validate the LAMMPS data-file subset used by this project."""

from pathlib import Path
import re


IGNORE_FIRST_LINE_CHECK = True
_SECTION = re.compile(r"^(Atoms|Bonds|Velocities|Angles)\b")


def read_file(filename: str) -> list[str]:
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(path)
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _declared_count(header: list[str], kind: str) -> int | None:
    pattern = re.compile(rf"^(\d+)\s+{re.escape(kind)}$")
    for line in header:
        match = pattern.fullmatch(line)
        if match:
            return int(match.group(1))
    return None


def header_check(content: list[str]) -> str:
    if not content:
        return "empty_header"
    if not IGNORE_FIRST_LINE_CHECK and not content[0].startswith(
        "LAMMPS data file via write_data, version 12"
    ):
        return "front_line_error"
    if _declared_count(content, "atoms") is None:
        return "data_size_line_error"
    return ""


def split_content(content: list[str]) -> tuple[list[str], list[str], list[str]]:
    sections: list[list[str]] = []
    current: list[str] = []
    for line in content:
        if _SECTION.match(line):
            if current:
                sections.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append(current)

    header = sections[0] if sections else []
    atoms = next((section for section in sections if section[0].startswith("Atoms")), [])
    bonds = next((section for section in sections if section[0].startswith("Bonds")), [])
    return header, atoms, bonds


def get_data_body(part_content: list[str]) -> list[list[str]]:
    if not part_content:
        raise ValueError("required LAMMPS section is missing")
    rows: list[list[str]] = []
    for raw_line in part_content[1:]:
        fields = raw_line.split()
        if len(fields) == 4:
            rows.append(fields)
        elif len(fields) == 9:
            rows.append([fields[0], *fields[3:6]])
        else:
            raise ValueError(f"unsupported row shape: {raw_line!r}")
    return rows


def content_check(content: list[str]):
    """Return `(error, atoms, bonds)` while preserving the legacy API."""

    try:
        header, atom_section, bond_section = split_content(content)
        error = header_check(header)
        if error:
            return error, None, None
        atoms = get_data_body(atom_section)
        bonds = get_data_body(bond_section)
        declared_atoms = _declared_count(header, "atoms")
        declared_bonds = _declared_count(header, "bonds")
        if declared_atoms != len(atoms):
            return "atom_count_mismatch", None, None
        if declared_bonds is not None and declared_bonds != len(bonds):
            return "bond_count_mismatch", None, None
        if len(atoms) != len(bonds):
            return "length_not_match", None, None
        return "", atoms, bonds
    except ValueError as exc:
        return f"format_error: {exc}", None, None


if __name__ == "__main__":
    sample = Path(__file__).resolve().parent / "data.random_knot_widened_L1000_K0_melt_limit_1"
    info, atoms, _ = content_check(read_file(str(sample)))
    if info:
        raise ValueError(info)
    print(len(atoms))
