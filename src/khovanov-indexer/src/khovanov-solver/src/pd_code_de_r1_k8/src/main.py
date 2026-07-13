"""Command-line and compatibility API for PD-code simplification."""

from ast import literal_eval
import sys

from pd_simplify import simplify_pd_code


def de_r1_k8(pd_code0: list[list[int]]) -> list[list[int]]:
    """Remove all Reidemeister-I and nugatory crossings."""

    return simplify_pd_code(pd_code0)


def main() -> int:
    text = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not text:
        raise ValueError("expected a PD-code literal on standard input")
    pd_code = literal_eval(text)
    print(de_r1_k8(pd_code))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
