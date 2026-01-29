import pathlib

import pytest
import rdflib

from pyshacl import validate

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 0, 0),
        ("loc/monograph/22932823.cbd.rdf", 0, 0),
        ("loc/monograph/23703536.cbd.rdf", 0, 0),
        ("loc/monograph/22483233.cbd.rdf", 0, 0),
        ("loc/monograph/23694998.cbd.rdf", 0, 0),
    ],
)
def test_text_works(rdf_file_path: str, violations: int, warnings: int, dctap_to_shacl):
    """Tests BIBFRAME Text Works"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    text_graph = dctap_to_shacl("Monograph_Work_Text.tsv")
    admin_metadata_graph = dctap_to_shacl("Monograph_AdminMetadata.tsv")
    shacl_graph = admin_metadata_graph + text_graph
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
        ("loc/monograph/12516952.cbd.rdf", 0, 0),
        ("loc/monograph/22932823.cbd.rdf", 0, 0),
        ("loc/monograph/23703536.cbd.rdf", 0, 0),
        ("loc/monograph/22483233.cbd.rdf", 0, 0),
        ("loc/monograph/23694998.cbd.rdf", 0, 0),
    ],
)
def test_print_instances(
    rdf_file_path: str, violations: int, warnings: int, dctap_to_shacl
):
    """Tests BIBFRAME Print Instances"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    print_graph = dctap_to_shacl("Monograph_Instance_Print.tsv")
    admin_metadata_graph = dctap_to_shacl("Monograph_AdminMetadata.tsv")
    shacl_graph = admin_metadata_graph + print_graph
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
