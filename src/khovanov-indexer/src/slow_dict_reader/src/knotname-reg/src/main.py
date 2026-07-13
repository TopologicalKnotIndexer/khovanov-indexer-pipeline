"""Read a knot name from standard input and print its canonical spelling."""

import sys
from AmphichiralChecker import knotname_reg

def main() -> None:
    input_data = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    print(knotname_reg(input_data))

if __name__ == "__main__":
    main()
