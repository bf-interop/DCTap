import pathlib

import pytest
import rdflib

from pyshacl import validate

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/serial/11158534.cbd.rdf", 0, 0),
        ("loc/serial/21507607.cbd.rdf", 0, 0),
        ("loc/serial/23326748.cbd.rdf", 0, 0),
        ("loc/serial/23793113.cbd.rdf", 0, 0),
        ("loc/serial/23996113.cbd.rdf", 0, 0),
    ],
)
def test_text_works(rdf_file_path: str, violations: int, warnings: int, dctap_to_shacl):
    """Tests BIBFRAME Serial Works"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    text_graph = dctap_to_shacl("Serial_Work_Text.tsv")
    admin_metadata_graph = dctap_to_shacl("Serial_AdminMetadata.tsv")
    shacl_graph = text_graph + admin_metadata_graph
    results = validate(str(rdf_test_file), shacl_graph)
    assert violations == len(
        [
            r
            for r in results[1].subjects(
                rdflib.SH.resultSeverity, rdflib.SH.Violation, unique=True
            )
        ]
    )
    assert warnings == len(
        [
            r
            for r in results[1].subjects(
                rdflib.SH.resultSeverity, rdflib.SH.Warning, unique=True
            )
        ]
    )


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/serial/11158534.cbd.rdf", 0, 0),
        ("loc/serial/21507607.cbd.rdf", 0, 0),
        ("loc/serial/23326748.cbd.rdf", 0, 0),
        ("loc/serial/23793113.cbd.rdf", 0, 0),
        ("loc/serial/23996113.cbd.rdf", 0, 0),
    ],
)
def test_print_instances(
    rdf_file_path: str, violations: int, warnings: int, dctap_to_shacl
):
    """Tests BIBFRAME Serial Instances"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    print_graph = dctap_to_shacl("Serial_Instance_Electronic.tsv")
    admin_metadata_graph = dctap_to_shacl("Serial_AdminMetadata.tsv")
    shacl_graph = print_graph + admin_metadata_graph
    results = validate(str(rdf_test_file), shacl_graph)
    assert violations == len(
        [
            r
            for r in results[1].subjects(
                rdflib.SH.resultSeverity, rdflib.SH.Violation, unique=True
            )
        ]
    )
    assert warnings == len(
        [
            r
            for r in results[1].subjects(
                rdflib.SH.resultSeverity, rdflib.SH.Warning, unique=True
            )
        ]
    )
