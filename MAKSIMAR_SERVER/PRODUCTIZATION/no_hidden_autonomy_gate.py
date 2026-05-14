from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.PRODUCTIZATION.operator_acceptance_package_builder import (
    build_operator_acceptance_preview,
)
from MAKSIMAR_SERVER.PRODUCTIZATION.product_readiness_models import build_product_readiness_preview
from MAKSIMAR_SERVER.PRODUCTIZATION.sale_ready_package_models import build_sale_ready_package


def build_no_hidden_autonomy_gate() -> Dict[str, object]:
    readiness = build_product_readiness_preview()
    sale_package = build_sale_ready_package()
    operator = build_operator_acceptance_preview()

    blocked_capabilities: Tuple[str, ...] = (
        "hidden_autonomous_self_expansion",
        "direct_core_write",
        "auto_apply",
        "runtime_mutation",
        "deployment_without_operator_approval",
        "external_release_without_acceptance",
        "cross_tenant_data_merge",
        "automatic_training_mutation",
    )

    gate_ready = (
        readiness["preview_ready"] is True
        and sale_package.sale_ready_package_ready is True
        and operator["preview_ready"] is True
        and readiness["hidden_autonomy_allowed"] is False
        and readiness["deployment_allowed_now"] is False
        and operator["operator_approval_granted"] is False
    )

    return {
        "gate_id": "no_hidden_autonomy_gate_phase_6_8_001",
        "gate_ready": gate_ready,
        "blocked_capabilities": blocked_capabilities,
        "hidden_autonomy_allowed": False,
        "direct_core_write_allowed": False,
        "auto_apply_allowed": False,
        "runtime_mutation_allowed": False,
        "deployment_allowed_now": False,
        "external_release_allowed_now": False,
        "operator_approval_required": operator["operator_approval_required"],
        "operator_approval_granted": operator["operator_approval_granted"],
        "sale_ready_claim_allowed": gate_ready,
        "roadmap_v5_1_closure_allowed_next": gate_ready,
    }
