"""Run the bundled molecular-data converter as a local program."""

from ast import literal_eval
from pathlib import Path
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
CONVERTER_MAIN = SOURCE_DIR / "che_data_to_pd_code" / "src" / "che_data_to_pd_code.py"


def from_file_to_pd_code(filename: str, *, timeout: float = 120.0) -> list[list[int]]:
    """Convert a LAMMPS molecular data file to a validated PD-code list."""

    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(path)
    if not CONVERTER_MAIN.is_file():
        raise FileNotFoundError(CONVERTER_MAIN)
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    completed = subprocess.run(
        [sys.executable, str(CONVERTER_MAIN), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"bundled molecular converter failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    try:
        pd_code = literal_eval(completed.stdout.strip())
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError(
            f"bundled molecular converter returned invalid output: {completed.stdout!r}"
        ) from exc
    if not isinstance(pd_code, list):
        raise RuntimeError("bundled molecular converter did not return a PD-code list")
    return pd_code
