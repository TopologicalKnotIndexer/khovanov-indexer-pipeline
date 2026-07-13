# slow_dict_reader

Parse the text record format used by TopologicalKnotIndexer invariant catalogs
and return a mapping from invariant text to canonical knot names.

Despite the historical repository name, parsing is linear in the input size.
The project is independently cloneable and uses ordinary tracked data files;
it does not require Git submodules or third-party Python packages.

## Record format

Each non-empty, non-comment line must have this form:

```text
[INVARIANT|KNOT_NAME]
```

For example:

```text
[1|K0a1]
[-L^4 + L^2*M^2 - 2*L^2|K3a1]
```

Lines beginning with `#` are ignored. The invariant is retained as text. Knot
names are normalized for casing, mirror conventions, amphichiral knots, and
composite-factor ordering. Duplicate canonical names for the same invariant
are removed while preserving first-seen order. Invalid records report their
line number instead of relying on disabled-by-optimization assertions.

## Python API

```python
from slow_dict_reader import slow_dict_reader, slow_dict_reader_raw

mapping = slow_dict_reader("data/sorted_HOMFLY-PT.txt")
same_mapping = slow_dict_reader_raw("[1|K0a1]\n")
```

Files are decoded as UTF-8 with optional BOM support. Missing files raise
`FileNotFoundError`.

## Command-line usage

The CLI reads records from standard input and writes JSON:

```bash
python src/slow_dict_reader.py < data/sorted_HOMFLY-PT.txt
```

Malformed input is reported on standard error with exit status 2.

## Bundled normalization data

The former `knotname-reg` dependency is stored under `src/knotname-reg` as
regular tracked files. The runtime owns a static normalizer and reads its three
reference tables directly; it does not dynamically modify `sys.path`. The
audited source revision is recorded in `VENDORED_DEPENDENCIES.md`.

## Development

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance. See
`LICENSE` for this repository's license.
