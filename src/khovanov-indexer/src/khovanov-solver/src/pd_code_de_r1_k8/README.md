# pd-code-de-r1-k8

Remove Reidemeister-I and nugatory crossings from knot or link planar diagram
(PD) codes. This standalone repository was originally extracted from
`khovanov-solver` and has no nested Git dependency.

## Usage

Pass a Python-style PD-code literal on standard input:

```bash
python src/main.py <<<'[[1, 1, 2, 2]]'
```

Output:

```text
[]
```

From Python, add `src` to the import path and call:

```python
from main import de_r1_k8

reduced = de_r1_k8([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]])
```

The function validates that every crossing has four positive integer labels
and that every label occurs exactly twice. It returns a new value and never
mutates its input. Standard input is parsed with `ast.literal_eval`; executable
Python expressions are rejected.

## Algorithm

Repeated-label crossings are removed as Reidemeister-I moves. For the
remaining projection, crossings and arc labels form a bipartite incidence
graph. A crossing is nugatory exactly when deleting its crossing vertex
increases the graph's connected-component count. Removing such a crossing
reconnects the two opposite strands. The result is renumbered by traversing
each link component, and R1 removal is repeated because a nugatory reduction
can expose a new R1 crossing.

This graph formulation depends only on PD incidence, not on a particular arc
numbering, and supports multiple link components. The legacy `de_k8` function
name remains available for downstream compatibility.

## Development

```bash
python -m unittest discover -s tests -v
```

The implementation uses only the Python standard library. No PyPI publication
is performed by this project.
