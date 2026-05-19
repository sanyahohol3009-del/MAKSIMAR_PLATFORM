from __future__ import annotations

from pathlib import Path


def test_data_plane_existing_sources_binding_is_reference_only() -> None:
    path = Path("DATA_PLANE/existing_bindings/data_plane_existing_sources.yaml")
    text = path.read_text(encoding="utf-8")

    assert "decision: reference_existing_sources_no_move_no_delete" in text
    assert "action: reference_only" in text
    assert "no_move_without_correction_pass: true" in text
    assert "no_delete_without_correction_pass: true" in text
    assert "no_migration_without_correction_pass: true" in text
    assert "no_direct_canonical_write: true" in text
    assert "dashboard_read_only: true" in text


def test_data_plane_container_boundary_blocks_unsafe_paths() -> None:
    path = Path("DATA_PLANE/boundaries/container_adapter_boundary.yaml")
    text = path.read_text(encoding="utf-8")

    assert "dashboard_to_data_plane_mutation" in text
    assert "ui_to_data_plane_execution" in text
    assert "control_plane_heavy_payload_transfer" in text
    assert "data_plane_direct_core_write" in text
    assert "container_direct_core_write" in text
    assert "legacy_file_move_without_correction_gate" in text
    assert "legacy_file_delete_without_correction_gate" in text


def test_data_plane_policy_declares_append_only_and_payload_reference_rules() -> None:
    path = Path("DATA_PLANE/config/data_plane_policy.yaml")
    text = path.read_text(encoding="utf-8")

    assert "append_only:" in text
    assert "overwrite_allowed: false" in text
    assert "delete_allowed: false" in text
    assert "heavy_payload_in_control_path_allowed: false" in text
    assert "payload_reference_required: true" in text
    assert "direct_canonical_write_allowed: false" in text
