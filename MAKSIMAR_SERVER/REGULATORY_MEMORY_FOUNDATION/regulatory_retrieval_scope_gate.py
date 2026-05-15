from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_memory_routing_models import (
    build_regulatory_memory_routing_registry,
)


@dataclass(frozen=True, slots=True)
class RegulatoryRetrievalScopeGate:
    gate_id: str
    route_ids: Tuple[str, ...]
    routing_registry_ready: bool
    tenant_scope_required: bool
    business_scope_required: bool
    jurisdiction_scope_required: bool
    source_scope_required: bool
    same_tenant_only: bool
    read_only: bool
    cross_tenant_retrieval_allowed: bool
    cross_tenant_merge_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    auto_routing_merge_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    gate_ready: bool

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError("gate_id must be non-empty")
        if not self.route_ids:
            raise ValueError("route_ids must be non-empty")
        if self.routing_registry_ready is not True:
            raise ValueError("routing_registry_ready must be True")
        if self.tenant_scope_required is not True:
            raise ValueError("tenant_scope_required must be True")
        if self.business_scope_required is not True:
            raise ValueError("business_scope_required must be True")
        if self.jurisdiction_scope_required is not True:
            raise ValueError("jurisdiction_scope_required must be True")
        if self.source_scope_required is not True:
            raise ValueError("source_scope_required must be True")
        if self.same_tenant_only is not True:
            raise ValueError("same_tenant_only must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.cross_tenant_retrieval_allowed:
            raise ValueError("cross_tenant_retrieval_allowed must be False")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.auto_routing_merge_allowed:
            raise ValueError("auto_routing_merge_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.gate_ready is not True:
            raise ValueError("gate_ready must be True")


def build_regulatory_retrieval_scope_gate() -> RegulatoryRetrievalScopeGate:
    registry = build_regulatory_memory_routing_registry()

    return RegulatoryRetrievalScopeGate(
        gate_id="regulatory_retrieval_scope_gate_step_8_001",
        route_ids=tuple(route.route_id for route in registry.routes),
        routing_registry_ready=registry.registry_ready,
        tenant_scope_required=registry.tenant_scope_required,
        business_scope_required=registry.business_scope_required,
        jurisdiction_scope_required=registry.jurisdiction_scope_required,
        source_scope_required=registry.source_scope_required,
        same_tenant_only=True,
        read_only=registry.read_only,
        cross_tenant_retrieval_allowed=registry.cross_tenant_retrieval_allowed,
        cross_tenant_merge_allowed=registry.cross_tenant_merge_allowed,
        cross_jurisdiction_merge_allowed=registry.cross_jurisdiction_merge_allowed,
        auto_routing_merge_allowed=registry.auto_routing_merge_allowed,
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
        direct_core_write_allowed=registry.direct_core_write_allowed,
        gate_ready=registry.registry_ready,
    )


def build_regulatory_retrieval_scope_gate_preview() -> Dict[str, object]:
    gate = build_regulatory_retrieval_scope_gate()

    return {
        "preview_id": "regulatory_retrieval_scope_gate_preview_step_8_001",
        "preview_ready": gate.gate_ready,
        "gate_id": gate.gate_id,
        "route_ids": gate.route_ids,
        "route_count": len(gate.route_ids),
        "routing_registry_ready": gate.routing_registry_ready,
        "tenant_scope_required": gate.tenant_scope_required,
        "business_scope_required": gate.business_scope_required,
        "jurisdiction_scope_required": gate.jurisdiction_scope_required,
        "source_scope_required": gate.source_scope_required,
        "same_tenant_only": gate.same_tenant_only,
        "read_only": gate.read_only,
        "cross_tenant_retrieval_allowed": gate.cross_tenant_retrieval_allowed,
        "cross_tenant_merge_allowed": gate.cross_tenant_merge_allowed,
        "cross_jurisdiction_merge_allowed": gate.cross_jurisdiction_merge_allowed,
        "auto_routing_merge_allowed": gate.auto_routing_merge_allowed,
        "runtime_mutation_allowed": gate.runtime_mutation_allowed,
        "direct_core_write_allowed": gate.direct_core_write_allowed,
    }
