"""Run the bundled Khovanov indexer as a local program."""

from pathlib import Path
import os
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
INDEXER_MAIN = SOURCE_DIR / "khovanov-indexer" / "src" / "main.py"


def from_pd_code_to_knot_name(
    pd_code: list[list[int]],
    *,
    java_path: str | os.PathLike[str] | None = None,
    timeout: float = 120.0,
    max_heap: str = "16g",
) -> list[str]:
    """Return all catalog names matching the PD code's Khovanov homology."""

    if not isinstance(pd_code, list):
        raise TypeError("pd_code must be a list")
    if not INDEXER_MAIN.is_file():
        raise FileNotFoundError(INDEXER_MAIN)
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    command = [
        sys.executable,
        str(INDEXER_MAIN),
        "--timeout",
        str(timeout),
        "--max-heap",
        max_heap,
    ]
    if java_path is not None:
        command.extend(["--java", os.fspath(java_path)])
    completed = subprocess.run(
        command,
        input=repr(pd_code),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout + 10,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"bundled Khovanov indexer failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]
