from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.PRODUCTIZATION.sale_ready_package_models import build_sale_ready_package


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DEPLOYMENT_BOUNDARY_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/operations_deployment_backup_incidents/operations_deployment_backup_incidents_contract.py",
    "MAKSIMAR_CORE_LIB/runtime_observability/config_boundary_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/rollback_readiness_contract.py",
    "docs/security_governance/governed_action_model/WRITE_APPLY_BOUNDARY_v1.md",
    "docs/security_governance/governed_action_model/GOVERNED_ACTION_BASELINE_v1.md",
)


@dataclass(frozen=True, slots=True)
class DeploymentBoundaryReview:
    review_id: str
    missing_required_surfaces: Tuple[str, ...]
    sale_ready_package_ready: bool
    deployment_boundary_review_ready: bool
    deployment_allowed_now: bool
    external_release_allowed_now: bool
    rollback_required: bool
    operator_approval_required: bool
    security_boundary_required: bool
    hidden_autonomy_allowed: bool

    def __post_init__(self) -> None:
        if not self.review_id:
            raise ValueError("review_id must be non-empty")
        if self.missing_required_surfaces:
            raise ValueError(f"missing required surfaces: {self.missing_required_surfaces}")
        if self.sale_ready_package_ready is not True:
            raise ValueError("sale_ready_package_ready must be True")
        if self.deployment_boundary_review_ready is not True:
            raise ValueError("deployment_boundary_review_ready must be True")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.external_release_allowed_now:
            raise ValueError("external_release_allowed_now must be False")
        if self.rollback_required is not True:
            raise ValueError("rollback_required must be True")
        if self.operator_approval_required is not True:
            raise ValueError("operator_approval_required must be True")
        if self.security_boundary_required is not True:
            raise ValueError("security_boundary_required must be True")
        if self.hidden_autonomy_allowed:
            raise ValueError("hidden_autonomy_allowed must be False")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_deployment_boundary_review() -> DeploymentBoundaryReview:
    package = build_sale_ready_package()
    missing = _missing(REQUIRED_DEPLOYMENT_BOUNDARY_SURFACES)

    return DeploymentBoundaryReview(
        review_id="deployment_boundary_review_phase_6_8_001",
        missing_required_surfaces=missing,
        sale_ready_package_ready=package.sale_ready_package_ready,
        deployment_boundary_review_ready=missing == () and package.sale_ready_package_ready,
        deployment_allowed_now=False,
        external_release_allowed_now=False,
        rollback_required=True,
        operator_approval_required=True,
        security_boundary_required=True,
        hidden_autonomy_allowed=False,
    )


def build_deployment_boundary_review_preview() -> Dict[str, object]:
    review = build_deployment_boundary_review()

    return {
        "preview_id": "deployment_boundary_review_preview_phase_6_8_001",
        "preview_ready": review.deployment_boundary_review_ready,
        "required_surfaces": REQUIRED_DEPLOYMENT_BOUNDARY_SURFACES,
        "missing_required_surfaces": review.missing_required_surfaces,
        "deployment_allowed_now": review.deployment_allowed_now,
        "external_release_allowed_now": review.external_release_allowed_now,
        "rollback_required": review.rollback_required,
        "operator_approval_required": review.operator_approval_required,
        "security_boundary_required": review.security_boundary_required,
        "hidden_autonomy_allowed": review.hidden_autonomy_allowed,
    }
