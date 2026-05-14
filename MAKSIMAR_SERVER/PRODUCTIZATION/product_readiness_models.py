from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Literal, Tuple

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_polyglot_model_worker_preview


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ProductReadinessArea = Literal[
    "memory_governance",
    "proposal_audit",
    "controlled_codegen",
    "sandbox_owner_review",
    "self_expansion_gate",
    "client_learning_input",
    "polyglot_model_worker_bridge",
    "product_hardening",
    "operations_boundary",
    "operator_visibility",
]

REQUIRED_PRODUCT_READINESS_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_candidate_builder.py",
    "MAKSIMAR_SERVER/MEMORY_ACCEPTANCE/memory_release_preview_builder.py",
    "MAKSIMAR_SERVER/PROPOSAL_AUDIT/proposal_audit_preview_builder.py",
    "MAKSIMAR_SERVER/CODEGEN_CONTEXT/codegen_preview_builder.py",
    "MAKSIMAR_SERVER/SANDBOX_REVIEW/sandbox_owner_review_preview_builder.py",
    "MAKSIMAR_SERVER/SELF_EXPANSION_GATE/self_expansion_preview_builder.py",
    "MAKSIMAR_SERVER/CLIENT_LEARNING_INPUT/client_learning_input_preview_builder.py",
    "MAKSIMAR_SERVER/POLYGLOT_MODEL_WORKER_BRIDGE/polyglot_bridge_preview_builder.py",
    "MAKSIMAR_CORE_LIB/product_hardening_onboarding_packaging/product_hardening_onboarding_packaging_contract.py",
    "MAKSIMAR_CORE_LIB/operations_deployment_backup_incidents/operations_deployment_backup_incidents_contract.py",
    "MAKSIMAR_CORE_LIB/products_layer/product_registry.py",
    "MAKSIMAR_CORE_LIB/products_layer/product_models.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/operator_audit_visibility_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/owner_review_package_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/rollback_readiness_contract.py",
    "docs/security_governance",
)


@dataclass(frozen=True, slots=True)
class ProductReadinessAreaStatus:
    area_id: str
    area: ProductReadinessArea
    ready: bool
    operator_visible: bool
    approval_required: bool
    hidden_autonomy_allowed: bool
    deployment_allowed_now: bool
    auto_apply_allowed: bool

    def __post_init__(self) -> None:
        if not self.area_id:
            raise ValueError("area_id must be non-empty")
        if self.ready is not True:
            raise ValueError("ready must be True")
        if self.operator_visible is not True:
            raise ValueError("operator_visible must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.hidden_autonomy_allowed:
            raise ValueError("hidden_autonomy_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")


@dataclass(frozen=True, slots=True)
class ProductReadinessContract:
    contract_id: str
    roadmap_family: str
    phase_id: str
    track_scope: str
    areas: Tuple[ProductReadinessAreaStatus, ...]
    missing_required_surfaces: Tuple[str, ...]
    upstream_polyglot_ready: bool
    product_readiness_model_ready: bool
    sale_ready_packaging_allowed: bool
    operator_acceptance_required: bool
    deployment_boundary_review_required: bool
    hidden_autonomy_allowed: bool
    direct_core_write_allowed: bool
    auto_apply_allowed: bool
    deployment_allowed_now: bool
    external_release_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.phase_id != "PHASE 6.8":
            raise ValueError("phase_id must be PHASE 6.8")
        if self.track_scope != "productization_sale_ready_sovereign_ai":
            raise ValueError("track_scope must be productization_sale_ready_sovereign_ai")
        if not self.areas:
            raise ValueError("areas must be non-empty")
        if self.missing_required_surfaces:
            raise ValueError(f"missing required surfaces: {self.missing_required_surfaces}")
        if self.upstream_polyglot_ready is not True:
            raise ValueError("upstream_polyglot_ready must be True")
        if self.product_readiness_model_ready is not True:
            raise ValueError("product_readiness_model_ready must be True")
        if self.sale_ready_packaging_allowed is not True:
            raise ValueError("sale_ready_packaging_allowed must be True")
        if self.operator_acceptance_required is not True:
            raise ValueError("operator_acceptance_required must be True")
        if self.deployment_boundary_review_required is not True:
            raise ValueError("deployment_boundary_review_required must be True")
        if self.hidden_autonomy_allowed:
            raise ValueError("hidden_autonomy_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.external_release_allowed_now:
            raise ValueError("external_release_allowed_now must be False")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_product_readiness_contract() -> ProductReadinessContract:
    polyglot = build_polyglot_model_worker_preview()
    missing = _missing(REQUIRED_PRODUCT_READINESS_SURFACES)

    areas = (
        ProductReadinessAreaStatus("area_memory_governance", "memory_governance", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_proposal_audit", "proposal_audit", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_controlled_codegen", "controlled_codegen", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_sandbox_owner_review", "sandbox_owner_review", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_self_expansion_gate", "self_expansion_gate", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_client_learning_input", "client_learning_input", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_polyglot_model_worker_bridge", "polyglot_model_worker_bridge", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_product_hardening", "product_hardening", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_operations_boundary", "operations_boundary", True, True, True, False, False, False),
        ProductReadinessAreaStatus("area_operator_visibility", "operator_visibility", True, True, True, False, False, False),
    )

    return ProductReadinessContract(
        contract_id="product_readiness_contract_phase_6_8_001",
        roadmap_family="memory_roadmap_v5_1",
        phase_id="PHASE 6.8",
        track_scope="productization_sale_ready_sovereign_ai",
        areas=areas,
        missing_required_surfaces=missing,
        upstream_polyglot_ready=polyglot["preview_ready"],
        product_readiness_model_ready=missing == () and polyglot["preview_ready"] is True,
        sale_ready_packaging_allowed=True,
        operator_acceptance_required=True,
        deployment_boundary_review_required=True,
        hidden_autonomy_allowed=False,
        direct_core_write_allowed=False,
        auto_apply_allowed=False,
        deployment_allowed_now=False,
        external_release_allowed_now=False,
    )


def build_product_readiness_preview() -> Dict[str, object]:
    contract = build_product_readiness_contract()

    return {
        "preview_id": "product_readiness_preview_phase_6_8_001",
        "preview_ready": contract.product_readiness_model_ready,
        "required_surfaces": REQUIRED_PRODUCT_READINESS_SURFACES,
        "missing_required_surfaces": contract.missing_required_surfaces,
        "area_count": len(contract.areas),
        "upstream_polyglot_ready": contract.upstream_polyglot_ready,
        "sale_ready_packaging_allowed": contract.sale_ready_packaging_allowed,
        "operator_acceptance_required": contract.operator_acceptance_required,
        "deployment_boundary_review_required": contract.deployment_boundary_review_required,
        "hidden_autonomy_allowed": contract.hidden_autonomy_allowed,
        "direct_core_write_allowed": contract.direct_core_write_allowed,
        "auto_apply_allowed": contract.auto_apply_allowed,
        "deployment_allowed_now": contract.deployment_allowed_now,
        "external_release_allowed_now": contract.external_release_allowed_now,
    }
