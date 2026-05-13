from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_preview_builder import (
    build_self_expansion_preview,
)


def build_self_expansion_gate_summary() -> Dict[str, object]:
    preview = build_self_expansion_preview()
    gate = preview["gate"]

    return {
        "summary_id": "self_expansion_gate_summary_phase_6_5_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.5",
        "track_scope": "bootstrapped_self_expansion_gate",
        "proposal_only_self_expansion_allowed": gate["proposal_only_self_expansion_allowed"],
        "autonomous_self_expansion_allowed": gate["autonomous_self_expansion_allowed"],
        "gap_detection_allowed": gate["gap_detection_allowed"],
        "proposal_preparation_allowed": gate["proposal_preparation_allowed"],
        "sandbox_owner_review_required": gate["sandbox_owner_review_required"],
        "human_approval_required": gate["human_approval_required"],
        "direct_core_write_allowed": gate["direct_core_write_allowed"],
        "auto_apply_allowed": gate["auto_apply_allowed"],
        "deployment_allowed": gate["deployment_allowed"],
        "runtime_mutation_allowed": gate["runtime_mutation_allowed"],
        "productization_allowed_now": gate["productization_allowed_now"],
        "client_metrics_learning_allowed_next": gate["client_metrics_learning_allowed_next"],
    }
