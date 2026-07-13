# che-data-to-spatial-coord

Extract an ordered closed polygon from the LAMMPS data-file subset used by the
TopologicalKnotIndexer molecular pipeline.

## Input contract

The file must contain `Atoms` and `Bonds` sections. Atom rows may use either
the four-column compact form or the nine-column legacy form. Bond rows use the
standard four columns (`bond-id`, type, left atom, right atom). The atom and
bond counts must agree with the header, and the bond graph must be one
connected 2-regular cycle.

Invalid counts, duplicate identifiers, missing endpoints, non-finite
coordinates, paths, or multiple cycles raise explicit exceptions.

## Usage

```python
from src.che_data_to_spatial_coord import che_data_to_spatial_coord

points = che_data_to_spatial_coord("molecule.data")
print(points[0])  # [x, y, z]
```

The traversal starts at the smallest atom identifier and chooses the smaller
of its two neighbors, which makes output deterministic without assuming that
atom `1` exists.

## Binary export

`src.file_zip.zip_pos_list()` encodes points as little-endian IEEE-754 triples
(`x`, `y`, `z`), 24 bytes per point. `compress_file()` writes that payload.

## Development

Only Python 3.10 or newer and the standard library are required. Validate the
committed 1000-point sample and run regression tests with:

```bash
python src/che_data_to_spatial_coord.py
python -m unittest discover -s tests -v
```
