import pathlib

import pytest

from pyshacl import validate

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 5, 2),
        ("loc/monograph/22932823.cbd.rdf", 6, 2),
        ("loc/monograph/23703536.cbd.rdf", 0, 3),
        ("loc/monograph/22483233.cbd.rdf", 0, 3),
        ("loc/monograph/23694998.cbd.rdf", 0, 3),
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
    shacl_graph = dctap_to_shacl("Monograph_Work_Text.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 3, 1),
        ("loc/monograph/22932823.cbd.rdf", 2, 1),
        ("loc/monograph/23703536.cbd.rdf", 0, 1),
        ("loc/monograph/22483233.cbd.rdf", 0, 1),
        ("loc/monograph/23694998.cbd.rdf", 0, 1),
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
    shacl_graph = dctap_to_shacl("Monograph_Instance_Print.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/monograph/12516952.cbd.rdf", 24, 0),
        ("loc/monograph/22932823.cbd.rdf", 16, 0),
        ("loc/monograph/23703536.cbd.rdf", 16, 0),
        ("loc/monograph/22483233.cbd.rdf", 16, 0),
        ("loc/monograph/23694998.cbd.rdf", 16, 0),
    ],
)
def test_monograph_admin_metadata(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Monograph Admin Metadata"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    shacl_graph = dctap_to_shacl("Monograph_AdminMetadata.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count
