"""Command-line interface for khovanov-indexer-pipeline."""

import argparse
import subprocess

from khovanov_indexer_pipeline import khovanov_indexer_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Identify a closed molecular chain through Khovanov homology."
    )
    parser.add_argument("file", help="LAMMPS molecular data file")
    parser.add_argument("--java", help="path or command name for Java")
    parser.add_argument("--projection-timeout", type=float, default=120.0)
    parser.add_argument("--index-timeout", type=float, default=120.0)
    parser.add_argument("--max-heap", default="16g")
    args = parser.parse_args(argv)
    try:
        for name in khovanov_indexer_pipeline(
            args.file,
            java_path=args.java,
            projection_timeout=args.projection_timeout,
            index_timeout=args.index_timeout,
            max_heap=args.max_heap,
        ):
            print(name)
    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        TypeError,
        ValueError,
        RuntimeError,
    ) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
