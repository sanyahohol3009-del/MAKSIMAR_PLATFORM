from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.tenant_regulatory_preview_builder import (
    build_tenant_regulatory_scope_preview,
)


RegulatorySourceStatus = Literal["draft", "active", "superseded", "withdrawn", "archived"]
RegulatorySourceKind = Literal[
    "law",
    "regulation",
    "administrative_guidance",
    "court_reference",
    "policy_reference",
    "compliance_reference",
]


@dataclass(frozen=True, slots=True)
class RegulatorySourceVersion:
    source_ref: str
    source_kind: RegulatorySourceKind
    source_version: str
    source_status: RegulatorySourceStatus
    tenant_scope_id: str
    tenant_id: str
    business_id: str
    country_code: str
    jurisdiction_id: str
    source_uri: str
    published_date: str
    effective_date: str
    retrieved_date: str
    source_bound: bool
    version_required: bool
    effective_date_required: bool
    precedence_required: bool
    approval_required: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    source_version_ready: bool

    def __post_init__(self) -> None:
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if not self.source_version:
            raise ValueError("source_version must be non-empty")
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
        if not self.source_uri:
            raise ValueError("source_uri must be non-empty")
        published = date.fromisoformat(self.published_date)
        effective = date.fromisoformat(self.effective_date)
        retrieved = date.fromisoformat(self.retrieved_date)
        if retrieved < published:
            raise ValueError("retrieved_date must be >= published_date")
        if effective < published:
            raise ValueError("effective_date must be >= published_date")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.version_required is not True:
            raise ValueError("version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.precedence_required is not True:
            raise ValueError("precedence_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.source_version_ready is not True:
            raise ValueError("source_version_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatorySourceVersionRegistry:
    registry_id: str
    sources: Tuple[RegulatorySourceVersion, ...]
    tenant_scope_ready: bool
    source_version_required: bool
    effective_date_required: bool
    jurisdiction_id_required: bool
    tenant_scope_id_required: bool
    precedence_required: bool
    approval_required: bool
    canonical_truth_update_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    registry_ready: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.sources:
            raise ValueError("sources must be non-empty")
        source_refs = {source.source_ref for source in self.sources}
        if len(source_refs) != len(self.sources):
            raise ValueError("source_ref values must be unique")
        if self.tenant_scope_ready is not True:
            raise ValueError("tenant_scope_ready must be True")
        if self.source_version_required is not True:
            raise ValueError("source_version_required must be True")
        if self.effective_date_required is not True:
            raise ValueError("effective_date_required must be True")
        if self.jurisdiction_id_required is not True:
            raise ValueError("jurisdiction_id_required must be True")
        if self.tenant_scope_id_required is not True:
            raise ValueError("tenant_scope_id_required must be True")
        if self.precedence_required is not True:
            raise ValueError("precedence_required must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.canonical_truth_update_allowed:
            raise ValueError("canonical_truth_update_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if not all(source.source_version_ready for source in self.sources):
            raise ValueError("all source versions must be ready")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")


def build_regulatory_source_version_registry() -> RegulatorySourceVersionRegistry:
    tenant_scope = build_tenant_regulatory_scope_preview()
    allowed_scope_ids = {
        "tenant_scope_demo_de_regulatory_001",
        "tenant_scope_demo_eu_compliance_001",
        "tenant_scope_demo_ua_policy_001",
    }

    sources = (
        RegulatorySourceVersion(
            source_ref="reg_source_de_demo_law_v1",
            source_kind="law",
            source_version="2026-01-01",
            source_status="active",
            tenant_scope_id="tenant_scope_demo_de_regulatory_001",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="DE",
            jurisdiction_id="jurisdiction_de_country",
            source_uri="source://de/demo/law/2026-01-01",
            published_date="2026-01-01",
            effective_date="2026-01-01",
            retrieved_date="2026-01-02",
            source_bound=True,
            version_required=True,
            effective_date_required=True,
            precedence_required=True,
            approval_required=True,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            source_version_ready=True,
        ),
        RegulatorySourceVersion(
            source_ref="reg_source_eu_demo_regulation_v1",
            source_kind="regulation",
            source_version="2026-01-15",
            source_status="active",
            tenant_scope_id="tenant_scope_demo_eu_compliance_001",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="EU",
            jurisdiction_id="jurisdiction_eu_union",
            source_uri="source://eu/demo/regulation/2026-01-15",
            published_date="2026-01-15",
            effective_date="2026-02-01",
            retrieved_date="2026-02-02",
            source_bound=True,
            version_required=True,
            effective_date_required=True,
            precedence_required=True,
            approval_required=True,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            source_version_ready=True,
        ),
        RegulatorySourceVersion(
            source_ref="reg_source_ua_demo_policy_v1",
            source_kind="policy_reference",
            source_version="2026-02-01",
            source_status="draft",
            tenant_scope_id="tenant_scope_demo_ua_policy_001",
            tenant_id="tenant_demo_ua_001",
            business_id="business_demo_ua_001",
            country_code="UA",
            jurisdiction_id="jurisdiction_ua_country",
            source_uri="source://ua/demo/policy/2026-02-01",
            published_date="2026-02-01",
            effective_date="2026-02-10",
            retrieved_date="2026-02-10",
            source_bound=True,
            version_required=True,
            effective_date_required=True,
            precedence_required=True,
            approval_required=True,
            canonical_truth_update_allowed=False,
            runtime_mutation_allowed=False,
            source_version_ready=True,
        ),
    )

    for source in sources:
        if source.tenant_scope_id not in allowed_scope_ids:
            raise ValueError(f"unknown tenant_scope_id: {source.tenant_scope_id}")

    return RegulatorySourceVersionRegistry(
        registry_id="regulatory_source_version_registry_step_4_001",
        sources=sources,
        tenant_scope_ready=tenant_scope["preview_ready"],
        source_version_required=True,
        effective_date_required=True,
        jurisdiction_id_required=True,
        tenant_scope_id_required=True,
        precedence_required=True,
        approval_required=True,
        canonical_truth_update_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
        registry_ready=tenant_scope["preview_ready"] is True,
    )
