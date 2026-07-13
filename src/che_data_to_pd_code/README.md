# che_data_to_pd_code

Convert the closed molecular chain in a LAMMPS data file to a knot planar
diagram (PD) code. The repository contains all Python and C++ source required
by the pipeline and can be cloned and used independently without Git
submodules.

## Requirements

- Python 3.10 or newer
- A C++17 compiler (`g++` by default, or set the `CXX` environment variable)

No third-party Python package is required.

## Command-line usage

```bash
python src/che_data_to_pd_code.py path/to/molecule.data
```

The resulting PD code is written to standard output. Invalid molecular data,
non-cycle bond graphs, non-finite coordinates, compiler failures, and malformed
native-engine output are reported as errors with a nonzero exit status.

## Python API

```python
from che_data_to_pd_code import che_data_to_pd_code

pd_code = che_data_to_pd_code("path/to/molecule.data")
```

## Input contract

The LAMMPS file must contain `Atoms` and `Bonds` sections whose declared counts
match their rows. Atom rows may use the four-column compact form or the
nine-column legacy form. The bond graph must be one connected 2-regular cycle.
Traversal starts at the smallest atom identifier and is deterministic.

## Pipeline and algorithm

1. Parse and validate atom coordinates and bond endpoints.
2. Traverse the unique molecular cycle to obtain ordered 3D coordinates.
3. Build the bundled C++17 projection engine on first use.
4. Search a bounded set of regular projection directions, recording crossing
   order and over/under heights.
5. Safely parse and structurally validate the smallest PD code found.

The native search is bounded and reports failure instead of looping forever.
The former dependency directories under `src/` are now ordinary tracked source
trees. Imports are static; no code modifies `sys.path` or invokes Git submodule
operations. Audited source revisions are recorded in
`VENDORED_DEPENDENCIES.md`.

## Development

Run the parent and bundled dependency tests with:

```bash
python -m unittest discover -s tests -v
python -m unittest discover -s src/che_data_to_spatial_coord/tests -v
python -m unittest discover -s src/spatial_coord_to_pd_code/tests -v
```

No PyPI publication is performed as part of repository maintenance.
