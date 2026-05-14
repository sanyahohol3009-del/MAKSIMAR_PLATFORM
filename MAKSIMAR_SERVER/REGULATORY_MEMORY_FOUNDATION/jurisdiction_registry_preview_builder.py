from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.country_jurisdiction_binding import (
    build_country_jurisdiction_binding_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.jurisdiction_applicability_builder import (
    build_jurisdiction_applicability_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.jurisdiction_registry_models import (
    build_jurisdiction_registry,
)


def build_jurisdiction_registry_preview() -> Dict[str, object]:
    registry = build_jurisdiction_registry()
    binding = build_country_jurisdiction_binding_preview()
    applicability = build_jurisdiction_applicability_preview()

    preview_path = (
        "jurisdiction_registry_models",
        "country_jurisdiction_binding",
        "jurisdiction_applicability_matrix",
        "tenant_regulatory_scope_next",
    )

    preview_ready = (
        registry.registry_ready
        and binding["preview_ready"] is True
        and applicability["preview_ready"] is True
        and registry.cross_jurisdiction_merge_allowed is False
    )

    return {
        "preview_id": "jurisdiction_registry_preview_step_2_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 2 — Country / Jurisdiction Registry Binding",
        "next_step": "STEP 3 — Tenant Regulatory Scope & Isolation",
        "preview_path": preview_path,
        "registry_id": registry.registry_id,
        "country_count": len(binding["country_codes"]),
        "jurisdiction_count": len(registry.entries),
        "applicability_pair_count": applicability["applicability_pair_count"],
        "country_codes": binding["country_codes"],
        "jurisdiction_ids": binding["jurisdiction_ids"],
        "country_code_required": registry.country_code_required,
        "jurisdiction_id_required": registry.jurisdiction_id_required,
        "applicability_scope_required": registry.applicability_scope_required,
        "source_bound_required": registry.source_bound_required,
        "version_required": True,
        "effective_date_required": True,
        "cross_jurisdiction_merge_allowed": registry.cross_jurisdiction_merge_allowed,
        "runtime_mutation_allowed": False,
        "direct_core_write_allowed": False,
        "deployment_allowed_now": False,
    }
