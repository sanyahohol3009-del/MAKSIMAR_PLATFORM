from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT.client_metrics_filter_models import (
    build_client_metrics_filter_policy,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PRIVACY_TENANT_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/customer_metrics_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_trust_scope_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_federation_policy_models.py",
    "MAKSIMAR_SERVER/MEMORY_SYNC/node_memory_scope_models.py",
    "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py",
    "MAKSIMAR_SERVER/SELF_EXPANSION_GATE/self_expansion_preview_builder.py",
)


@dataclass(frozen=True, slots=True)
class PrivacyTenantBoundaryContract:
    contract_id: str
    source_bound: bool
    tenant_isolation_required: bool
    personal_data_redaction_required: bool
    cross_tenant_merge_allowed: bool
    raw_payload_storage_allowed: bool
    automatic_training_allowed: bool
    runtime_mutation_allowed: bool
    productization_allowed_now: bool
    missing_required_surfaces: Tuple[str, ...]
    boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.tenant_isolation_required is not True:
            raise ValueError("tenant_isolation_required must be True")
        if self.personal_data_redaction_required is not True:
            raise ValueError("personal_data_redaction_required must be True")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.raw_payload_storage_allowed:
            raise ValueError("raw_payload_storage_allowed must be False")
        if self.automatic_training_allowed:
            raise ValueError("automatic_training_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.productization_allowed_now:
            raise ValueError("productization_allowed_now must be False")
        if self.missing_required_surfaces:
            raise ValueError(f"missing required surfaces: {self.missing_required_surfaces}")
        if self.boundary_ready is not True:
            raise ValueError("boundary_ready must be True")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_privacy_tenant_boundary_contract() -> PrivacyTenantBoundaryContract:
    filter_policy = build_client_metrics_filter_policy()
    missing = _missing(REQUIRED_PRIVACY_TENANT_SURFACES)

    return PrivacyTenantBoundaryContract(
        contract_id="privacy_tenant_boundary_contract_phase_6_6_001",
        source_bound=filter_policy.source_bound_required,
        tenant_isolation_required=filter_policy.tenant_boundary_required,
        personal_data_redaction_required=filter_policy.personal_data_redaction_required,
        cross_tenant_merge_allowed=False,
        raw_payload_storage_allowed=filter_policy.raw_payload_allowed,
        automatic_training_allowed=filter_policy.automatic_training_allowed,
        runtime_mutation_allowed=filter_policy.runtime_mutation_allowed,
        productization_allowed_now=filter_policy.productization_allowed_now,
        missing_required_surfaces=missing,
        boundary_ready=missing == (),
    )


def build_privacy_tenant_boundary_preview() -> Dict[str, object]:
    contract = build_privacy_tenant_boundary_contract()

    return {
        "preview_id": "privacy_tenant_boundary_preview_phase_6_6_001",
        "preview_ready": contract.boundary_ready,
        "required_surfaces": REQUIRED_PRIVACY_TENANT_SURFACES,
        "missing_required_surfaces": contract.missing_required_surfaces,
        "source_bound": contract.source_bound,
        "tenant_isolation_required": contract.tenant_isolation_required,
        "personal_data_redaction_required": contract.personal_data_redaction_required,
        "cross_tenant_merge_allowed": contract.cross_tenant_merge_allowed,
        "raw_payload_storage_allowed": contract.raw_payload_storage_allowed,
        "automatic_training_allowed": contract.automatic_training_allowed,
        "runtime_mutation_allowed": contract.runtime_mutation_allowed,
        "productization_allowed_now": contract.productization_allowed_now,
    }
