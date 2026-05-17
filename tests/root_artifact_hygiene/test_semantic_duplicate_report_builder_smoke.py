from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_report_builder import (
    SemanticDuplicateReportItem,
    SemanticDuplicateReportReadModel,
    build_semantic_duplicate_report,
    build_semantic_duplicate_report_from_paths,
    semantic_duplicate_report_read_model_from_mapping,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_models import (
    NO_EXISTING_MATCH_SENTINEL,
    SemanticDuplicateAction,
    SemanticDuplicateRelation,
    SemanticDuplicateRisk,
    SemanticDuplicateScanCandidate,
    SemanticDuplicateScanReadModel,
    SemanticFamily,
)


def test_semantic_duplicate_report_item_is_dashboard_safe_and_non_mutating() -> None:
    item = SemanticDuplicateReportItem(
        target_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_report_builder.py",
        existing_path=NO_EXISTING_MATCH_SENTINEL,
        target_family="root_artifact_hygiene",
        existing_family="unknown",
        duplicate_relation="no_relation",
        action="create_new",
        risk_level="none",
        requires_approval=False,
        reason_codes=("no_existing_semantic_match_found",),
    )

    payload = item.to_dict()

    assert payload["dashboard_safe"] is True
    assert payload["scan_readonly"] is True
    assert payload["auto_delete_allowed"] is False
    assert payload["auto_move_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["canonical_write_allowed"] is False


def test_semantic_duplicate_report_item_rejects_mutating_flags() -> None:
    with pytest.raises(ValueError):
        SemanticDuplicateReportItem(
            target_path="target.py",
            existing_path=NO_EXISTING_MATCH_SENTINEL,
            target_family="testing_tooling",
            existing_family="unknown",
            duplicate_relation="no_relation",
            action="create_new",
            risk_level="none",
            requires_approval=False,
            auto_delete_allowed=True,
        )

    with pytest.raises(ValueError):
        SemanticDuplicateReportItem(
            target_path="target.py",
            existing_path=NO_EXISTING_MATCH_SENTINEL,
            target_family="testing_tooling",
            existing_family="unknown",
            duplicate_relation="no_relation",
            action="create_new",
            risk_level="none",
            requires_approval=False,
            auto_move_allowed=True,
        )


def test_build_semantic_duplicate_report_from_scan_read_model() -> None:
    scan_read_model = SemanticDuplicateScanReadModel.from_candidates(
        scan_scope="phase_0_batch_0_3",
        target_paths=(
            "MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
            "SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
        ),
        candidates=(
            SemanticDuplicateScanCandidate(
                target_path="MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
                existing_path="MAKSIMAR_CORE_LIB/other/signature_verifier_contract.py",
                target_family=SemanticFamily.SECURITY,
                existing_family=SemanticFamily.SECURITY,
                duplicate_relation=SemanticDuplicateRelation.EXACT_NAME_MATCH,
                action=SemanticDuplicateAction.TRUE_DUPLICATE_RISK,
                risk_level=SemanticDuplicateRisk.HIGH,
                reason_codes=("exact_name_match",),
                requires_approval=True,
            ),
            SemanticDuplicateScanCandidate(
                target_path="SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
                existing_path="MAKSIMAR_CORE_LIB/security_layer/security_gate_adapter.py",
                target_family=SemanticFamily.SECURITY,
                existing_family=SemanticFamily.SECURITY,
                duplicate_relation=SemanticDuplicateRelation.CONTAINER_BOUNDARY_DUPLICATE,
                action=SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED,
                risk_level=SemanticDuplicateRisk.LOW,
                reason_codes=("container_boundary_duplicate",),
            ),
        ),
    )

    report = build_semantic_duplicate_report(scan_read_model)
    payload = report.to_dict()

    assert report.layer_id == "ROOT_ARTIFACT_HYGIENE"
    assert report.batch_id == "PHASE_0_BATCH_0_3"
    assert report.total_items == 2
    assert report.true_duplicate_risk_count == 1
    assert report.container_boundary_duplicate_allowed_count == 1
    assert report.approval_required_count == 1
    assert report.high_risk_count == 1
    assert report.delete_allowed is False
    assert report.move_allowed is False
    assert report.dashboard_safe is True
    assert "true_duplicate_risk_present" in report.warnings
    assert "container_boundary_duplicates_present" in report.warnings
    assert report.next_action == "resolve_true_duplicate_or_migration_candidates"

    assert payload["dashboard_safe"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
    assert payload["canonical_write_allowed"] is False


def test_semantic_duplicate_report_round_trip() -> None:
    report = SemanticDuplicateReportReadModel.from_items(
        scan_scope="project",
        target_paths=("target.py",),
        items=(
            SemanticDuplicateReportItem(
                target_path="target.py",
                existing_path=NO_EXISTING_MATCH_SENTINEL,
                target_family="testing_tooling",
                existing_family="unknown",
                duplicate_relation="no_relation",
                action="create_new",
                risk_level="none",
                requires_approval=False,
                reason_codes=("no_existing_semantic_match_found",),
            ),
        ),
    )

    restored = semantic_duplicate_report_read_model_from_mapping(report.to_dict())

    assert restored == report
    assert restored.to_dict() == report.to_dict()


def test_build_semantic_duplicate_report_from_paths() -> None:
    report = build_semantic_duplicate_report_from_paths(
        scan_scope="phase_0_batch_0_3",
        target_paths=(
            "MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
            "MAKSIMAR_CORE_LIB/root_artifact_hygiene/root_artifact_report_builder.py",
        ),
        existing_paths=(
            "MAKSIMAR_CORE_LIB/other/signature_verifier_contract.py",
            "tests/roadmap_index/test_batched_foundation_roadmap_schema_smoke.py",
        ),
    )

    assert report.true_duplicate_risk_count == 1
    assert report.create_new_count >= 1
    assert report.scan_readonly is True
    assert report.delete_allowed is False
    assert report.move_allowed is False


def test_root_artifact_semantic_duplicate_scan_tool_smoke(tmp_path: Path) -> None:
    (tmp_path / "existing.py").write_text("VALUE = 1\n", encoding="utf-8")

    tool = Path("tools/root_artifact_semantic_duplicate_scan.py")
    assert tool.exists()

    completed = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--root",
            str(tmp_path),
            "--target",
            "target.py",
            "--existing",
            "existing.py",
            "--scan-scope",
            "test",
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
