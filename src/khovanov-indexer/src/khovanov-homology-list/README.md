# Khovanov homology list

A static catalog of Khovanov homology signatures for 1,871 named knots used
by the TopologicalKnotIndexer tools.

## Files and format

- `data/combined_knot_name.txt` lists names in source order.
- `data/khovanov.txt` contains the corresponding homology/name records.
- `data/sorted_khovanov.txt` contains the same records sorted
  lexicographically by homology text.

Records have the form:

```text
[HOMOLOGY|KNOT_NAME]
```

Terms such as `q^5*t^2*Z[0,2]` record the bigrading and torsion data emitted by
the JavaKh-based pipeline. The text is intentionally kept as a stable lookup
key rather than parsed into a project-specific object model.

## Consuming the data

```python
from pathlib import Path

for line in Path("data/khovanov.txt").read_text(encoding="utf-8").splitlines():
    homology, name = line[1:-1].rsplit("|", 1)
```

All three files contain 1,871 lines. No external software is required to read
the committed data.

## License

MIT. See `LICENSE`.

