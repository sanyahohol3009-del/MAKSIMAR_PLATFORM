from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.PROPOSAL_AUDIT.proposal_audit_preview_builder import (
    build_proposal_audit_preview,
)


def build_proposal_audit_spine_summary() -> Dict[str, object]:
    preview = build_proposal_audit_preview()
    summary = preview["summary"]

    return {
        "summary_id": "proposal_audit_spine_summary_phase_6_2_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": summary["roadmap_family"],
        "phase_id": summary["phase_id"],
        "track_scope": summary["track_scope"],
        "proposal_visible": summary["proposal_visible"],
        "audit_visible": summary["audit_visible"],
        "approval_visible": summary["approval_visible"],
        "operator_review_required": summary["operator_review_required"],
        "approval_granted_by_default": summary["approval_granted_by_default"],
        "code_write_allowed": summary["code_write_allowed"],
        "action_execution_allowed": summary["action_execution_allowed"],
        "controlled_codegen_allowed_next": summary["controlled_codegen_allowed_next"],
        "sandbox_execution_allowed_now": summary["sandbox_execution_allowed_now"],
        "self_expansion_allowed_now": summary["self_expansion_allowed_now"],
        "productization_allowed_now": summary["productization_allowed_now"],
    }
