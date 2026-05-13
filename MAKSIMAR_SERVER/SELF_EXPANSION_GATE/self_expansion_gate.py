from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_preview
from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_owner_review_preview
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.gap_to_proposal_builder import (
    build_gap_to_proposal_context,
)
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_readiness_models import (
    build_self_expansion_readiness_contract,
)


def build_self_expansion_gate() -> Dict[str, object]:
    readiness = build_self_expansion_readiness_contract()
    gap_proposal = build_gap_to_proposal_context()
    codegen = build_codegen_preview()
    sandbox_review = build_sandbox_owner_review_preview()

    gate_flow: Tuple[str, ...] = (
        "gap_detection",
        "gap_to_proposal_context",
        "proposal_audit_required",
        "controlled_codegen_context_required",
        "sandbox_owner_review_required",
        "human_approval_required",
        "client_metrics_learning_next_only",
    )

    gate_ready = (
        readiness.readiness_ready
        and gap_proposal["gap_to_proposal_ready"] is True
        and codegen["preview_ready"] is True
        and sandbox_review["preview_ready"] is True
        and readiness.proposal_only_self_expansion_allowed is True
        and readiness.autonomous_self_expansion_allowed is False
    )

    return {
        "gate_id": "self_expansion_gate_phase_6_5_001",
        "gate_ready": gate_ready,
        "gate_flow": gate_flow,
        "gap_to_proposal_context_id": gap_proposal["gap_to_proposal_context_id"],
        "codegen_preview_id": codegen["preview_id"],
        "sandbox_owner_review_preview_id": sandbox_review["preview_id"],
        "proposal_only_self_expansion_allowed": readiness.proposal_only_self_expansion_allowed,
        "autonomous_self_expansion_allowed": readiness.autonomous_self_expansion_allowed,
        "gap_detection_allowed": True,
        "proposal_preparation_allowed": True,
        "codegen_context_allowed": True,
        "sandbox_owner_review_required": readiness.sandbox_owner_review_required,
        "human_approval_required": readiness.human_approval_required,
        "direct_core_write_allowed": readiness.direct_core_write_allowed,
        "auto_apply_allowed": readiness.auto_apply_allowed,
        "deployment_allowed": readiness.deployment_allowed,
        "runtime_mutation_allowed": readiness.runtime_mutation_allowed,
        "productization_allowed_now": readiness.productization_allowed_now,
        "client_metrics_learning_allowed_next": gate_ready,
    }
