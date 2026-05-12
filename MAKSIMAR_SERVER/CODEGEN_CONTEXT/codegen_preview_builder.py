from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_artifact_context_builder import (
    build_codegen_artifact_context,
)
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_boundary_models import build_codegen_boundary_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_intent_models import build_codegen_intent_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_proposal_builder import build_codegen_proposal_context
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_read_summary import build_codegen_read_summary


def build_codegen_preview() -> Dict[str, object]:
    intent = build_codegen_intent_contract()
    boundary = build_codegen_boundary_contract()
    artifact = build_codegen_artifact_context()
    proposal = build_codegen_proposal_context()
    summary = build_codegen_read_summary()

    preview_path = (
        "codegen_intent_models",
        "codegen_boundary_models",
        "codegen_artifact_context",
        "codegen_proposal_context",
        "codegen_read_summary",
        "sandbox_owner_review_next_only",
    )

    preview_ready = (
        summary["summary_ready"] is True
        and intent.intent_contract_ready
        and boundary.boundary_contract_ready
        and artifact["artifact_context_ready"] is True
        and proposal["proposal_context_ready"] is True
    )

    return {
        "preview_id": "codegen_preview_phase_6_3_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "intent_contract_id": intent.contract_id,
        "boundary_contract_id": boundary.contract_id,
        "artifact_context_id": artifact["artifact_context_id"],
        "proposal_context_id": proposal["codegen_proposal_context_id"],
        "summary": summary,
        "direct_core_write_allowed": summary["direct_core_write_allowed"],
        "deployment_allowed": summary["deployment_allowed"],
        "sandbox_execution_allowed_now": summary["sandbox_execution_allowed_now"],
        "self_expansion_allowed_now": summary["self_expansion_allowed_now"],
        "productization_allowed_now": summary["productization_allowed_now"],
        "sandbox_owner_review_allowed_next": summary["sandbox_owner_review_allowed_next"],
    }
