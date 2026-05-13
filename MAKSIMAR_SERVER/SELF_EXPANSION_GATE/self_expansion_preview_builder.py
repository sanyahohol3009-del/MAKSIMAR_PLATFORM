from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.gap_to_proposal_builder import (
    build_gap_to_proposal_context,
)
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_gate import build_self_expansion_gate
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_readiness_models import (
    build_self_expansion_readiness_contract,
)


def build_self_expansion_preview() -> Dict[str, object]:
    readiness = build_self_expansion_readiness_contract()
    gap_proposal = build_gap_to_proposal_context()
    gate = build_self_expansion_gate()

    preview_path = (
        "self_expansion_readiness",
        "gap_detection",
        "gap_to_proposal_context",
        "proposal_audit_required",
        "controlled_codegen_context_required",
        "sandbox_owner_review_required",
        "human_approval_required",
        "client_metrics_learning_next_only",
    )

    preview_ready = (
        readiness.readiness_ready
        and gap_proposal["gap_to_proposal_ready"] is True
        and gate["gate_ready"] is True
    )

    return {
        "preview_id": "self_expansion_preview_phase_6_5_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "readiness_contract_id": readiness.contract_id,
        "gap_to_proposal_context": gap_proposal,
        "gate": gate,
        "proposal_only_self_expansion_allowed": gate["proposal_only_self_expansion_allowed"],
        "autonomous_self_expansion_allowed": gate["autonomous_self_expansion_allowed"],
        "direct_core_write_allowed": gate["direct_core_write_allowed"],
        "auto_apply_allowed": gate["auto_apply_allowed"],
        "deployment_allowed": gate["deployment_allowed"],
        "runtime_mutation_allowed": gate["runtime_mutation_allowed"],
        "productization_allowed_now": gate["productization_allowed_now"],
        "client_metrics_learning_allowed_next": gate["client_metrics_learning_allowed_next"],
    }
