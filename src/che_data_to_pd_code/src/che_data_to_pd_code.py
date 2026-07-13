"""Convert a molecular LAMMPS data file to a knot PD code."""

from pathlib import Path
import argparse

from to_pd_code import to_pd_code
from to_spatial_coord import to_spatial_coord


def che_data_to_pd_code(che_data_file_path: str) -> list[list[int]]:
    """Read *che_data_file_path* and return its projected knot PD code."""

    path = Path(che_data_file_path)
    if not path.is_file():
        raise FileNotFoundError(path)
    return to_pd_code(to_spatial_coord(str(path)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a LAMMPS molecular data file to a knot PD code."
    )
    parser.add_argument("input", help="path to the LAMMPS data file")
    args = parser.parse_args(argv)
    try:
        print(che_data_to_pd_code(args.input))
    except (FileNotFoundError, TypeError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
