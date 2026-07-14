# khovanov-indexer-pipeline

An end-to-end pipeline from a closed molecular chain in a LAMMPS data file to
candidate knot names identified by integral Khovanov homology.

Khovanov homology is not treated as a complete invariant: the pipeline can
return multiple names, and an empty result means no catalog record matches.

## Requirements

- Python 3.10 or newer
- A C++17 compiler (`g++` by default, or set `CXX`)
- A Java runtime (`java` on `PATH`, or pass an explicit path)

The repository is independently cloneable. All organization dependencies,
native source, catalogs, and JavaKh bytecode are ordinary tracked files—not Git
submodules. Linux, Bash, and symbolic links are not required.

## Command-line usage

```bash
python src/main.py path/to/molecule.data
```

Optional controls:

```text
python src/main.py molecule.data --java /path/to/java --projection-timeout 120 --index-timeout 120 --max-heap 4g
```

Each candidate name is printed on its own line. Missing/malformed molecular
data, compiler errors, backend failures, and timeouts produce a diagnostic and
exit status 2.

## Pipeline

1. Validate LAMMPS `Atoms`/`Bonds` sections and traverse the single 2-regular
   molecular cycle deterministically.
2. Compile the bundled C++17 projection engine on first use and search a bounded
   set of regular projections.
3. Parse and validate the resulting PD code.
4. Remove Reidemeister-I and verified nugatory crossings.
5. Run bundled JavaKh directly with a platform-correct classpath.
6. Look up the homology string in the 1,871-line normalized catalog.

Each bundled stage is invoked as a fixed local program. No runtime code changes
`sys.path` or invokes Git submodule commands. Audited dependency revisions are
listed in `VENDORED_DEPENDENCIES.md`.

## Python API

```python
from khovanov_indexer_pipeline import khovanov_indexer_pipeline

candidates = khovanov_indexer_pipeline(
    "molecule.data", projection_timeout=120, index_timeout=120, max_heap="4g"
)
```

## Development

```bash
python -m unittest discover -s tests -v
```

The end-to-end regression uses a three-atom cycle whose zero-crossing result is
the unknot. No Python packages are installed or published by maintenance.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_khovanov_indexer_pipeline,
  author = {{GGN\_2015}},
  title = {{khovanov-indexer-pipeline}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/khovanov-indexer-pipeline}
}
```
