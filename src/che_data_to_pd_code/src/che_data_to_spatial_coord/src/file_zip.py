"""Extract an ordered coordinate cycle from validated LAMMPS atom/bond data."""

from pathlib import Path
import math
import struct

try:
    from .file_checker import content_check, read_file
except ImportError:  # Direct execution from the src directory.
    from file_checker import content_check, read_file


def parse_atoms(atoms_list: list[list[str]]) -> dict[int, list[float]]:
    atoms: dict[int, list[float]] = {}
    for raw_id, raw_x, raw_y, raw_z in atoms_list:
        atom_id = int(raw_id)
        if atom_id in atoms:
            raise ValueError(f"duplicate atom id: {atom_id}")
        point = [float(raw_x), float(raw_y), float(raw_z)]
        if not all(math.isfinite(value) for value in point):
            raise ValueError(f"non-finite coordinate for atom {atom_id}")
        atoms[atom_id] = point
    return atoms


def add_edge(graph: dict[int, set[int]], left: int, right: int) -> None:
    if left == right:
        raise ValueError("self-bonds are not valid cycle edges")
    graph.setdefault(left, set()).add(right)
    graph.setdefault(right, set()).add(left)


def parse_bonds(bonds_list: list[list[str]]) -> dict[int, set[int]]:
    graph: dict[int, set[int]] = {}
    seen_bonds: set[int] = set()
    for raw_bond, _, raw_left, raw_right in bonds_list:
        bond_id = int(raw_bond)
        if bond_id in seen_bonds:
            raise ValueError(f"duplicate bond id: {bond_id}")
        seen_bonds.add(bond_id)
        add_edge(graph, int(raw_left), int(raw_right))
    return graph


def get_loop(graph: dict[int, set[int]]) -> list[int]:
    """Return a deterministic traversal of a single undirected cycle."""

    if not graph:
        return []
    invalid = {node: len(neighbors) for node, neighbors in graph.items() if len(neighbors) != 2}
    if invalid:
        raise ValueError(f"the bond graph is not 2-regular: {invalid}")

    start = min(graph)
    order = [start]
    previous: int | None = None
    current = start
    while True:
        candidates = sorted(graph[current] - ({previous} if previous is not None else set()))
        next_node = candidates[0]
        if next_node == start:
            break
        if next_node in order:
            raise ValueError("the bond graph contains a short cycle")
        order.append(next_node)
        previous, current = current, next_node
    if len(order) != len(graph):
        raise ValueError("the bond graph contains multiple components")
    return order


def content_pos_list(
    atoms_list: list[list[str]], bonds_list: list[list[str]]
) -> list[list[float]]:
    atoms = parse_atoms(atoms_list)
    graph = parse_bonds(bonds_list)
    if set(atoms) != set(graph):
        missing_coordinates = sorted(set(graph) - set(atoms))
        missing_bonds = sorted(set(atoms) - set(graph))
        raise ValueError(
            f"atom/bond ids differ; missing coordinates={missing_coordinates}, "
            f"missing bonds={missing_bonds}"
        )
    return [atoms[atom_id] for atom_id in get_loop(graph)]


def zip_pos_list(pos_list: list[list[float]]) -> bytes:
    payload = bytearray()
    for point in pos_list:
        if len(point) != 3:
            raise ValueError("every coordinate must contain x, y, z")
        payload.extend(struct.pack("<ddd", *point))
    return bytes(payload)


def get_pos_list(input_path: str) -> list[list[float]]:
    error, atoms, bonds = content_check(read_file(input_path))
    if error:
        raise ValueError(error)
    return content_pos_list(atoms, bonds)


def compress_file(input_path: str, output_path: str) -> None:
    Path(output_path).write_bytes(zip_pos_list(get_pos_list(input_path)))


if __name__ == "__main__":
    sample = Path(__file__).resolve().parent / "data.random_knot_widened_L1000_K0_melt_limit_1"
    compress_file(str(sample), "tmp.bin")
