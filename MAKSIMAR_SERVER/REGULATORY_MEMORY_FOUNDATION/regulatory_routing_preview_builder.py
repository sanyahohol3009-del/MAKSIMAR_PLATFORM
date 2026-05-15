from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.cross_tenant_leak_guard import (
    build_cross_tenant_leak_guard_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_memory_routing_models import (
    build_regulatory_memory_routing_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_retrieval_scope_gate import (
    build_regulatory_retrieval_scope_gate_preview,
)


def build_regulatory_routing_preview() -> Dict[str, object]:
    registry = build_regulatory_memory_routing_registry()
    scope_gate = build_regulatory_retrieval_scope_gate_preview()
    leak_guard = build_cross_tenant_leak_guard_preview()

    preview_path = (
        "regulatory_memory_routing_models",
        "regulatory_retrieval_scope_gate",
        "cross_tenant_leak_guard",
        "regulatory_memory_final_closure_next",
    )

    preview_ready = (
        registry.registry_ready
        and scope_gate["preview_ready"] is True
        and leak_guard["preview_ready"] is True
        and leak_guard["leak_detected"] is False
        and registry.cross_tenant_retrieval_allowed is False
        and registry.cross_tenant_merge_allowed is False
    )

    return {
        "preview_id": "regulatory_routing_preview_step_8_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 8 — Regulatory Routing / No Cross-Tenant Leak",
        "next_step": "STEP 9 — Regulatory Memory Final Closure",
        "preview_path": preview_path,
        "registry_id": registry.registry_id,
        "route_count": len(registry.routes),
        "tenant_count": leak_guard["tenant_count"],
        "checked_route_count": leak_guard["checked_route_count"],
        "blocked_decisions": leak_guard["blocked_decisions"],
        "tenant_scope_required": registry.tenant_scope_required,
        "business_scope_required": registry.business_scope_required,
        "jurisdiction_scope_required": registry.jurisdiction_scope_required,
        "source_scope_required": registry.source_scope_required,
        "same_tenant_only": scope_gate["same_tenant_only"],
        "read_only": registry.read_only,
        "leak_detected": leak_guard["leak_detected"],
        "cross_tenant_retrieval_allowed": registry.cross_tenant_retrieval_allowed,
        "cross_tenant_merge_allowed": registry.cross_tenant_merge_allowed,
        "cross_jurisdiction_merge_allowed": registry.cross_jurisdiction_merge_allowed,
        "auto_routing_merge_allowed": registry.auto_routing_merge_allowed,
        "runtime_mutation_allowed": registry.runtime_mutation_allowed,
        "direct_core_write_allowed": registry.direct_core_write_allowed,
        "deployment_allowed_now": registry.deployment_allowed_now,
    }
