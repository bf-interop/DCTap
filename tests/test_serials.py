import pathlib

import pytest

from pyshacl import validate

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/serial/11158534.cbd.rdf", 0, 8),
        ("loc/serial/21507607.cbd.rdf", 0, 6),
        ("loc/serial/23326748.cbd.rdf", 0, 3),
        ("loc/serial/23793113.cbd.rdf", 0, 3),
        ("loc/serial/23996113.cbd.rdf", 6, 3),
    ],
)
def test_serial_works(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Serial Works"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    shacl_graph = dctap_to_shacl("Serial_Work_Text.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/serial/11158534.cbd.rdf", 0, 8),
        ("loc/serial/21507607.cbd.rdf", 0, 4),
        ("loc/serial/23326748.cbd.rdf", 0, 1),
        ("loc/serial/23793113.cbd.rdf", 0, 2),
        ("loc/serial/23996113.cbd.rdf", 4, 1),
    ],
)
def test_serials_instances(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Serial Instances"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    shacl_graph = dctap_to_shacl("Serial_Instance_Electronic.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count


@pytest.mark.parametrize(
    "rdf_file_path, violations, warnings",
    [
        ("loc/serial/11158534.cbd.rdf", 16, 0),
        ("loc/serial/21507607.cbd.rdf", 24, 0),
        ("loc/serial/23326748.cbd.rdf", 16, 0),
        ("loc/serial/23793113.cbd.rdf", 16, 0),
        ("loc/serial/23996113.cbd.rdf", 32, 0),
    ],
)
def test_serials_admin_metadata(
    rdf_file_path: str,
    violations: int,
    warnings: int,
    dctap_to_shacl,
    violation_query,
    warning_query,
):
    """Tests BIBFRAME Serial Admin Metadata"""
    rdf_test_file = TEST_DIRECTORY / rdf_file_path
    shacl_graph = dctap_to_shacl("Serial_AdminMetadata.tsv")
    results = validate(str(rdf_test_file), shacl_graph=shacl_graph, allow_warnings=True)
    violation_count = int(list(results[1].query(violation_query))[0][0])
    warning_count = int(list(results[1].query(warning_query))[0][0])
    assert violations == violation_count
    assert warnings == warning_count
