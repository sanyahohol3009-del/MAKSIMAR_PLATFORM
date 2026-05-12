from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_operator_review_package
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_spine_models import (
    build_proposal_audit_spine_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_APPROVAL_SURFACES: Tuple[str, ...] = (
    "docs/security_governance/APPROVAL_AND_CONSENT_MODEL_v1.md",
    "docs/security_governance/governed_action_model/GOVERNED_ACTION_BASELINE_v1.md",
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_operator_review_builder.py",
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_candidate_builder.py",
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_preview_builder.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_approval_read_model() -> Dict[str, object]:
    contract = build_proposal_audit_spine_contract()
    review = build_memory_operator_review_package()
    missing = _missing(REQUIRED_APPROVAL_SURFACES)

    approval_read_model_ready = (
        contract.approval_visible is True
        and review["review_ready"] is True
        and review["operator_approval_required"] is True
        and review["operator_approval_granted"] is False
        and missing == ()
    )

    return {
        "approval_read_model_id": "approval_read_model_phase_6_2_001",
        "approval_read_model_ready": approval_read_model_ready,
        "required_surfaces": REQUIRED_APPROVAL_SURFACES,
        "missing_surfaces": missing,
        "approval_visible": contract.approval_visible,
        "operator_review_required": contract.operator_review_required,
        "operator_approval_required": review["operator_approval_required"],
        "operator_approval_granted": review["operator_approval_granted"],
        "approval_granted_by_default": contract.approval_granted_by_default,
        "release_allowed_without_operator_approval": False,
        "code_write_allowed": contract.code_write_allowed,
        "action_execution_allowed": contract.action_execution_allowed,
        "runtime_mutation_allowed": False,
    }
