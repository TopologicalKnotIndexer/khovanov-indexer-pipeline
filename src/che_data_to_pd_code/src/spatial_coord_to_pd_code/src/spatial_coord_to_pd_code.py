"""Convert a closed spatial polygon to a PD code with the bundled C++ engine."""

from ast import literal_eval
from collections import Counter
from pathlib import Path
import math
import os
import shutil
import stat
import subprocess


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "knot-pdcode_src" / "main.cpp"
EXECUTABLE = HERE / ("knot-pdcode.exe" if os.name == "nt" else "knot-pdcode")
SAMPLE_DATA = HERE / "sample_data.txt"


def _compiler() -> str:
    requested = os.environ.get("CXX", "g++")
    resolved = shutil.which(requested)
    if resolved:
        return resolved
    path = Path(requested)
    if path.is_file():
        return str(path.resolve())
    raise FileNotFoundError("a C++17 compiler was not found; set CXX or install g++")


def _build_engine() -> None:
    result = subprocess.run(
        [_compiler(), "-std=c++17", "-O2", "-o", str(EXECUTABLE), str(SOURCE)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0 or not EXECUTABLE.is_file():
        raise RuntimeError(f"could not build knot-pdcode:\n{result.stderr}")


def _validate_coordinates(spatial_coord: list[list[float]]) -> None:
    if not isinstance(spatial_coord, list):
        raise TypeError("spatial_coord must be a list")
    for point in spatial_coord:
        if not isinstance(point, list) or len(point) != 3:
            raise ValueError("every point must be a three-item list")
        for coordinate in point:
            if isinstance(coordinate, bool) or not isinstance(coordinate, (int, float)):
                raise TypeError("coordinates must be finite integers or floats")
            if not math.isfinite(coordinate):
                raise ValueError("coordinates must be finite")


def _serialize_coordinates(spatial_coord: list[list[float]]) -> str:
    lines = [str(len(spatial_coord))]
    lines.extend("%.20f %.20f %.20f" % tuple(point) for point in spatial_coord)
    return "\n".join(lines) + "\n"


def _validate_pd_output(value: object) -> list[list[int]]:
    if not isinstance(value, list):
        raise ValueError("the C++ engine did not return a list")
    labels: list[int] = []
    for crossing in value:
        if not isinstance(crossing, list) or len(crossing) != 4:
            raise ValueError("the C++ engine returned a malformed crossing")
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int):
                raise ValueError("the C++ engine returned a non-integer label")
            labels.append(label)
    if any(count != 2 for count in Counter(labels).values()):
        raise ValueError("the C++ engine returned labels that do not occur twice")
    return value


def spatial_coord_to_pd_code(spatial_coord: list[list[float]]) -> list[list[int]]:
    """Project a closed polygon and return the smallest PD code found."""

    _validate_coordinates(spatial_coord)
    if not EXECUTABLE.is_file():
        _build_engine()
    if os.name != "nt":
        EXECUTABLE.chmod(EXECUTABLE.stat().st_mode | stat.S_IXUSR)

    result = subprocess.run(
        [str(EXECUTABLE)],
        input=_serialize_coordinates(spatial_coord),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"knot-pdcode failed with exit code {result.returncode}:\n{result.stderr}")
    try:
        parsed = literal_eval(result.stdout.strip())
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"knot-pdcode returned invalid output: {result.stdout!r}") from exc
    return _validate_pd_output(parsed)


def _get_sample_data() -> list[list[float]]:
    points: list[list[float]] = []
    for line in SAMPLE_DATA.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            points.append([float(value) for value in stripped.split()])
    _validate_coordinates(points)
    return points


if __name__ == "__main__":
    print(spatial_coord_to_pd_code(_get_sample_data()))
