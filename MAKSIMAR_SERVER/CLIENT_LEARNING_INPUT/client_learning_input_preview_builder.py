from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.client_metrics_filter_models import (
    build_client_metrics_filter_policy,
)
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.learning_input_pack_models import (
    build_learning_input_pack,
)
from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.privacy_tenant_boundary_models import (
    build_privacy_tenant_boundary_preview,
)


def build_client_learning_input_preview() -> Dict[str, object]:
    filter_policy = build_client_metrics_filter_policy()
    boundary = build_privacy_tenant_boundary_preview()
    pack = build_learning_input_pack()

    preview_path = (
        "client_metrics_filter_policy",
        "privacy_tenant_boundary",
        "learning_input_pack",
        "proposal_route_required",
        "human_review_required",
        "polyglot_model_worker_next_only",
    )

    preview_ready = (
        filter_policy.filter_policy_ready
        and boundary["preview_ready"] is True
        and pack.pack_ready
        and pack.automatic_training_allowed is False
        and pack.direct_model_mutation_allowed is False
        and pack.runtime_mutation_allowed is False
    )

    return {
        "preview_id": "client_learning_input_preview_phase_6_6_001",
        "preview_ready": preview_ready,
        "preview_path": preview_path,
        "filter_policy_id": filter_policy.policy_id,
        "privacy_tenant_boundary_preview_id": boundary["preview_id"],
        "learning_input_pack_id": pack.pack_id,
        "learning_input_item_count": len(pack.items),
        "source_bound": pack.source_bound,
        "tenant_boundary_ready": pack.tenant_boundary_ready,
        "privacy_boundary_ready": pack.privacy_boundary_ready,
        "proposal_route_required": pack.proposal_route_required,
        "human_review_required": pack.human_review_required,
        "automatic_training_allowed": pack.automatic_training_allowed,
        "direct_model_mutation_allowed": pack.direct_model_mutation_allowed,
        "runtime_mutation_allowed": pack.runtime_mutation_allowed,
        "productization_allowed_now": pack.productization_allowed_now,
        "polyglot_model_worker_allowed_next": pack.polyglot_model_worker_allowed_next,
    }
