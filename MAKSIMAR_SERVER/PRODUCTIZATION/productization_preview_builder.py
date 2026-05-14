from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.PRODUCTIZATION.deployment_boundary_review import (
    build_deployment_boundary_review_preview,
)
from MAKSIMAR_SERVER.PRODUCTIZATION.no_hidden_autonomy_gate import build_no_hidden_autonomy_gate
from MAKSIMAR_SERVER.PRODUCTIZATION.operator_acceptance_package_builder import (
    build_operator_acceptance_preview,
)
from MAKSIMAR_SERVER.PRODUCTIZATION.product_readiness_models import build_product_readiness_preview
from MAKSIMAR_SERVER.PRODUCTIZATION.sale_ready_package_models import build_sale_ready_package


def build_productization_preview() -> Dict[str, object]:
    readiness = build_product_readiness_preview()
    sale_package = build_sale_ready_package()
    deployment = build_deployment_boundary_review_preview()
    operator = build_operator_acceptance_preview()
    no_hidden_autonomy = build_no_hidden_autonomy_gate()

    preview_path = (
        "product_readiness_model",
        "sale_ready_package_model",
        "deployment_boundary_review",
        "operator_acceptance_package",
        "no_hidden_autonomy_gate",
        "roadmap_v5_1_closure_next_only",
    )

    preview_ready = (
        readiness["preview_ready"] is True
        and sale_package.sale_ready_package_ready is True
        and deployment["preview_ready"] is True
        and operator["preview_ready"] is True
        and no_hidden_autonomy["gate_ready"] is True
    )

    return {
        "preview_id": "productization_preview_phase_6_8_001",
        "preview_ready": preview_ready,
        "roadmap_family": "memory_roadmap_v5_1",
        "phase_id": "PHASE 6.8",
        "track_scope": "productization_sale_ready_sovereign_ai",
        "preview_path": preview_path,
        "product_readiness": readiness,
        "sale_ready_package_id": sale_package.package_id,
        "deployment_boundary": deployment,
        "operator_acceptance": operator,
        "no_hidden_autonomy": no_hidden_autonomy,
        "sale_ready_claim_allowed": no_hidden_autonomy["sale_ready_claim_allowed"],
        "operator_approval_required": operator["operator_approval_required"],
        "operator_approval_granted": operator["operator_approval_granted"],
        "hidden_autonomy_allowed": no_hidden_autonomy["hidden_autonomy_allowed"],
        "direct_core_write_allowed": no_hidden_autonomy["direct_core_write_allowed"],
        "auto_apply_allowed": no_hidden_autonomy["auto_apply_allowed"],
        "runtime_mutation_allowed": no_hidden_autonomy["runtime_mutation_allowed"],
        "deployment_allowed_now": no_hidden_autonomy["deployment_allowed_now"],
        "external_release_allowed_now": no_hidden_autonomy["external_release_allowed_now"],
        "roadmap_v5_1_closure_allowed_next": no_hidden_autonomy["roadmap_v5_1_closure_allowed_next"],
    }
