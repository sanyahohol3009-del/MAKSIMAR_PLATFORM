from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_scope_models import (
    build_tenant_regulatory_scope_registry,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_TENANT_ISOLATION_SURFACES: Tuple[str, ...] = (
    "docs/architecture/foundation/country_jurisdiction_registry_binding_v1.md",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/regulatory_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/legal_jurisdiction_models.py",
    "MAKSIMAR_SERVER/MEMORY_SYNC/node_memory_scope_models.py",
    "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_federation_policy_models.py",
)


@dataclass(frozen=True, slots=True)
class TenantRegulatoryIsolationGate:
    gate_id: str
    required_surfaces: Tuple[str, ...]
    missing_surfaces: Tuple[str, ...]
    tenant_scope_registry_ready: bool
    tenant_isolation_required: bool
    cross_tenant_merge_allowed: bool
    cross_tenant_read_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    source_bound_required: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    gate_ready: bool

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError("gate_id must be non-empty")
        if self.missing_surfaces:
            raise ValueError(f"missing tenant isolation surfaces: {self.missing_surfaces}")
        if self.tenant_scope_registry_ready is not True:
            raise ValueError("tenant_scope_registry_ready must be True")
        if self.tenant_isolation_required is not True:
            raise ValueError("tenant_isolation_required must be True")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_tenant_read_allowed:
            raise ValueError("cross_tenant_read_allowed must be False")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.gate_ready is not True:
            raise ValueError("gate_ready must be True")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_tenant_regulatory_isolation_gate() -> TenantRegulatoryIsolationGate:
    registry = build_tenant_regulatory_scope_registry()
    missing = _missing(REQUIRED_TENANT_ISOLATION_SURFACES)

    return TenantRegulatoryIsolationGate(
        gate_id="tenant_regulatory_isolation_gate_step_3_001",
        required_surfaces=REQUIRED_TENANT_ISOLATION_SURFACES,
        missing_surfaces=missing,
        tenant_scope_registry_ready=registry.registry_ready,
        tenant_isolation_required=registry.tenant_isolation_required,
        cross_tenant_merge_allowed=False,
        cross_tenant_read_allowed=False,
        cross_jurisdiction_merge_allowed=registry.cross_jurisdiction_merge_allowed,
        source_bound_required=registry.source_bound_required,
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
        direct_core_write_allowed=registry.direct_core_write_allowed,
        deployment_allowed_now=registry.deployment_allowed_now,
        gate_ready=registry.registry_ready and missing == (),
    )


def build_tenant_regulatory_isolation_preview() -> Dict[str, object]:
    gate = build_tenant_regulatory_isolation_gate()

    return {
        "preview_id": "tenant_regulatory_isolation_preview_step_3_001",
        "preview_ready": gate.gate_ready,
        "gate_id": gate.gate_id,
        "required_surfaces": gate.required_surfaces,
        "missing_surfaces": gate.missing_surfaces,
        "tenant_scope_registry_ready": gate.tenant_scope_registry_ready,
        "tenant_isolation_required": gate.tenant_isolation_required,
        "cross_tenant_merge_allowed": gate.cross_tenant_merge_allowed,
        "cross_tenant_read_allowed": gate.cross_tenant_read_allowed,
        "cross_jurisdiction_merge_allowed": gate.cross_jurisdiction_merge_allowed,
        "source_bound_required": gate.source_bound_required,
        "runtime_mutation_allowed": gate.runtime_mutation_allowed,
        "direct_core_write_allowed": gate.direct_core_write_allowed,
        "deployment_allowed_now": gate.deployment_allowed_now,
    }
