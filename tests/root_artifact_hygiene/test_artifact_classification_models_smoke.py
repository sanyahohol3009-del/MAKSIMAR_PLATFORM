from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_classification_models import (
    ArtifactAllowedAction,
    ArtifactClassificationEntry,
    ArtifactClassificationReadModel,
    ArtifactLocationStatus,
    ArtifactRiskLevel,
    artifact_classification_read_model_from_mapping,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_location_policy import (
    build_artifact_classification_read_model,
    classify_inventory_entry_location,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryEntry,
    RootSurfaceInventoryReadModel,
    RootSurfacePathType,
)


def test_artifact_classification_entry_is_dashboard_safe_and_non_mutating() -> None:
    entry = ArtifactClassificationEntry(
        artifact_path="full_pytest_run.txt",
        artifact_class=RootArtifactCandidateKind.AUDIT_CANDIDATE,
        current_location=".",
        expected_location="docs/archive/reports",
        location_status=ArtifactLocationStatus.AUDIT_REPORT,
        risk_level=ArtifactRiskLevel.LOW,
        allowed_action=ArtifactAllowedAction.ARCHIVE_LATER_WITH_APPROVAL,
        correction_required=False,
        archive_candidate=True,
        reason_codes=("audit_or_report_requires_archive_pass",),
        requires_approval=True,
    )

    payload = entry.to_dict()

    assert payload["artifact_path"] == "full_pytest_run.txt"
    assert payload["artifact_class"] == "audit_candidate"
    assert payload["location_status"] == "audit_report"
    assert payload["allowed_action"] == "archive_later_with_approval"
    assert payload["auto_delete_allowed"] is False
    assert payload["auto_move_allowed"] is False
    assert payload["requires_approval"] is True
    assert payload["dashboard_safe"] is True


def test_artifact_classification_entry_rejects_auto_delete_or_auto_move() -> None:
    with pytest.raises(ValueError):
        ArtifactClassificationEntry(
            artifact_path="audit.txt",
            artifact_class=RootArtifactCandidateKind.AUDIT_CANDIDATE,
            current_location=".",
            expected_location="docs/archive/audits",
            location_status=ArtifactLocationStatus.AUDIT_REPORT,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.REVIEW_ONLY,
            correction_required=False,
            archive_candidate=True,
            auto_delete_allowed=True,
        )

    with pytest.raises(ValueError):
        ArtifactClassificationEntry(
            artifact_path="audit.txt",
            artifact_class=RootArtifactCandidateKind.AUDIT_CANDIDATE,
            current_location=".",
            expected_location="docs/archive/audits",
            location_status=ArtifactLocationStatus.AUDIT_REPORT,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.REVIEW_ONLY,
            correction_required=False,
            archive_candidate=True,
            auto_move_allowed=True,
        )


def test_classification_policy_maps_inventory_candidates() -> None:
    source_entry = RootSurfaceInventoryEntry(
        relative_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/root_surface_inventory_models.py",
        path_type=RootSurfacePathType.FILE,
        candidate_kind=RootArtifactCandidateKind.SOURCE_CANDIDATE,
        reason_codes=("known_source_root",),
    )
    backup_entry = RootSurfaceInventoryEntry(
        relative_path="tests/conftest.py.bak_restore_pytest_monitor_helper",
        path_type=RootSurfacePathType.FILE,
        candidate_kind=RootArtifactCandidateKind.BACKUP_CANDIDATE,
        reason_codes=("backup_filename_marker",),
    )
    audit_entry = RootSurfaceInventoryEntry(
        relative_path="full_pytest_run.txt",
        path_type=RootSurfacePathType.FILE,
        candidate_kind=RootArtifactCandidateKind.AUDIT_CANDIDATE,
        reason_codes=("audit_report_or_coverage_marker",),
    )
    vendor_entry = RootSurfaceInventoryEntry(
        relative_path="EXTERNAL_BACKENDS/mempalace/security_reports/vendor_bandit_report.json",
        path_type=RootSurfacePathType.FILE,
        candidate_kind=RootArtifactCandidateKind.VENDOR_CANDIDATE,
        reason_codes=("under_external_backends",),
    )
    unknown_entry = RootSurfaceInventoryEntry(
        relative_path="unexpected.custom",
        path_type=RootSurfacePathType.FILE,
        candidate_kind=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
        reason_codes=("unknown_root_surface_path",),
    )

    source_classification = classify_inventory_entry_location(source_entry)
    backup_classification = classify_inventory_entry_location(backup_entry)
    audit_classification = classify_inventory_entry_location(audit_entry)
    vendor_classification = classify_inventory_entry_location(vendor_entry)
    unknown_classification = classify_inventory_entry_location(unknown_entry)

    assert source_classification.location_status is ArtifactLocationStatus.CORRECT_LOCATION
    assert source_classification.allowed_action is ArtifactAllowedAction.USE_IN_PLACE

    assert backup_classification.location_status is ArtifactLocationStatus.BACKUP
    assert backup_classification.archive_candidate is True
    assert backup_classification.requires_approval is True

    assert audit_classification.location_status is ArtifactLocationStatus.AUDIT_REPORT
    assert audit_classification.expected_location == "docs/archive/reports"

    assert vendor_classification.location_status is ArtifactLocationStatus.EXTERNAL_VENDOR
    assert vendor_classification.allowed_action is ArtifactAllowedAction.KEEP_VENDOR_SANDBOXED

    assert unknown_classification.location_status is ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS
    assert unknown_classification.correction_required is True
    assert unknown_classification.requires_approval is True


def test_artifact_classification_read_model_summarizes_dashboard_fields() -> None:
    inventory = RootSurfaceInventoryReadModel.from_entries(
        scanned_root="/project",
        entries=(
            RootSurfaceInventoryEntry(
                relative_path="README.md",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.SOURCE_CANDIDATE,
                reason_codes=("known_source_root_file",),
            ),
            RootSurfaceInventoryEntry(
                relative_path="full_pytest_run.txt",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.AUDIT_CANDIDATE,
                reason_codes=("audit_report_or_coverage_marker",),
            ),
            RootSurfaceInventoryEntry(
                relative_path="unknown.custom",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
                reason_codes=("unknown_root_surface_path",),
            ),
        ),
    )

    read_model = build_artifact_classification_read_model(inventory)
    payload = read_model.to_dict()

    assert read_model.layer_id == "ROOT_ARTIFACT_HYGIENE"
    assert read_model.batch_id == "PHASE_0_BATCH_0_2"
    assert read_model.total_classifications == 3
    assert read_model.correct_location_count == 1
    assert read_model.audit_report_count == 1
    assert read_model.correction_required_count == 1
    assert read_model.archive_candidate_count == 1
    assert read_model.approval_required_count == 2

    assert read_model.scan_readonly is True
    assert read_model.delete_allowed is False
    assert read_model.move_allowed is False
    assert read_model.dashboard_safe is True
    assert read_model.runtime_mutation_allowed is False
    assert read_model.canonical_write_allowed is False

    assert "archive_candidates_present" in read_model.warnings
    assert "correction_required_candidates_present" in read_model.warnings
    assert read_model.next_action == "prepare_correction_or_archive_review"

    assert payload["dashboard_safe"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
    assert payload["canonical_write_allowed"] is False


def test_artifact_classification_read_model_round_trip() -> None:
    read_model = ArtifactClassificationReadModel.from_entries(
        scanned_root="/project",
        classifications=(
            ArtifactClassificationEntry(
                artifact_path="README.md",
                artifact_class=RootArtifactCandidateKind.SOURCE_CANDIDATE,
                current_location="README.md",
                expected_location="README.md",
                location_status=ArtifactLocationStatus.CORRECT_LOCATION,
                risk_level=ArtifactRiskLevel.NONE,
                allowed_action=ArtifactAllowedAction.USE_IN_PLACE,
                correction_required=False,
                archive_candidate=False,
                reason_codes=("known_source_root_file",),
            ),
        ),
    )

    restored = artifact_classification_read_model_from_mapping(read_model.to_dict())

    assert restored == read_model
    assert restored.to_dict() == read_model.to_dict()
