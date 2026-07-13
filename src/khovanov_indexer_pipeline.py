"""End-to-end molecular-data to Khovanov-candidate pipeline."""

from os import PathLike

from from_file_to_pd_code import from_file_to_pd_code
from from_pd_code_to_knot_name import from_pd_code_to_knot_name


def khovanov_indexer_pipeline(
    molecular_file: str,
    *,
    java_path: str | PathLike[str] | None = None,
    projection_timeout: float = 120.0,
    index_timeout: float = 120.0,
    max_heap: str = "16g",
) -> list[str]:
    """Convert a molecular cycle and return all matching catalog names."""

    pd_code = from_file_to_pd_code(molecular_file, timeout=projection_timeout)
    return from_pd_code_to_knot_name(
        pd_code,
        java_path=java_path,
        timeout=index_timeout,
        max_heap=max_heap,
    )
