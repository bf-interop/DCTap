import pathlib

import pytest

from pyshacl import validate

from conftest import load_params

TEST_DIRECTORY = pathlib.Path(__file__).parent


@pytest.mark.parametrize("rdf_file_path, violations, warnings", load_params("monograph_text_works.csv"))
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


@pytest.mark.parametrize("rdf_file_path, violations, warnings", load_params("monograph_print_instances.csv"))
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


@pytest.mark.parametrize("rdf_file_path, violations, warnings", load_params("monograph_admin_metadata.csv"))
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
