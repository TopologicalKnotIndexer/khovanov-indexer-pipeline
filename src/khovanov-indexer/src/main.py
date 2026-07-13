"""Command-line interface for khovanov-indexer."""

from ast import literal_eval
import argparse
import subprocess
import sys

from khovanov_indexer import khovanov_indexer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Identify catalogued knots by integral Khovanov homology."
    )
    parser.add_argument("--java", help="path or command name for Java")
    parser.add_argument("--timeout", type=float, help="maximum JavaKh runtime in seconds")
    parser.add_argument("--max-heap", default="16g", help="Java heap limit, for example 4g")
    args = parser.parse_args(argv)
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        parser.exit(2, "error: expected a PD-code literal on standard input\n")
    try:
        pd_code = literal_eval(raw)
        if not isinstance(pd_code, list):
            raise TypeError("a PD code must be a list")
        for name in khovanov_indexer(
            pd_code,
            java_path=args.java,
            timeout=args.timeout,
            max_heap=args.max_heap,
        ):
            print(name)
    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        SyntaxError,
        TypeError,
        ValueError,
        RuntimeError,
    ) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
