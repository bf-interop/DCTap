import pathlib

import pytest

from pyshacl import validate

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 29, 2),
        ("loc/monograph/22932823.cbd.rdf", 22, 2),
        ("loc/monograph/23703536.cbd.rdf", 16, 3),
        ("loc/monograph/22483233.cbd.rdf", 16, 3),
        ("loc/monograph/23694998.cbd.rdf", 16, 3),
    ],
)
def test_text_works(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Text Works"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    text_graph = dctap_to_shacl("Monograph_Work_Text.tsv")
    admin_metadata_graph = dctap_to_shacl("Monograph_AdminMetadata.tsv")
    shacl_graph = admin_metadata_graph + text_graph
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 27, 1),
        ("loc/monograph/22932823.cbd.rdf", 18, 1),
        ("loc/monograph/23703536.cbd.rdf", 16, 1),
        ("loc/monograph/22483233.cbd.rdf", 16, 1),
        ("loc/monograph/23694998.cbd.rdf", 16, 1),
    ],
)
def test_print_instances(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Print Instances"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    print_graph = dctap_to_shacl("Monograph_Instance_Print.tsv")
    admin_metadata_graph = dctap_to_shacl("Monograph_AdminMetadata.tsv")
    shacl_graph = admin_metadata_graph + print_graph
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count
