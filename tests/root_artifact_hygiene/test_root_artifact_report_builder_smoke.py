from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.artifact_classification_models import (
    ArtifactAllowedAction,
    ArtifactClassificationEntry,
    ArtifactClassificationReadModel,
    ArtifactLocationStatus,
    ArtifactRiskLevel,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_artifact_report_builder import (
    RootArtifactReportItem,
    RootArtifactReportReadModel,
    build_root_artifact_report,
    build_root_artifact_report_from_project_root,
    root_artifact_report_read_model_from_mapping,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.root_surface_inventory_models import (
    RootArtifactCandidateKind,
)


def test_root_artifact_report_item_is_dashboard_safe_and_non_mutating() -> None:
    item = RootArtifactReportItem(
        artifact_path="full_pytest_run.txt",
        artifact_class="audit_candidate",
        current_location=".",
        expected_location="docs/archive/reports",
        location_status="audit_report",
        allowed_action="archive_later_with_approval",
        correction_required=False,
        archive_candidate=True,
        requires_approval=True,
        risk_level="low",
        reason_codes=("audit_or_report_requires_archive_pass",),
    )

    payload = item.to_dict()

    assert payload["dashboard_safe"] is True
    assert payload["auto_delete_allowed"] is False
    assert payload["auto_move_allowed"] is False
    assert payload["archive_candidate"] is True
    assert payload["requires_approval"] is True


def test_root_artifact_report_item_rejects_mutating_flags() -> None:
    with pytest.raises(ValueError):
        RootArtifactReportItem(
            artifact_path="full_pytest_run.txt",
            artifact_class="audit_candidate",
            current_location=".",
            expected_location="docs/archive/reports",
            location_status="audit_report",
            allowed_action="archive_later_with_approval",
            correction_required=False,
            archive_candidate=True,
            requires_approval=True,
            risk_level="low",
            auto_delete_allowed=True,
        )

    with pytest.raises(ValueError):
        RootArtifactReportItem(
            artifact_path="full_pytest_run.txt",
            artifact_class="audit_candidate",
            current_location=".",
            expected_location="docs/archive/reports",
            location_status="audit_report",
            allowed_action="archive_later_with_approval",
            correction_required=False,
            archive_candidate=True,
            requires_approval=True,
            risk_level="low",
            auto_move_allowed=True,
        )


def test_build_root_artifact_report_from_classification_read_model() -> None:
    classification_read_model = ArtifactClassificationReadModel.from_entries(
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
                reason_codes=("audit_or_report_requires_archive_pass",),
                requires_approval=True,
            ),
            ArtifactClassificationEntry(
                artifact_path="unknown.custom",
                artifact_class=RootArtifactCandidateKind.UNKNOWN_CANDIDATE,
                current_location=".",
                expected_location="manual_review_required",
                location_status=ArtifactLocationStatus.CANDIDATE_FOR_CORRECTION_PASS,
                risk_level=ArtifactRiskLevel.MEDIUM,
                allowed_action=ArtifactAllowedAction.MIGRATION_PASS_REQUIRED,
                correction_required=True,
                archive_candidate=False,
                reason_codes=("unknown_candidate_requires_manual_location_review",),
                requires_approval=True,
            ),
        ),
    )

    report = build_root_artifact_report(classification_read_model)
    payload = report.to_dict()

    assert report.layer_id == "ROOT_ARTIFACT_HYGIENE"
    assert report.batch_id == "PHASE_0_BATCH_0_3"
    assert report.total_items == 3
    assert report.source_count == 1
    assert report.audit_report_count == 1
    assert report.unknown_count == 1
    assert report.archive_candidate_count == 1
    assert report.correction_required_count == 1
    assert report.approval_required_count == 2
    assert report.scan_readonly is True
    assert report.delete_allowed is False
    assert report.move_allowed is False
    assert report.dashboard_safe is True
    assert report.runtime_mutation_allowed is False
    assert report.canonical_write_allowed is False
    assert "archive_candidate_items_present" in report.warnings
    assert "correction_required_items_present" in report.warnings
    assert report.next_action == "review_correction_and_archive_candidates"

    assert payload["dashboard_safe"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
    assert payload["canonical_write_allowed"] is False


def test_root_artifact_report_round_trip() -> None:
    report = RootArtifactReportReadModel.from_items(
        scanned_root="/project",
        items=(
            RootArtifactReportItem(
                artifact_path="README.md",
                artifact_class="source_candidate",
                current_location="README.md",
                expected_location="README.md",
                location_status="correct_location",
                allowed_action="use_in_place",
                correction_required=False,
                archive_candidate=False,
                requires_approval=False,
                risk_level="none",
                reason_codes=("known_source_root_file",),
            ),
        ),
    )

    restored = root_artifact_report_read_model_from_mapping(report.to_dict())

    assert restored == report
    assert restored.to_dict() == report.to_dict()


def test_build_root_artifact_report_from_project_root_is_read_only(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("readme\n", encoding="utf-8")
    (tmp_path / "full_pytest_run.txt").write_text("pytest\n", encoding="utf-8")

    report = build_root_artifact_report_from_project_root(tmp_path, max_depth=1)

    assert report.total_items >= 2
    assert report.scan_readonly is True
    assert report.delete_allowed is False
    assert report.move_allowed is False
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "full_pytest_run.txt").exists()


def test_root_artifact_hygiene_report_tool_smoke(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("readme\n", encoding="utf-8")

    tool = Path("tools/root_artifact_hygiene_report.py")
    assert tool.exists()

    completed = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--root",
            str(tmp_path),
            "--max-depth",
            "1",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout

    payload = json.loads(completed.stdout)

    assert payload["layer_id"] == "ROOT_ARTIFACT_HYGIENE"
    assert payload["batch_id"] == "PHASE_0_BATCH_0_3"
    assert payload["scan_readonly"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
