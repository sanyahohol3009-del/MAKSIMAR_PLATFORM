from __future__ import annotations

from pathlib import Path

from tools.foundation_roadmap_ci_check import (
    DEFAULT_ROADMAP_PATH,
    DEFAULT_SCHEMA_PATH,
    load_json_file,
    validate_roadmap_shape,
)


def test_batched_foundation_roadmap_schema_files_exist() -> None:
    assert Path(DEFAULT_ROADMAP_PATH).exists()
    assert Path(DEFAULT_SCHEMA_PATH).exists()


def test_batched_foundation_roadmap_shape_is_valid() -> None:
    roadmap = load_json_file(Path(DEFAULT_ROADMAP_PATH))
    issues = validate_roadmap_shape(roadmap)

    assert issues == ()
    assert roadmap["roadmap_id"] == "batched_foundation_roadmap_v2_1_correction_patch"
    assert roadmap["version"] == "2.1"


def test_batched_foundation_roadmap_contains_v2_1_correction_requirements() -> None:
    roadmap = load_json_file(Path(DEFAULT_ROADMAP_PATH))

    assert roadmap["global_rules"]["semantic_duplicate_scan_required"] is True
    assert roadmap["global_rules"]["no_delete_without_correction_pass"] is True
    assert roadmap["global_rules"]["no_move_without_correction_pass"] is True
    assert roadmap["global_rules"]["full_auto_pytest_required"] is True

    forbidden_paths = set(roadmap["forbidden_paths"])
    assert "MAKSIMAR_CORE_LIB/data_plane/append_on y_log_models.py" in forbidden_paths
    assert "MAKSIMAR_CORE_LIB/data_plane/immutable_ledge_contract.py" in forbidden_paths
    assert "MAKSIMAR_CORE_LIB/update_recovery/signature_verifier_contract.py" in forbidden_paths
    assert "tests/network_containerization/test_network_network_topology_builder_smoke.py" in forbidden_paths


def test_active_batch_0_2_contains_semantic_duplicate_correction_files() -> None:
    roadmap = load_json_file(Path(DEFAULT_ROADMAP_PATH))

    batches = {
        batch["batch_id"]: batch
        for phase in roadmap["phases"]
        for batch in phase["batches"]
    }

    batch_0_2 = batches["0.2"]

    assert batch_0_2["status"] == "ACTIVE"
    assert batch_0_2["semantic_duplicate_scan_required"] is True

    assert "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py" in batch_0_2["correction_additions"]
    assert "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_policy.py" in batch_0_2["correction_additions"]
    assert "tests/root_artifact_hygiene/test_semantic_duplicate_scan_models_smoke.py" in batch_0_2["correction_tests"]
    assert "tests/root_artifact_hygiene/test_semantic_duplicate_scan_policy_smoke.py" in batch_0_2["correction_tests"]
    assert "SemanticDuplicateScanReadModel" in batch_0_2["dashboard_read_models"]
