from __future__ import annotations

from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryEntry,
    RootSurfaceInventoryReadModel,
    RootSurfacePathType,
    build_root_surface_inventory,
    classify_root_surface_path,
    read_model_from_mapping,
)


def test_classifies_known_root_surface_candidates() -> None:
    source_entry = classify_root_surface_path(
        "MAKSIMAR_CORE_LIB/root_artifact_hygiene",
        is_dir=True,
    )
    backup_entry = classify_root_surface_path(
        "tests/conftest.py.bak_restore_pytest_monitor_helper",
        is_dir=False,
    )
    audit_entry = classify_root_surface_path(
        "audit_phase_3_1_display_topology_precut_20260510_001154.txt",
        is_dir=False,
    )
    generated_entry = classify_root_surface_path(
        "project_audit/roadmap_baseline_20260515_235329",
        is_dir=True,
    )
    vendor_entry = classify_root_surface_path(
        "EXTERNAL_BACKENDS/mempalace/security_reports/vendor_bandit_report.json",
        is_dir=False,
    )
    unknown_entry = classify_root_surface_path(
        "unexpected_root_file.custom",
        is_dir=False,
    )

    assert source_entry.candidate_kind is RootArtifactCandidateKind.SOURCE_CANDIDATE
    assert backup_entry.candidate_kind is RootArtifactCandidateKind.BACKUP_CANDIDATE
    assert audit_entry.candidate_kind is RootArtifactCandidateKind.AUDIT_CANDIDATE
    assert generated_entry.candidate_kind is RootArtifactCandidateKind.GENERATED_CANDIDATE
    assert vendor_entry.candidate_kind is RootArtifactCandidateKind.VENDOR_CANDIDATE
    assert unknown_entry.candidate_kind is RootArtifactCandidateKind.UNKNOWN_CANDIDATE

    assert source_entry.delete_allowed is False
    assert source_entry.move_allowed is False
    assert source_entry.dashboard_safe is True


def test_rejects_absolute_or_parent_relative_paths() -> None:
    with pytest.raises(ValueError):
        classify_root_surface_path("/tmp/not-project-relative", is_dir=False)

    with pytest.raises(ValueError):
        classify_root_surface_path("../outside", is_dir=False)


def test_root_surface_inventory_read_model_is_dashboard_safe() -> None:
    entries = (
        RootSurfaceInventoryEntry(
            relative_path="README.md",
            path_type=RootSurfacePathType.FILE,
            candidate_kind=RootArtifactCandidateKind.SOURCE_CANDIDATE,
            reason_codes=("known_source_root_file",),
            size_bytes=10,
        ),
        RootSurfaceInventoryEntry(
            relative_path="full_pytest_run.txt",
            path_type=RootSurfacePathType.FILE,
            candidate_kind=RootArtifactCandidateKind.AUDIT_CANDIDATE,
            reason_codes=("audit_report_or_coverage_marker",),
            size_bytes=20,
        ),
        RootSurfaceInventoryEntry(
            relative_path="unknown.custom",
            path_type=RootSurfacePathType.FILE,
            candidate_kind=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
            reason_codes=("unknown_root_surface_path",),
            size_bytes=30,
        ),
    )

    read_model = RootSurfaceInventoryReadModel.from_entries(
        scanned_root="/project",
        entries=entries,
    )

    assert read_model.layer_id == "ROOT_ARTIFACT_HYGIENE"
    assert read_model.batch_id == "PHASE_0_BATCH_0_1"
    assert read_model.status == "ready"
    assert read_model.readiness == 1.0

    assert read_model.total_entries == 3
    assert read_model.total_root_files == 3
    assert read_model.total_root_dirs == 0
    assert read_model.source_candidates == 1
    assert read_model.audit_candidates == 1
    assert read_model.unknown_candidates == 1

    assert read_model.scan_readonly is True
    assert read_model.delete_allowed is False
    assert read_model.move_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.runtime_mutation_allowed is False
    assert read_model.canonical_write_allowed is False
    assert "unknown_candidates_present" in read_model.warnings
    assert read_model.next_action == "review_unknown_candidates_before_classification"

    payload = read_model.to_dict()

    assert payload["dashboard_safe"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["entries"][0]["dashboard_safe"] is True


def test_read_model_round_trip_from_mapping() -> None:
    read_model = RootSurfaceInventoryReadModel.from_entries(
        scanned_root="/project",
        entries=(
            RootSurfaceInventoryEntry(
                relative_path="README.md",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.SOURCE_CANDIDATE,
                reason_codes=("known_source_root_file",),
                size_bytes=10,
            ),
        ),
    )

    restored = read_model_from_mapping(read_model.to_dict())

    assert restored == read_model
    assert restored.to_dict() == read_model.to_dict()


def test_build_root_surface_inventory_scans_without_mutation(tmp_path: Path) -> None:
    (tmp_path / "MAKSIMAR_CORE_LIB").mkdir()
    (tmp_path / "MAKSIMAR_CORE_LIB" / "example.py").write_text(
        "VALUE = 1\n",
        encoding="utf-8",
    )

    (tmp_path / "project_audit").mkdir()
    (tmp_path / "project_audit" / "run.txt").write_text(
        "audit\n",
        encoding="utf-8",
    )

    (tmp_path / "EXTERNAL_BACKENDS").mkdir()
    (tmp_path / "EXTERNAL_BACKENDS" / "vendor.json").write_text(
        "{}\n",
        encoding="utf-8",
    )

    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "conftest.py.bak_restore").write_text(
        "# backup\n",
        encoding="utf-8",
    )

    (tmp_path / "audit_phase_1.txt").write_text(
        "audit\n",
        encoding="utf-8",
    )
    (tmp_path / "unknown.custom").write_text(
        "unknown\n",
        encoding="utf-8",
    )

    read_model = build_root_surface_inventory(tmp_path, max_depth=2)

    assert read_model.total_entries >= 6
    assert read_model.source_candidates >= 1
    assert read_model.generated_candidates >= 1
    assert read_model.vendor_candidates >= 1
    assert read_model.backup_candidates >= 1
    assert read_model.audit_candidates >= 1
    assert read_model.unknown_candidates >= 1

    assert read_model.scan_readonly is True
    assert read_model.delete_allowed is False
    assert read_model.move_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.runtime_mutation_allowed is False
    assert read_model.canonical_write_allowed is False

    assert (tmp_path / "MAKSIMAR_CORE_LIB" / "example.py").exists()
    assert (tmp_path / "unknown.custom").exists()
