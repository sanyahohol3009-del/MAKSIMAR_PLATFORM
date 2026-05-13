from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.client_learning_input_preview_builder import (
    build_client_learning_input_preview,
)


def build_client_learning_input_summary() -> Dict[str, object]:
    preview = build_client_learning_input_preview()

    return {
        "summary_id": "client_learning_input_summary_phase_6_6_001",
        "summary_ready": preview["preview_ready"],
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.6",
        "track_scope": "client_metrics_learning_input",
        "learning_input_item_count": preview["learning_input_item_count"],
        "source_bound": preview["source_bound"],
        "tenant_boundary_ready": preview["tenant_boundary_ready"],
        "privacy_boundary_ready": preview["privacy_boundary_ready"],
        "proposal_route_required": preview["proposal_route_required"],
        "human_review_required": preview["human_review_required"],
        "automatic_training_allowed": preview["automatic_training_allowed"],
        "direct_model_mutation_allowed": preview["direct_model_mutation_allowed"],
        "runtime_mutation_allowed": preview["runtime_mutation_allowed"],
        "productization_allowed_now": preview["productization_allowed_now"],
        "polyglot_model_worker_allowed_next": preview["polyglot_model_worker_allowed_next"],
    }
