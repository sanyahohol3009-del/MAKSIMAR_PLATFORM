from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.DATA_PLANE import (
    DATA_PLANE_SERVER_BATCH_ID,
    DATA_PLANE_SERVER_CONTAINER_RUNTIME_ENABLED,
    DATA_PLANE_SERVER_DASHBOARD_MUTATION_ALLOWED,
    DATA_PLANE_SERVER_DIRECT_CANONICAL_WRITE_ALLOWED,
    DATA_PLANE_SERVER_DIRECT_EXECUTION_ALLOWED,
    DATA_PLANE_SERVER_HEAVY_PAYLOAD_IN_CONTROL_PATH_ALLOWED,
    DATA_PLANE_SERVER_PACKAGE_ID,
    DATA_PLANE_SERVER_PHASE_ID,
    DATA_PLANE_SERVER_SURFACE_DECLARED,
)


def test_data_plane_surface_files_exist() -> None:
    required_paths = (
        Path("DATA_PLANE/README.md"),
        Path("DATA_PLANE/layer_manifest.yaml"),
        Path("DATA_PLANE/container_contract.yaml"),
        Path("DATA_PLANE/config/data_plane_policy.yaml"),
        Path("DATA_PLANE/boundaries/container_adapter_boundary.yaml"),
        Path("DATA_PLANE/existing_bindings/data_plane_existing_sources.yaml"),
        Path("MAKSIMAR_SERVER/DATA_PLANE/__init__.py"),
    )

    for path in required_paths:
        assert path.exists(), f"missing required DATA_PLANE surface file: {path}"


def test_data_plane_server_boundary_constants_are_safe() -> None:
    assert DATA_PLANE_SERVER_PACKAGE_ID == "MAKSIMAR_SERVER_DATA_PLANE"
    assert DATA_PLANE_SERVER_PHASE_ID == "PHASE_2_DATA_PLANE_FOUNDATION_V1"
    assert DATA_PLANE_SERVER_BATCH_ID == "BATCH_2_1"
    assert DATA_PLANE_SERVER_SURFACE_DECLARED is True
    assert DATA_PLANE_SERVER_CONTAINER_RUNTIME_ENABLED is False
    assert DATA_PLANE_SERVER_DIRECT_EXECUTION_ALLOWED is False
    assert DATA_PLANE_SERVER_DASHBOARD_MUTATION_ALLOWED is False
    assert DATA_PLANE_SERVER_DIRECT_CANONICAL_WRITE_ALLOWED is False
    assert DATA_PLANE_SERVER_HEAVY_PAYLOAD_IN_CONTROL_PATH_ALLOWED is False


def test_existing_core_lib_data_plane_files_are_preserved() -> None:
    existing_paths = (
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_cleanup_contract.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_cleanup_models.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_ownership_contract.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_ownership_models.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_retention_contract.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/artifact_retention_models.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/data_plane_shell_contract.py"),
        Path("MAKSIMAR_CORE_LIB/data_plane/data_plane_shell_models.py"),
    )

    for path in existing_paths:
        assert path.exists(), f"existing data_plane source must remain in place: {path}"
