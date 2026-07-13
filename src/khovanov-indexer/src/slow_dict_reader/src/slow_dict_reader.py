"""Read invariant-to-knot-name records from the organization's text format."""

from pathlib import Path
import json
import sys

try:
    from .knotname_reg import knotname_reg
except ImportError:  # Direct execution from the src directory.
    from knotname_reg import knotname_reg


def slow_dict_reader_raw(content: str) -> dict[str, list[str]]:
    """Parse ``[INVARIANT|KNOT_NAME]`` records from *content*.

    Names are normalized and duplicate normalized names are removed while
    retaining their first-seen order for each invariant.
    """

    if not isinstance(content, str):
        raise TypeError("content must be a string")
    result: dict[str, list[str]] = {}
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip().lstrip("\ufeff")
        if not line or line.startswith("#"):
            continue
        if not (line.startswith("[") and line.endswith("]")):
            raise ValueError(f"line {line_number}: expected [INVARIANT|KNOT_NAME]")
        body = line[1:-1]
        if "|" not in body:
            raise ValueError(f"line {line_number}: missing '|' separator")
        invariant, raw_name = (part.strip() for part in body.split("|", 1))
        if not invariant or not raw_name:
            raise ValueError(f"line {line_number}: invariant and knot name must be non-empty")
        try:
            name = knotname_reg(raw_name)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
        names = result.setdefault(invariant, [])
        if name not in names:
            names.append(name)
    return result


def slow_dict_reader(filepath: str) -> dict[str, list[str]]:
    """Read and parse a UTF-8 record file."""

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(path)
    return slow_dict_reader_raw(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    content = sys.stdin.buffer.read().decode("utf-8-sig")
    try:
        result = slow_dict_reader_raw(content)
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
