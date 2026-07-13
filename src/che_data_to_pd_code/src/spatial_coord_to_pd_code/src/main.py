from ast import literal_eval
import sys
from spatial_coord_to_pd_code import spatial_coord_to_pd_code

def main() -> None:
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    inp = literal_eval(raw)
    print(spatial_coord_to_pd_code(inp))

if __name__ == "__main__":
    main()
