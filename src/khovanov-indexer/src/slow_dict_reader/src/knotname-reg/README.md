# knotname-reg

Normalize prime and composite knot names, including mirror conventions,
amphichiral knots, and the writhe corrections used by this organization.

## Supported names

Prime names use the form `[m]K<c>a<i>` or `[m]K<c>n<i>`, for example `K7a7`
or `mK8n2`. Input is case-insensitive and output uses canonical casing.
Composite knots are comma-separated prime names; their components are sorted
without removing multiplicity.

## Command-line usage

```bash
echo "mk6a3,mk4a1" | python src/main.py
```

Output:

```text
K4a1,K6a3
```

## Python API

```python
from src.AmphichiralChecker import knotname_reg

assert knotname_reg("K7A7") == "mK7a7"
```

## Algorithm and data

`src/data/need_mirror.txt` records names whose organization-wide convention
requires toggling the mirror prefix. `name_pair.txt` maps canonical names to
tabulation names, and `amphichiral_list.txt` identifies knots for which the
mirror prefix is redundant. Data files are loaded once per checker instance.

Invalid or empty names raise `ValueError`; non-string values raise `TypeError`.
The normalizer does not silently accept malformed names.

## Development

Python 3.10 or newer and the standard library are sufficient. Run:

```bash
python -m unittest discover -s tests -v
```

