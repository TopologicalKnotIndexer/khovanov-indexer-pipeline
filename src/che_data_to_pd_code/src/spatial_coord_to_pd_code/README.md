# spatial-coord-to-pd-code

Convert a closed polygonal curve in three-dimensional space to a planar
diagram (PD) code.

## Requirements

- Python 3.10 or newer.
- A C++17 compiler (`g++` by default, or set the `CXX` environment variable).

The repository includes the complete C++ source and builds a native executable
on first use. It no longer depends on a prebuilt Linux x86-64 binary or Bash.

## Usage

```bash
echo '[[0, 0, 0], [1, 0, 0], [0, 1, 0]]' | python src/main.py
```

The CLI expects a Python literal containing a list of `[x, y, z]` points. The
same operation is available from Python:

```python
from src.spatial_coord_to_pd_code import spatial_coord_to_pd_code

pd_code = spatial_coord_to_pd_code([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
```

Points must be finite numbers. The zero-through-three-point case represents a
zero-crossing curve and returns `[]`.

## Algorithm

The C++ engine centers the polygon, samples bounded random projection
directions, rejects degenerate projections, records segment intersections and
their over/under heights, and emits the smallest crossing diagram found. The
search is bounded; if no regular projection is found, the program returns an
error instead of looping forever.

The output parser uses `ast.literal_eval` and validates every crossing and arc
occurrence before returning it.

## Development

Compile and run the bundled sample with:

```bash
python src/spatial_coord_to_pd_code.py
```

The build uses only files committed in this repository.

