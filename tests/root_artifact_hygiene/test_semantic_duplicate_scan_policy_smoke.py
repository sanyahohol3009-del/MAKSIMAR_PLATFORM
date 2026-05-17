from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_models import (
    NO_EXISTING_MATCH_SENTINEL,
    SemanticDuplicateAction,
    SemanticDuplicateRelation,
    SemanticDuplicateRisk,
    SemanticFamily,
)
from MAKSIMAR_CORE_LIB.root_artifact_hygiene.semantic_duplicate_scan_policy import (
    build_semantic_duplicate_candidate,
    build_semantic_duplicate_scan_read_model,
    classify_semantic_duplicate_relation,
    infer_semantic_family,
)


def test_infer_semantic_family_from_paths() -> None:
    assert (
        infer_semantic_family(
            "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py"
        )
        is SemanticFamily.ROOT_ARTIFACT_HYGIENE
    )
    assert (
        infer_semantic_family("MAKSIMAR_CORE_LIB/security_layer/rbac_contract.py")
        is SemanticFamily.SECURITY
    )
    assert (
        infer_semantic_family("MAKSIMAR_CORE_LIB/data_plane/append_only_log_models.py")
        is SemanticFamily.DATA
    )
    assert (
        infer_semantic_family("MAKSIMAR_CORE_LIB/update_recovery/update_package_models.py")
        is SemanticFamily.UPDATE_RECOVERY
    )
    assert (
        infer_semantic_family("NETWORK_SEGMENTATION/network_segments.yaml")
        is SemanticFamily.NETWORK_CONTAINERIZATION
    )
    assert (
        infer_semantic_family("MAKSIMAR_CORE_LIB/ai_orchestration/model_router_contract.py")
        is SemanticFamily.AI_ORCHESTRATION
    )
    assert infer_semantic_family("unknown/path.custom") is SemanticFamily.UNKNOWN


def test_exact_name_match_is_true_duplicate_risk() -> None:
    candidate = build_semantic_duplicate_candidate(
        target_path="MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
        existing_path="MAKSIMAR_CORE_LIB/other/signature_verifier_contract.py",
    )

    assert candidate.duplicate_relation is SemanticDuplicateRelation.EXACT_NAME_MATCH
    assert candidate.action is SemanticDuplicateAction.TRUE_DUPLICATE_RISK
    assert candidate.risk_level is SemanticDuplicateRisk.HIGH
    assert candidate.requires_approval is True


def test_existing_legacy_semantic_match_wraps_as_adapter() -> None:
    candidate = build_semantic_duplicate_candidate(
        target_path="MAKSIMAR_CORE_LIB/security_layer/policy_enforcer_contract.py",
        existing_path="MAKSIMAR_CORE_LIB/policy_engine/policy_loader.py",
    )

    assert candidate.duplicate_relation is SemanticDuplicateRelation.LEGACY_IMPLEMENTATION
    assert candidate.action is SemanticDuplicateAction.WRAP_AS_ADAPTER
    assert candidate.risk_level is SemanticDuplicateRisk.MEDIUM


def test_container_boundary_duplicate_is_allowed_when_intentional() -> None:
    candidate = build_semantic_duplicate_candidate(
        target_path="SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
        existing_path="MAKSIMAR_CORE_LIB/security_layer/security_gate_adapter.py",
    )

    assert candidate.duplicate_relation is SemanticDuplicateRelation.CONTAINER_BOUNDARY_DUPLICATE
    assert candidate.action is SemanticDuplicateAction.CONTAINER_BOUNDARY_DUPLICATE_ALLOWED
    assert candidate.risk_level is SemanticDuplicateRisk.LOW
    assert candidate.requires_approval is False


def test_no_existing_match_produces_create_new_candidate() -> None:
    candidate = build_semantic_duplicate_candidate(
        target_path="MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
        existing_path=NO_EXISTING_MATCH_SENTINEL,
    )

    assert candidate.duplicate_relation is SemanticDuplicateRelation.NO_RELATION
    assert candidate.action is SemanticDuplicateAction.CREATE_NEW
    assert candidate.risk_level is SemanticDuplicateRisk.NONE
    assert candidate.existing_path == NO_EXISTING_MATCH_SENTINEL


def test_build_semantic_duplicate_scan_read_model() -> None:
    read_model = build_semantic_duplicate_scan_read_model(
        scan_scope="phase_0_batch_0_2",
        target_paths=(
            "MAKSIMAR_CORE_LIB/root_artifact_hygiene/semantic_duplicate_scan_models.py",
            "MAKSIMAR_CORE_LIB/security_layer/signature_verifier_contract.py",
            "SECURITY_LAYER/boundaries/container_adapter_boundary.yaml",
        ),
        existing_paths=(
            "tests/roadmap_index/test_batched_foundation_roadmap_schema_smoke.py",
            "MAKSIMAR_CORE_LIB/other/signature_verifier_contract.py",
            "MAKSIMAR_CORE_LIB/security_layer/security_gate_adapter.py",
        ),
    )

    assert read_model.scan_scope == "phase_0_batch_0_2"
    assert read_model.create_new_count >= 1
    assert read_model.true_duplicate_risk_count == 1
    assert read_model.container_boundary_duplicate_allowed_count == 1
    assert read_model.approval_required_count == 1
    assert read_model.delete_allowed is False
    assert read_model.move_allowed is False
    assert read_model.dashboard_safe is True


def test_rejects_absolute_paths() -> None:
    with pytest.raises(ValueError):
        classify_semantic_duplicate_relation(
            target_path="/tmp/absolute.py",
            existing_path="relative.py",
        )
