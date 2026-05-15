from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_memory_routing_models import (
    build_regulatory_memory_routing_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_retrieval_scope_gate import (
    build_regulatory_retrieval_scope_gate_preview,
)


@dataclass(frozen=True, slots=True)
class CrossTenantLeakGuardResult:
    guard_id: str
    checked_route_ids: Tuple[str, ...]
    tenant_ids: Tuple[str, ...]
    blocked_decisions: Tuple[str, ...]
    retrieval_scope_gate_ready: bool
    leak_guard_ready: bool
    leak_detected: bool
    cross_tenant_retrieval_allowed: bool
    cross_tenant_merge_allowed: bool
    auto_routing_merge_allowed: bool
    read_only: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.guard_id:
            raise ValueError("guard_id must be non-empty")
        if not self.checked_route_ids:
            raise ValueError("checked_route_ids must be non-empty")
        if not self.tenant_ids:
            raise ValueError("tenant_ids must be non-empty")
        if not self.blocked_decisions:
            raise ValueError("blocked_decisions must be non-empty")
        if self.retrieval_scope_gate_ready is not True:
            raise ValueError("retrieval_scope_gate_ready must be True")
        if self.leak_guard_ready is not True:
            raise ValueError("leak_guard_ready must be True")
        if self.leak_detected:
            raise ValueError("leak_detected must be False")
        if self.cross_tenant_retrieval_allowed:
            raise ValueError("cross_tenant_retrieval_allowed must be False")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.auto_routing_merge_allowed:
            raise ValueError("auto_routing_merge_allowed must be False")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")


def build_cross_tenant_leak_guard_result() -> CrossTenantLeakGuardResult:
    registry = build_regulatory_memory_routing_registry()
    scope_gate = build_regulatory_retrieval_scope_gate_preview()

    blocked_decisions = tuple(
        route.route_decision for route in registry.routes if route.route_decision.startswith("deny_")
    )

    return CrossTenantLeakGuardResult(
        guard_id="cross_tenant_leak_guard_result_step_8_001",
        checked_route_ids=tuple(route.route_id for route in registry.routes),
        tenant_ids=tuple(sorted({route.tenant_id for route in registry.routes})),
        blocked_decisions=blocked_decisions,
        retrieval_scope_gate_ready=scope_gate["preview_ready"],
        leak_guard_ready=scope_gate["preview_ready"] is True and registry.registry_ready,
        leak_detected=False,
        cross_tenant_retrieval_allowed=registry.cross_tenant_retrieval_allowed,
        cross_tenant_merge_allowed=registry.cross_tenant_merge_allowed,
        auto_routing_merge_allowed=registry.auto_routing_merge_allowed,
        read_only=registry.read_only,
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
        direct_core_write_allowed=registry.direct_core_write_allowed,
        deployment_allowed_now=registry.deployment_allowed_now,
    )


def build_cross_tenant_leak_guard_preview() -> Dict[str, object]:
    result = build_cross_tenant_leak_guard_result()

    return {
        "preview_id": "cross_tenant_leak_guard_preview_step_8_001",
        "preview_ready": result.leak_guard_ready,
        "guard_id": result.guard_id,
        "checked_route_ids": result.checked_route_ids,
        "checked_route_count": len(result.checked_route_ids),
        "tenant_ids": result.tenant_ids,
        "tenant_count": len(result.tenant_ids),
        "blocked_decisions": result.blocked_decisions,
        "retrieval_scope_gate_ready": result.retrieval_scope_gate_ready,
        "leak_detected": result.leak_detected,
        "cross_tenant_retrieval_allowed": result.cross_tenant_retrieval_allowed,
        "cross_tenant_merge_allowed": result.cross_tenant_merge_allowed,
        "auto_routing_merge_allowed": result.auto_routing_merge_allowed,
        "read_only": result.read_only,
        "runtime_mutation_allowed": result.runtime_mutation_allowed,
        "direct_core_write_allowed": result.direct_core_write_allowed,
        "deployment_allowed_now": result.deployment_allowed_now,
    }
