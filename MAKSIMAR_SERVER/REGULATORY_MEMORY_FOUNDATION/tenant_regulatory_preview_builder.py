from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_country_scope_binding import (
    build_tenant_country_scope_binding_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_isolation_gate import (
    build_tenant_regulatory_isolation_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_scope_models import (
    build_tenant_regulatory_scope_registry,
)


def build_tenant_regulatory_scope_preview() -> Dict[str, object]:
    registry = build_tenant_regulatory_scope_registry()
    isolation = build_tenant_regulatory_isolation_preview()
    binding = build_tenant_country_scope_binding_preview()

    preview_path = (
        "tenant_regulatory_scope_models",
        "tenant_regulatory_isolation_gate",
        "tenant_country_scope_binding",
        "source_version_effective_date_precedence_next",
    )

    preview_ready = (
        registry.registry_ready
        and isolation["preview_ready"] is True
        and binding["preview_ready"] is True
        and registry.cross_tenant_merge_allowed is False
    )

    return {
        "preview_id": "tenant_regulatory_scope_preview_step_3_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 3 — Tenant Regulatory Scope & Isolation",
        "next_step": "STEP 4 — Source Version / Effective Date / Precedence",
        "preview_path": preview_path,
        "registry_id": registry.registry_id,
        "tenant_scope_count": len(registry.entries),
        "tenant_count": binding["tenant_count"],
        "business_count": binding["business_count"],
        "country_count": binding["country_count"],
        "jurisdiction_count": binding["jurisdiction_count"],
        "tenant_ids": binding["tenant_ids"],
        "business_ids": binding["business_ids"],
        "country_codes": binding["country_codes"],
        "jurisdiction_ids": binding["jurisdiction_ids"],
        "tenant_id_required": registry.tenant_id_required,
        "business_id_required": registry.business_id_required,
        "country_code_required": registry.country_code_required,
        "jurisdiction_id_required": registry.jurisdiction_id_required,
        "tenant_isolation_required": registry.tenant_isolation_required,
        "source_bound_required": registry.source_bound_required,
        "version_required": True,
        "effective_date_required": True,
        "cross_tenant_merge_allowed": registry.cross_tenant_merge_allowed,
        "cross_tenant_read_allowed": isolation["cross_tenant_read_allowed"],
        "cross_jurisdiction_merge_allowed": registry.cross_jurisdiction_merge_allowed,
        "runtime_mutation_allowed": registry.runtime_mutation_allowed,
        "direct_core_write_allowed": registry.direct_core_write_allowed,
        "deployment_allowed_now": registry.deployment_allowed_now,
    }
