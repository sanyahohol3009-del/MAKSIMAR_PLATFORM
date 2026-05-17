from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_classification_models import (
    ArtifactAllowedAction,
    ArtifactClassificationEntry,
    ArtifactLocationStatus,
    ArtifactRiskLevel,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_location_policy import (
    build_artifact_classification_read_model,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
    RootSurfaceInventoryEntry,
    RootSurfaceInventoryReadModel,
    RootSurfacePathType,
)


def test_no_auto_delete_or_auto_move_is_allowed_for_any_policy_classification() -> None:
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
                relative_path="tests/conftest.py.bak_restore",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.BACKUP_CANDIDATE,
                reason_codes=("backup_filename_marker",),
            ),
            RootSurfaceInventoryEntry(
                relative_path="project_audit/roadmap_baseline_20260515_235329",
                path_type=RootSurfacePathType.DIRECTORY,
                candidate_kind=RootArtifactCandidateKind.GENERATED_CANDIDATE,
                reason_codes=("generated_or_runtime_artifact_root",),
            ),
            RootSurfaceInventoryEntry(
                relative_path="EXTERNAL_BACKENDS/mempalace/security_reports/vendor_bandit_report.json",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.VENDOR_CANDIDATE,
                reason_codes=("under_external_backends",),
            ),
            RootSurfaceInventoryEntry(
                relative_path="unexpected.custom",
                path_type=RootSurfacePathType.FILE,
                candidate_kind=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
                reason_codes=("unknown_root_surface_path",),
            ),
        ),
    )

    read_model = build_artifact_classification_read_model(inventory)

    assert read_model.delete_allowed is False
    assert read_model.move_allowed is False
    assert read_model.runtime_mutation_allowed is False
    assert read_model.canonical_write_allowed is False

    for classification in read_model.classifications:
        assert classification.auto_delete_allowed is False
        assert classification.auto_move_allowed is False
        assert classification.dashboard_safe is True


def test_archive_later_action_requires_explicit_approval() -> None:
    with pytest.raises(ValueError):
        ArtifactClassificationEntry(
            artifact_path="full_pytest_run.txt",
            artifact_class=RootArtifactCandidateKind.AUDIT_CANDIDATE,
            current_location=".",
            expected_location="docs/archive/reports",
            location_status=ArtifactLocationStatus.AUDIT_REPORT,
            risk_level=ArtifactRiskLevel.LOW,
            allowed_action=ArtifactAllowedAction.ARCHIVE_LATER_WITH_APPROVAL,
            correction_required=False,
            archive_candidate=True,
            requires_approval=False,
        )


def test_migration_action_requires_correction_required() -> None:
    with pytest.raises(ValueError):
        ArtifactClassificationEntry(
            artifact_path="wrong/place.py",
            artifact_class=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
            current_location="wrong",
            expected_location="correct",
            location_status=ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS,
            risk_level=ArtifactRiskLevel.MEDIUM,
            allowed_action=ArtifactAllowedAction.MIGRATION_PASS_REQUIRED,
            correction_required=False,
            archive_candidate=False,
            requires_approval=True,
        )
