"""Compute Khovanov homology with the bundled JavaKh bytecode."""

from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile

from de_k8_r1 import de_k8_r1
from input_sanity import input_sanity


SOURCE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SOURCE_DIR / "javakh_ori_temp"
JAVA_MAIN = "org.katlas.JavaKh.JavaKh"
JARS = (
    "log4j-1.2.12.jar",
    "commons-io-1.2.jar",
    "commons-cli-1.0.jar",
    "commons-logging-1.1.jar",
)
UNKNOT_HOMOLOGY = "q^-1*t^0*Z[0] + q^1*t^0*Z[0]"


def _find_java(explicit: str | os.PathLike[str] | None = None) -> str:
    candidate = os.fspath(explicit) if explicit is not None else "java"
    resolved = shutil.which(candidate)
    if resolved:
        return resolved
    path = Path(candidate)
    if path.is_file():
        return str(path.resolve())
    raise FileNotFoundError(
        f"Java executable not found: {candidate}; install a JDK/JRE, put "
        "'java' on PATH, or pass java_path"
    )


def _classpath() -> str:
    entries = [TEMPLATE_DIR, *(TEMPLATE_DIR / "jars" / name for name in JARS)]
    missing = [str(path) for path in entries if not path.exists()]
    if missing:
        raise FileNotFoundError(f"bundled JavaKh files are missing: {missing}")
    return os.pathsep.join(str(path) for path in entries)


def _pd_code_wrapper(pd_code: list[list[int]]) -> str:
    crossings = ["X" + str(crossing) for crossing in pd_code]
    return "PD[" + ", ".join(crossings) + "]"


def _parse_javakh_output(stdout: str) -> str:
    candidates = [value.strip() for value in re.findall(r'"([^"\r\n]+)"', stdout)]
    valid = [value for value in candidates if value.startswith("q^")]
    if not valid:
        excerpt = stdout.strip()[-500:]
        raise RuntimeError(f"JavaKh returned no quoted homology value: {excerpt!r}")
    return valid[-1]


def run_javakh_with_shell(
    pd_code: list[list[int]],
    *,
    java_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
    max_heap: str = "16g",
) -> str:
    """Run JavaKh directly; the legacy function name is retained for callers."""

    if not re.fullmatch(r"[1-9]\d*[mMgG]", max_heap):
        raise ValueError("max_heap must look like '512m', '4g', or '16g'")
    command = [
        _find_java(java_path),
        f"-Xmx{max_heap}",
        "-Djava.awt.headless=true",
        "-classpath",
        _classpath(),
        JAVA_MAIN,
    ]
    with tempfile.TemporaryDirectory(prefix=f"kho_solver_{os.getpid()}_") as directory:
        Path(directory, "PD.txt").write_text(_pd_code_wrapper(pd_code), encoding="utf-8")
        completed = subprocess.run(
            command,
            cwd=directory,
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
            f"JavaKh failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    return _parse_javakh_output(completed.stdout)


def kho_solver(
    all_input: str | list[list[int]],
    *,
    java_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
    max_heap: str = "16g",
) -> str:
    """Return the integral Khovanov homology string for a PD code."""

    pd_code = de_k8_r1(input_sanity(all_input))
    if not pd_code:
        return UNKNOT_HOMOLOGY
    return run_javakh_with_shell(
        pd_code, java_path=java_path, timeout=timeout, max_heap=max_heap
    )


if __name__ == "__main__":
    print(kho_solver([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))
