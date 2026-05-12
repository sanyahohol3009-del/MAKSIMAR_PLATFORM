from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.PROPOSAL_AUDIT.approval_read_model import build_approval_read_model
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.audit_inspector_binding import build_audit_inspector_binding
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_summary_builder import (
    build_proposal_audit_summary,
)
from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_inspector_binding import (
    build_proposal_inspector_binding,
)


def build_proposal_audit_preview() -> Dict[str, object]:
    proposal = build_proposal_inspector_binding()
    audit = build_audit_inspector_binding()
    approval = build_approval_read_model()
    summary = build_proposal_audit_summary()

    preview_path = (
        "proposal_inspector_binding",
        "audit_inspector_binding",
        "approval_read_model",
        "operator_review_required",
        "proposal_audit_summary",
        "controlled_codegen_next_only",
    )

    preview_ready = (
        summary["summary_ready"] is True
        and proposal["binding_ready"] is True
        and audit["binding_ready"] is True
        and approval["approval_read_model_ready"] is True
    )

    return {
        "preview_id": "proposal_audit_preview_phase_6_2_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "proposal": proposal,
        "audit": audit,
        "approval": approval,
        "summary": summary,
        "code_write_allowed": summary["code_write_allowed"],
        "action_execution_allowed": summary["action_execution_allowed"],
        "sandbox_execution_allowed_now": summary["sandbox_execution_allowed_now"],
        "self_expansion_allowed_now": summary["self_expansion_allowed_now"],
        "productization_allowed_now": summary["productization_allowed_now"],
        "controlled_codegen_allowed_next": summary["controlled_codegen_allowed_next"],
    }
