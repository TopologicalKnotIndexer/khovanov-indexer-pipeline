# khovanov-solver

Compute integral Khovanov homology from a knot planar diagram (PD) code using
the JavaKh bytecode committed in this repository.

## Requirements

- Python 3.10 or newer
- A Java runtime (`java` on `PATH`, or pass an explicit executable path)

The repository is independently cloneable. Organization-owned helper sources
are ordinary tracked files, not Git submodules. Bash and symbolic-link support
are not required.

## Command-line usage

```bash
echo '[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]' | python src/main.py
```

The Java executable, timeout, and heap limit can be controlled explicitly:

```bash
python src/main.py --java /path/to/java --timeout 120 --max-heap 4g
```

Errors are written to standard error and produce a nonzero exit status.

## Python API

```python
from kho_solver import kho_solver

homology = kho_solver(pd_code, java_path="java", timeout=120, max_heap="4g")
```

## Algorithm

The input is safely parsed and checked for four-entry crossings, integer arc
labels, and two occurrences of each label. Reidemeister-I and verified
nugatory crossings are removed before evaluation. The unknot has the explicit
result `q^-1*t^0*Z[0] + q^1*t^0*Z[0]` and does not invoke JavaKh.

For other knots, the solver writes JavaKh's `PD[...]` representation to an
isolated temporary directory and starts Java directly with a platform-correct
classpath. The process exit status and quoted homology value are both checked.
Temporary data is removed by `TemporaryDirectory`, including on failures.

The helper snapshots under `src/pd_code_de_r1_k8` and
`src/pd_code_input_sanity` are statically imported; no code changes `sys.path`
or performs Git submodule operations. See `VENDORED_DEPENDENCIES.md` for their
audited revisions.

## Development

```bash
python -m unittest discover -s tests -v
```

The integration test runs the bundled JavaKh backend when `java` is available.
No PyPI publication is performed as part of repository maintenance.
