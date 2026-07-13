"""Command-line interface for khovanov-solver."""

import argparse
import subprocess
import sys

from kho_solver import kho_solver


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read a knot PD code from stdin and print its integral Khovanov homology."
    )
    parser.add_argument("--java", help="path or command name for Java")
    parser.add_argument("--timeout", type=float, help="maximum JavaKh runtime in seconds")
    parser.add_argument("--max-heap", default="16g", help="Java heap limit, for example 4g")
    args = parser.parse_args(argv)
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        parser.exit(2, "error: expected a PD-code literal on standard input\n")
    try:
        print(
            kho_solver(
                raw,
                java_path=args.java,
                timeout=args.timeout,
                max_heap=args.max_heap,
            )
        )
    except (FileNotFoundError, TypeError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
