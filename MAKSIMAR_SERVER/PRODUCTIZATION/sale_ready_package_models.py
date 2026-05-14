from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.PRODUCTIZATION.product_readiness_models import build_product_readiness_preview


SaleReadyPackageItemKind = Literal[
    "architecture_summary",
    "governance_summary",
    "operator_acceptance",
    "security_boundary_summary",
    "deployment_boundary_review",
    "rollback_readiness",
    "roadmap_acceptance_index",
]


@dataclass(frozen=True, slots=True)
class SaleReadyPackageItem:
    item_id: str
    item_kind: SaleReadyPackageItemKind
    operator_visible: bool
    source_bound: bool
    approval_required: bool
    release_claim_allowed: bool
    external_deploy_allowed: bool
    item_ready: bool

    def __post_init__(self) -> None:
        if not self.item_id:
            raise ValueError("item_id must be non-empty")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.external_deploy_allowed:
            raise ValueError("external_deploy_allowed must be False")
        if self.item_ready is not True:
            raise ValueError("item_ready must be True")


@dataclass(frozen=True, slots=True)
class SaleReadyPackage:
    package_id: str
    roadmap_family: str
    phase_id: str
    package_items: Tuple[SaleReadyPackageItem, ...]
    product_readiness_ready: bool
    sale_ready_package_ready: bool
    operator_visible: bool
    approval_required: bool
    no_hidden_autonomy_required: bool
    deployment_boundary_review_required: bool
    external_deploy_allowed: bool
    productization_claim_allowed: bool

    def __post_init__(self) -> None:
        if not self.package_id:
            raise ValueError("package_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.8":
            raise ValueError("phase_id must be PHASE 6.8")
        if not self.package_items:
            raise ValueError("package_items must be non-empty")
        if self.product_readiness_ready is not True:
            raise ValueError("product_readiness_ready must be True")
        if self.sale_ready_package_ready is not True:
            raise ValueError("sale_ready_package_ready must be True")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.no_hidden_autonomy_required is not True:
            raise ValueError("no_hidden_autonomy_required must be True")
        if self.deployment_boundary_review_required is not True:
            raise ValueError("deployment_boundary_review_required must be True")
        if self.external_deploy_allowed:
            raise ValueError("external_deploy_allowed must be False")
        if self.productization_claim_allowed is not True:
            raise ValueError("productization_claim_allowed must be True")
        if not all(item.item_ready for item in self.package_items):
            raise ValueError("all package items must be ready")


def build_sale_ready_package() -> SaleReadyPackage:
    readiness = build_product_readiness_preview()

    items = (
        SaleReadyPackageItem("sale_item_architecture_summary", "architecture_summary", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_governance_summary", "governance_summary", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_operator_acceptance", "operator_acceptance", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_security_boundary", "security_boundary_summary", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_deployment_boundary_review", "deployment_boundary_review", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_rollback_readiness", "rollback_readiness", True, True, True, True, False, True),
        SaleReadyPackageItem("sale_item_roadmap_acceptance_index", "roadmap_acceptance_index", True, True, True, True, False, True),
    )

    return SaleReadyPackage(
        package_id="sale_ready_package_phase_6_8_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.8",
        package_items=items,
        product_readiness_ready=readiness["preview_ready"],
        sale_ready_package_ready=readiness["preview_ready"] is True,
        operator_visible=True,
        approval_required=True,
        no_hidden_autonomy_required=True,
        deployment_boundary_review_required=True,
        external_deploy_allowed=False,
        productization_claim_allowed=True,
    )
