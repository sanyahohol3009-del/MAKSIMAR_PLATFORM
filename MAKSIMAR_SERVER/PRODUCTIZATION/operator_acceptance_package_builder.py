from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.PRODUCTIZATION.deployment_boundary_review import (
    build_deployment_boundary_review_preview,
)
from MAKSIMAR_SERVER.PRODUCTIZATION.sale_ready_package_models import build_sale_ready_package


@dataclass(frozen=True, slots=True)
class OperatorAcceptancePackage:
    package_id: str
    acceptance_items: Tuple[str, ...]
    sale_ready_package_ready: bool
    deployment_boundary_review_ready: bool
    operator_acceptance_package_ready: bool
    operator_approval_required: bool
    operator_approval_granted: bool
    hidden_autonomy_allowed: bool
    deployment_allowed_now: bool
    external_release_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.package_id:
            raise ValueError("package_id must be non-empty")
        if not self.acceptance_items:
            raise ValueError("acceptance_items must be non-empty")
        if self.sale_ready_package_ready is not True:
            raise ValueError("sale_ready_package_ready must be True")
        if self.deployment_boundary_review_ready is not True:
            raise ValueError("deployment_boundary_review_ready must be True")
        if self.operator_acceptance_package_ready is not True:
            raise ValueError("operator_acceptance_package_ready must be True")
        if self.operator_approval_required is not True:
            raise ValueError("operator_approval_required must be True")
        if self.operator_approval_granted:
            raise ValueError("operator_approval_granted must be False until explicit operator action")
        if self.hidden_autonomy_allowed:
            raise ValueError("hidden_autonomy_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.external_release_allowed_now:
            raise ValueError("external_release_allowed_now must be False")


def build_operator_acceptance_package() -> OperatorAcceptancePackage:
    sale_package = build_sale_ready_package()
    deployment = build_deployment_boundary_review_preview()

    items = (
        "roadmap_v5_1_acceptance_chain_visible",
        "governance_chain_visible",
        "proposal_audit_chain_visible",
        "codegen_sandbox_owner_review_chain_visible",
        "polyglot_model_worker_bridge_visible",
        "deployment_boundary_review_visible",
        "rollback_readiness_visible",
        "no_hidden_autonomy_visible",
    )

    return OperatorAcceptancePackage(
        package_id="operator_acceptance_package_phase_6_8_001",
        acceptance_items=items,
        sale_ready_package_ready=sale_package.sale_ready_package_ready,
        deployment_boundary_review_ready=deployment["preview_ready"],
        operator_acceptance_package_ready=sale_package.sale_ready_package_ready and deployment["preview_ready"],
        operator_approval_required=True,
        operator_approval_granted=False,
        hidden_autonomy_allowed=False,
        deployment_allowed_now=False,
        external_release_allowed_now=False,
    )


def build_operator_acceptance_preview() -> Dict[str, object]:
    package = build_operator_acceptance_package()

    return {
        "preview_id": "operator_acceptance_preview_phase_6_8_001",
        "preview_ready": package.operator_acceptance_package_ready,
        "acceptance_items": package.acceptance_items,
        "acceptance_item_count": len(package.acceptance_items),
        "operator_approval_required": package.operator_approval_required,
        "operator_approval_granted": package.operator_approval_granted,
        "hidden_autonomy_allowed": package.hidden_autonomy_allowed,
        "deployment_allowed_now": package.deployment_allowed_now,
        "external_release_allowed_now": package.external_release_allowed_now,
    }
