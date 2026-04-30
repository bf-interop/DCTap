"""Pytest fixtures for DCTap to SHACL conversion testing."""

import csv
from pathlib import Path
from typing import Callable

TEST_DIRECTORY = Path(__file__).parent


def load_params(csv_name):
    with open(TEST_DIRECTORY / csv_name) as f:
        return [(row[0], int(row[1]), int(row[2])) for row in csv.reader(f) if row[0] != "rdf_file_path"]

import pytest
from dctap2shacl import DCTap2SHACLTransformer
from rdflib import Graph


@pytest.fixture
def violation_query():
    return """
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT (COUNT(DISTINCT ?result) AS ?count)
WHERE {
    ?result sh:resultSeverity sh:Violation .
}
"""


@pytest.fixture
def warning_query():
    return """
PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT (COUNT(DISTINCT ?result) AS ?count)
WHERE {
    ?result sh:resultSeverity sh:Warning .
}
"""


@pytest.fixture
def dctap_to_shacl() -> Callable[[str], Graph]:
    """
    Factory fixture that converts a DCTap TSV file to a SHACL rdflib Graph.

    This fixture returns a function that takes a TSV filename (or relative path)
    and converts it to a SHACL validation graph. The function automatically
    searches for the file in the Monograph DCTAP and Serials DCTAP directories.

    Args:
        tsv_filename: Name or relative path of the DCTap TSV file.
                      Examples: "Monograph_Work_Text.tsv",
                               "Monograph DCTAP/Monograph_Work_Text.tsv",
                               "Serials DCTAP/Serial_Work_Text.tsv"

    Returns:
        rdflib.Graph: SHACL validation graph

    Example:
        def test_monograph_work_validation(dctap_to_shacl):
            shacl_graph = dctap_to_shacl("Monograph_Work_Text.tsv")
            assert len(shacl_graph) > 0

        def test_with_full_path(dctap_to_shacl):
            shacl_graph = dctap_to_shacl("Monograph DCTAP/Monograph_Work_Text.tsv")
            assert len(shacl_graph) > 0
    """

    def _convert(tsv_filename: str) -> Graph:
        """Convert a DCTap TSV file to SHACL graph."""
        # Get the project root (parent of tests directory)
        project_root = Path(__file__).parent.parent

        # If the filename includes a directory path, use it directly
        if "/" in tsv_filename or "\\" in tsv_filename:
            tsv_path = project_root / tsv_filename
        else:
            # Search for the file in common locations
            possible_paths = [
                project_root / "Monograph DCTAP" / tsv_filename,
                project_root / "Serials DCTAP" / tsv_filename,
                project_root / tsv_filename,
            ]

            tsv_path = None
            for path in possible_paths:
                if path.exists():
                    tsv_path = path
                    break

            if tsv_path is None:
                raise FileNotFoundError(
                    f"DCTap file '{tsv_filename}' not found in Monograph DCTAP, "
                    f"Serials DCTAP, or project root directories"
                )

        # Convert to SHACL graph
        transformer = DCTap2SHACLTransformer()
        transformer.run(str(tsv_path))
        return transformer.graph

    return _convert
