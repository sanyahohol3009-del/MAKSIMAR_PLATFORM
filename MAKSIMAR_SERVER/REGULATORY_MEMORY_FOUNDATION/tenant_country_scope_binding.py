from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_isolation_gate import (
    build_tenant_regulatory_isolation_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_scope_models import (
    build_tenant_regulatory_scope_registry,
)


@dataclass(frozen=True, slots=True)
class TenantCountryScopeBinding:
    binding_id: str
    tenant_ids: Tuple[str, ...]
    business_ids: Tuple[str, ...]
    country_codes: Tuple[str, ...]
    jurisdiction_ids: Tuple[str, ...]
    tenant_country_pairs: Tuple[Tuple[str, str], ...]
    isolation_gate_ready: bool
    tenant_bound: bool
    jurisdiction_bound: bool
    source_bound_required: bool
    cross_tenant_merge_allowed: bool
    cross_tenant_read_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        if not self.binding_id:
            raise ValueError("binding_id must be non-empty")
        if not self.tenant_ids:
            raise ValueError("tenant_ids must be non-empty")
        if not self.business_ids:
            raise ValueError("business_ids must be non-empty")
        if not self.country_codes:
            raise ValueError("country_codes must be non-empty")
        if not self.jurisdiction_ids:
            raise ValueError("jurisdiction_ids must be non-empty")
        if not self.tenant_country_pairs:
            raise ValueError("tenant_country_pairs must be non-empty")
        if self.isolation_gate_ready is not True:
            raise ValueError("isolation_gate_ready must be True")
        if self.tenant_bound is not True:
            raise ValueError("tenant_bound must be True")
        if self.jurisdiction_bound is not True:
            raise ValueError("jurisdiction_bound must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_tenant_read_allowed:
            raise ValueError("cross_tenant_read_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.binding_ready is not True:
            raise ValueError("binding_ready must be True")


def build_tenant_country_scope_binding() -> TenantCountryScopeBinding:
    registry = build_tenant_regulatory_scope_registry()
    isolation = build_tenant_regulatory_isolation_preview()

    tenant_country_pairs = tuple(
        (entry.tenant_id, entry.country_code)
        for entry in registry.entries
    )

    return TenantCountryScopeBinding(
        binding_id="tenant_country_scope_binding_step_3_001",
        tenant_ids=tuple(sorted({entry.tenant_id for entry in registry.entries})),
        business_ids=tuple(sorted({entry.business_id for entry in registry.entries})),
        country_codes=tuple(sorted({entry.country_code for entry in registry.entries})),
        jurisdiction_ids=tuple(sorted({entry.jurisdiction_id for entry in registry.entries})),
        tenant_country_pairs=tenant_country_pairs,
        isolation_gate_ready=isolation["preview_ready"],
        tenant_bound=True,
        jurisdiction_bound=True,
        source_bound_required=registry.source_bound_required,
        cross_tenant_merge_allowed=registry.cross_tenant_merge_allowed,
        cross_tenant_read_allowed=isolation["cross_tenant_read_allowed"],
        runtime_mutation_allowed=registry.runtime_mutation_allowed,
        direct_core_write_allowed=registry.direct_core_write_allowed,
        deployment_allowed_now=registry.deployment_allowed_now,
        binding_ready=isolation["preview_ready"] is True and registry.registry_ready,
    )


def build_tenant_country_scope_binding_preview() -> Dict[str, object]:
    binding = build_tenant_country_scope_binding()

    return {
        "preview_id": "tenant_country_scope_binding_preview_step_3_001",
        "preview_ready": binding.binding_ready,
        "binding_id": binding.binding_id,
        "tenant_ids": binding.tenant_ids,
        "business_ids": binding.business_ids,
        "country_codes": binding.country_codes,
        "jurisdiction_ids": binding.jurisdiction_ids,
        "tenant_country_pairs": binding.tenant_country_pairs,
        "tenant_count": len(binding.tenant_ids),
        "business_count": len(binding.business_ids),
        "country_count": len(binding.country_codes),
        "jurisdiction_count": len(binding.jurisdiction_ids),
        "isolation_gate_ready": binding.isolation_gate_ready,
        "tenant_bound": binding.tenant_bound,
        "jurisdiction_bound": binding.jurisdiction_bound,
        "source_bound_required": binding.source_bound_required,
        "cross_tenant_merge_allowed": binding.cross_tenant_merge_allowed,
        "cross_tenant_read_allowed": binding.cross_tenant_read_allowed,
        "runtime_mutation_allowed": binding.runtime_mutation_allowed,
        "direct_core_write_allowed": binding.direct_core_write_allowed,
        "deployment_allowed_now": binding.deployment_allowed_now,
    }
