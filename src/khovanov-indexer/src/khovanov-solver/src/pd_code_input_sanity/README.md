# pd-code-input-sanity

Safely parse a textual PD code and check its weak structural invariants.

## What is checked

`input_sanity()` accepts either a string containing a Python literal or an
already constructed list. It verifies that:

- the outer value is a list;
- every crossing is a four-item list;
- every arc label is an integer (booleans are rejected); and
- every arc label occurs exactly twice.

The function deliberately does **not** prove planarity, connectedness, or a
particular orientation convention. Use a strong geometric validator when
those properties are required.

## Usage

```python
from src.pd_code_input_sanity import input_sanity

pd_code = input_sanity("[[1, 2, 2, 1]]")
print(pd_code)
```

List input is copied before it is returned, so validation does not introduce
an alias to caller-owned nested lists.

## Error handling and security

Text is parsed with `ast.literal_eval`; arbitrary expressions and function
calls are never executed. Malformed containers and label types raise
`TypeError`, while malformed crossing lengths, literals, or occurrence counts
raise `ValueError`. Validation uses explicit checks and therefore remains
active when Python is run with optimization enabled.

## Development

The project requires only Python 3.10 or newer and the standard library. Run
the regression suite with:

```bash
python -m unittest discover -s tests -v
```
