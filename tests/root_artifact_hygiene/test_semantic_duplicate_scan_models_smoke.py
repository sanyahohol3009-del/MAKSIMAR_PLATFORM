from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_models import (
    NO_EXISTING_MATCH_SENTINEL,
    SemanticDuplicateAction,
    SemanticDuplicateRelation,
    SemanticDuplicateRisk,
    SemanticDuplicateScanCandidate,
    SemanticDuplicateScanReadModel,
    SemanticFamily,
    semantic_duplicate_read_model_from_mapping,
)


def test_semantic_duplicate_candidate_is_dashboard_safe_and_non_mutating() -> None:
    candidate = SemanticDuplicateScanCandidate(
        target_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
        existing_path=NO_EXISTING_MATCH_SENTINEL,
        target_family=SemanticFamily.ROOT_ARTIFACT_HYGIENE,
        existing_family=SemanticFamily.UNKNOWN,
        duplicate_relation=SemanticDuplicateRelation.NO_RELATION,
        action=SemanticDuplicateAction.CREATE_NEW,
        risk_level=SemanticDuplicateRisk.NONE,
        reason_codes=("no_existing_semantic_match_found",),
    )

    payload = candidate.to_dict()

    assert payload["action"] == "create_new"
    assert payload["dashboard_safe"] is True
    assert payload["scan_readonly"] is True
    assert payload["runtime_mutation_allowed"] is False
    assert payload["canonical_write_allowed"] is False
    assert payload["auto_delete_allowed"] is False
    assert payload["auto_move_allowed"] is False


def test_true_duplicate_risk_requires_high_risk() -> None:
    with pytest.raises(ValueError):
        SemanticDuplicateScanCandidate(
            target_path="MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
            existing_path="MAKSIMAR_CORE_LIB/other/signature_verifier_contract.py",
            target_family=SemanticFamily.SECURITY,
            existing_family=SemanticFamily.SECURITY,
            duplicate_relation=SemanticDuplicateRelation.EXACT_NAME_MATCH,
            action=SemanticDuplicateAction.TRUE_DUPLICATE_RISK,
            risk_level=SemanticDuplicateRisk.MEDIUM,
            reason_codes=("exact_name_match",),
            requires_approval=True,
        )


def test_migration_candidate_requires_approval() -> None:
    with pytest.raises(ValueError):
        SemanticDuplicateScanCandidate(
            target_path="MAKSIMAR_CORE_LIB/security_layer/policy_enforcer_contract.py",
            existing_path="MAKSIMAR_CORE_LIB/policy_engine/policy_loader.py",
            target_family=SemanticFamily.SECURITY,
            existing_family=SemanticFamily.SECURITY,
            duplicate_relation=SemanticDuplicateRelation.SEMANTIC_FAMILY_MATCH,
            action=SemanticDuplicateAction.MIGRATION_CANDIDATE,
            risk_level=SemanticDuplicateRisk.MEDIUM,
            reason_codes=("semantic_family_match",),
            requires_approval=False,
        )


def test_container_boundary_action_requires_container_boundary_relation() -> None:
    with pytest.raises(ValueError):
        SemanticDuplicateScanCandidate(
            target_path="SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
            existing_path="MAKSIMAR_CORE_LIB/security_layer/security_gate_contract.py",
            target_family=SemanticFamily.SECURITY,
            existing_family=SemanticFamily.SECURITY,
            duplicate_relation=SemanticDuplicateRelation.SEMANTIC_FAMILY_MATCH,
            action=SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED,
            risk_level=SemanticDuplicateRisk.LOW,
            reason_codes=("container_boundary_duplicate",),
        )


def test_semantic_duplicate_read_model_summarizes_dashboard_fields() -> None:
    read_model = SemanticDuplicateScanReadModel.from_candidates(
        scan_scope="project",
        target_paths=(
            "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
            "MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
        ),
        candidates=(
            SemanticDuplicateScanCandidate(
                target_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
                existing_path=NO_EXISTING_MATCH_SENTINEL,
                target_family=SemanticFamily.ROOT_ARTIFACT_HYGIENE,
                existing_family=SemanticFamily.UNKNOWN,
                duplicate_relation=SemanticDuplicateRelation.NO_RELATION,
                action=SemanticDuplicateAction.CREATE_NEW,
                risk_level=SemanticDuplicateRisk.NONE,
                reason_codes=("no_existing_semantic_match_found",),
            ),
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
        ),
    )

    payload = read_model.to_dict()

    assert read_model.layer_id == "ROOT_ARTIFACT_HYGIENE"
    assert read_model.batch_id == "PHASE_0_BATCH_0_2"
    assert read_model.total_candidates == 2
    assert read_model.create_new_count == 1
    assert read_model.true_duplicate_risk_count == 1
    assert read_model.approval_required_count == 1
    assert "true_duplicate_risk_present" in read_model.warnings
    assert read_model.next_action == "resolve_true_duplicate_or_migration_candidates"

    assert payload["dashboard_safe"] is True
    assert payload["delete_allowed"] is False
    assert payload["move_allowed"] is False
    assert payload["runtime_mutation_allowed"] is False
    assert payload["canonical_write_allowed"] is False


def test_semantic_duplicate_read_model_round_trip() -> None:
    read_model = SemanticDuplicateScanReadModel.from_candidates(
        scan_scope="project",
        target_paths=(
            "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
        ),
        candidates=(
            SemanticDuplicateScanCandidate(
                target_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
                existing_path=NO_EXISTING_MATCH_SENTINEL,
                target_family=SemanticFamily.ROOT_ARTIFACT_HYGIENE,
                existing_family=SemanticFamily.UNKNOWN,
                duplicate_relation=SemanticDuplicateRelation.NO_RELATION,
                action=SemanticDuplicateAction.CREATE_NEW,
                risk_level=SemanticDuplicateRisk.NONE,
                reason_codes=("no_existing_semantic_match_found",),
            ),
        ),
    )

    restored = semantic_duplicate_read_model_from_mapping(read_model.to_dict())

    assert restored == read_model
    assert restored.to_dict() == read_model.to_dict()
