from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_artifact_context_builder import (
    build_codegen_artifact_context,
)
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_boundary_models import build_codegen_boundary_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_intent_models import build_codegen_intent_contract
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.codegen_proposal_builder import build_codegen_proposal_context
from MAKSIMAR_SERVER.CODEGEN_CONTEXT.controlled_codegen_models import (
    build_controlled_codegen_context_contract,
)


def build_codegen_read_summary() -> Dict[str, object]:
    contract = build_controlled_codegen_context_contract()
    intent = build_codegen_intent_contract()
    boundary = build_codegen_boundary_contract()
    artifact = build_codegen_artifact_context()
    proposal = build_codegen_proposal_context()

    read_summary_ready = (
        contract.controlled_codegen_context_ready
        and intent.intent_contract_ready
        and boundary.boundary_contract_ready
        and artifact["artifact_context_ready"] is True
        and proposal["proposal_context_ready"] is True
        and contract.direct_core_write_allowed is False
        and contract.deployment_allowed is False
        and contract.sandbox_execution_allowed_now is False
    )

    return {
        "summary_id": "codegen_read_summary_phase_6_3_001",
        "summary_ready": read_summary_ready,
        "roadmap_family": contract.roadmap_family,
        "phase_id": contract.phase_id,
        "track_scope": contract.track_scope,
        "existing_surfaces_reused": contract.existing_surfaces_reused,
        "intent_models_ready": intent.intent_contract_ready,
        "boundary_models_ready": boundary.boundary_contract_ready,
        "artifact_context_ready": artifact["artifact_context_ready"],
        "proposal_package_ready": proposal["proposal_context_ready"],
        "operator_preview_required": contract.operator_preview_required,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "deployment_allowed": contract.deployment_allowed,
        "sandbox_execution_allowed_now": contract.sandbox_execution_allowed_now,
        "self_expansion_allowed_now": contract.self_expansion_allowed_now,
        "productization_allowed_now": contract.productization_allowed_now,
        "sandbox_owner_review_allowed_next": read_summary_ready,
    }
