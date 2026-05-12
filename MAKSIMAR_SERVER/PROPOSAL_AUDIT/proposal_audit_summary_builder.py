from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.PROPOSAL_AUDIT.approval_read_model import build_approval_read_model
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.audit_inspector_binding import build_audit_inspector_binding
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_spine_models import (
    build_proposal_audit_spine_contract,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_inspector_binding import (
    build_proposal_inspector_binding,
)


def build_proposal_audit_summary() -> Dict[str, object]:
    contract = build_proposal_audit_spine_contract()
    proposal = build_proposal_inspector_binding()
    audit = build_audit_inspector_binding()
    approval = build_approval_read_model()

    summary_ready = (
        contract.spine_ready
        and proposal["binding_ready"] is True
        and audit["binding_ready"] is True
        and approval["approval_read_model_ready"] is True
        and contract.code_write_allowed is False
        and contract.action_execution_allowed is False
    )

    return {
        "summary_id": "proposal_audit_summary_phase_6_2_001",
        "summary_ready": summary_ready,
        "roadmap_family": contract.roadmap_family,
        "phase_id": contract.phase_id,
        "track_scope": contract.track_scope,
        "proposal_visible": contract.proposal_visible,
        "audit_visible": contract.audit_visible,
        "approval_visible": contract.approval_visible,
        "proposal_binding_ready": proposal["binding_ready"],
        "audit_binding_ready": audit["binding_ready"],
        "approval_read_model_ready": approval["approval_read_model_ready"],
        "existing_surfaces_reused": contract.existing_surfaces_reused,
        "operator_review_required": contract.operator_review_required,
        "approval_granted_by_default": contract.approval_granted_by_default,
        "code_write_allowed": contract.code_write_allowed,
        "action_execution_allowed": contract.action_execution_allowed,
        "sandbox_execution_allowed_now": contract.sandbox_execution_allowed_now,
        "self_expansion_allowed_now": contract.self_expansion_allowed_now,
        "productization_allowed_now": contract.productization_allowed_now,
        "controlled_codegen_allowed_next": summary_ready,
    }
