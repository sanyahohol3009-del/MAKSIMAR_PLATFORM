from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.jurisdiction_registry_preview_builder import (
    build_jurisdiction_registry_preview,
)


TenantRegulatoryScopeKind = Literal[
    "tenant_policy_scope",
    "business_regulatory_scope",
    "country_regulatory_scope",
    "compliance_evidence_scope",
]

TenantRegulatoryDataClass = Literal[
    "policy_reference",
    "regulatory_reference",
    "compliance_reference",
    "evidence_reference",
]


@dataclass(frozen=True, slots=True)
class TenantRegulatoryScopeEntry:
    tenant_scope_id: str
    tenant_id: str
    business_id: str
    country_code: str
    jurisdiction_id: str
    scope_kind: TenantRegulatoryScopeKind
    data_class: TenantRegulatoryDataClass
    tenant_bound: bool
    jurisdiction_bound: bool
    source_bound_required: bool
    version_required: bool
    effective_date_required: bool
    cross_tenant_merge_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    runtime_mutation_allowed: bool
    scope_ready: bool

    def __post_init__(self) -> None:
        if not self.tenant_scope_id:
            raise ValueError("tenant_scope_id must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.business_id:
            raise ValueError("business_id must be non-empty")
        if not self.country_code:
            raise ValueError("country_code must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if self.tenant_bound is not True:
            raise ValueError("tenant_bound must be True")
        if self.jurisdiction_bound is not True:
            raise ValueError("jurisdiction_bound must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.version_required is not True:
            raise ValueError("version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.scope_ready is not True:
            raise ValueError("scope_ready must be True")


@dataclass(frozen=True, slots=True)
class TenantRegulatoryScopeRegistry:
    registry_id: str
    entries: Tuple[TenantRegulatoryScopeEntry, ...]
    tenant_id_required: bool
    business_id_required: bool
    country_code_required: bool
    jurisdiction_id_required: bool
    tenant_isolation_required: bool
    source_bound_required: bool
    cross_tenant_merge_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    registry_ready: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.entries:
            raise ValueError("entries must be non-empty")
        scope_ids = {entry.tenant_scope_id for entry in self.entries}
        if len(scope_ids) != len(self.entries):
            raise ValueError("tenant_scope_id values must be unique")
        if self.tenant_id_required is not True:
            raise ValueError("tenant_id_required must be True")
        if self.business_id_required is not True:
            raise ValueError("business_id_required must be True")
        if self.country_code_required is not True:
            raise ValueError("country_code_required must be True")
        if self.jurisdiction_id_required is not True:
            raise ValueError("jurisdiction_id_required must be True")
        if self.tenant_isolation_required is not True:
            raise ValueError("tenant_isolation_required must be True")
        if self.source_bound_required is not True:
            raise ValueError("source_bound_required must be True")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if not all(entry.scope_ready for entry in self.entries):
            raise ValueError("all tenant regulatory scopes must be ready")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")


def build_tenant_regulatory_scope_registry() -> TenantRegulatoryScopeRegistry:
    jurisdiction = build_jurisdiction_registry_preview()

    entries = (
        TenantRegulatoryScopeEntry(
            tenant_scope_id="tenant_scope_demo_de_regulatory_001",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="DE",
            jurisdiction_id="jurisdiction_de_country",
            scope_kind="country_regulatory_scope",
            data_class="regulatory_reference",
            tenant_bound=True,
            jurisdiction_bound=True,
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        TenantRegulatoryScopeEntry(
            tenant_scope_id="tenant_scope_demo_eu_compliance_001",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="EU",
            jurisdiction_id="jurisdiction_eu_union",
            scope_kind="compliance_evidence_scope",
            data_class="compliance_reference",
            tenant_bound=True,
            jurisdiction_bound=True,
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        TenantRegulatoryScopeEntry(
            tenant_scope_id="tenant_scope_demo_ua_policy_001",
            tenant_id="tenant_demo_ua_001",
            business_id="business_demo_ua_001",
            country_code="UA",
            jurisdiction_id="jurisdiction_ua_country",
            scope_kind="tenant_policy_scope",
            data_class="policy_reference",
            tenant_bound=True,
            jurisdiction_bound=True,
            source_bound_required=True,
            version_required=True,
            effective_date_required=True,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
    )

    allowed_jurisdiction_ids = set(jurisdiction["jurisdiction_ids"])
    for entry in entries:
        if entry.jurisdiction_id not in allowed_jurisdiction_ids:
            raise ValueError(f"unknown jurisdiction_id: {entry.jurisdiction_id}")

    return TenantRegulatoryScopeRegistry(
        registry_id="tenant_regulatory_scope_registry_step_3_001",
        entries=entries,
        tenant_id_required=True,
        business_id_required=True,
        country_code_required=True,
        jurisdiction_id_required=True,
        tenant_isolation_required=True,
        source_bound_required=True,
        cross_tenant_merge_allowed=False,
        cross_jurisdiction_merge_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
        registry_ready=jurisdiction["preview_ready"] is True,
    )
