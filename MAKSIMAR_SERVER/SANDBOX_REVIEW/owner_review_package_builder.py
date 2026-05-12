from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_operator_review_package
from MAKSIMAR_SERVER.SANDBOX_REVIEW.evaluation_result_reader import build_evaluation_result_reader
from MAKSIMAR_SERVER.SANDBOX_REVIEW.sandbox_review_models import build_sandbox_review_contract


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_OWNER_REVIEW_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/oob_dashboard/owner_review_package_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/owner_review_package_models.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/approval_queue_panel_content_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/audit_timeline_panel_content_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/operator_audit_visibility_contract.py",
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_operator_review_builder.py",
    "MAKSIMAR_SERVER/PROPOSAL_AUDIT/approval_read_model.py",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_owner_review_package() -> Dict[str, object]:
    contract = build_sandbox_review_contract()
    evaluation_reader = build_evaluation_result_reader()
    memory_review = build_memory_operator_review_package()
    missing = _missing(REQUIRED_OWNER_REVIEW_SURFACES)

    owner_review_package_ready = (
        contract.owner_review_package_ready
        and evaluation_reader["evaluation_result_reader_ready"] is True
        and evaluation_reader["evaluation_passed"] is True
        and memory_review["review_ready"] is True
        and missing == ()
    )

    return {
        "owner_review_package_id": "owner_review_package_phase_6_4_001",
        "owner_review_package_ready": owner_review_package_ready,
        "required_surfaces": REQUIRED_OWNER_REVIEW_SURFACES,
        "missing_surfaces": missing,
        "evaluation_result_reader_id": evaluation_reader["evaluation_result_reader_id"],
        "memory_review_package_id": memory_review["review_package_id"],
        "owner_review_required": contract.owner_review_required,
        "owner_approval_required": contract.owner_approval_required,
        "owner_approval_granted": False,
        "owner_approval_granted_by_default": contract.owner_approval_granted_by_default,
        "risk_summary_required": True,
        "diff_preview_required": True,
        "sandbox_result_required": True,
        "simulation_result_required": True,
        "evaluation_result_required": True,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "self_expansion_allowed_now": contract.self_expansion_allowed_now,
        "productization_allowed_now": contract.productization_allowed_now,
    }
