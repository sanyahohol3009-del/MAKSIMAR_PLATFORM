from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_artifact_context_builder import (
    build_codegen_artifact_context,
)
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_boundary_models import build_codegen_boundary_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_intent_models import build_codegen_intent_contract
from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_summary


def build_codegen_proposal_context() -> Dict[str, object]:
    intent = build_codegen_intent_contract()
    boundary = build_codegen_boundary_contract()
    artifact = build_codegen_artifact_context()
    proposal_audit = build_proposal_audit_summary()

    proposal_package_flow: Tuple[str, ...] = (
        "codegen_intent_contract",
        "codegen_boundary_contract",
        "codegen_artifact_context",
        "proposal_audit_spine",
        "operator_preview_required",
        "sandbox_later_only",
    )

    proposal_context_ready = (
        intent.intent_contract_ready
        and boundary.boundary_contract_ready
        and artifact["artifact_context_ready"] is True
        and proposal_audit["summary_ready"] is True
        and proposal_audit["controlled_codegen_allowed_next"] is True
    )

    return {
        "codegen_proposal_context_id": "codegen_proposal_context_phase_6_3_001",
        "proposal_context_ready": proposal_context_ready,
        "proposal_package_flow": proposal_package_flow,
        "intent_count": len(intent.intents),
        "boundary_rule_count": len(boundary.rules),
        "artifact_context_ready": artifact["artifact_context_ready"],
        "proposal_audit_summary_ready": proposal_audit["summary_ready"],
        "operator_review_required": proposal_audit["operator_review_required"],
        "approval_granted_by_default": proposal_audit["approval_granted_by_default"],
        "direct_core_write_allowed": boundary.immutable_core_protected is False,
        "deployment_allowed": False,
        "sandbox_execution_allowed_now": False,
        "runtime_mutation_allowed": False,
    }
