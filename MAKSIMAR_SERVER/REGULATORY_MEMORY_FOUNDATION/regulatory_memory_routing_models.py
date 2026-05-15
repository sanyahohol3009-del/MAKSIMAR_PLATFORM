from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_update_preview_builder import (
    build_regulatory_update_approval_preview,
)


RegulatoryRetrievalScope = Literal[
    "tenant_regulatory_scope",
    "tenant_compliance_scope",
    "jurisdiction_evidence_scope",
    "approval_audit_scope",
]

RegulatoryRouteDecision = Literal[
    "allow_same_tenant_read_only",
    "deny_cross_tenant",
    "deny_cross_jurisdiction_merge",
    "deny_unapproved_mutation",
]


@dataclass(frozen=True, slots=True)
class RegulatoryMemoryRoute:
    route_id: str
    retrieval_scope: RegulatoryRetrievalScope
    route_decision: RegulatoryRouteDecision
    tenant_id: str
    business_id: str
    country_code: str
    jurisdiction_id: str
    source_ref: str
    tenant_bound: bool
    business_bound: bool
    jurisdiction_bound: bool
    source_bound: bool
    read_only: bool
    approval_required: bool
    approval_granted: bool
    cross_tenant_retrieval_allowed: bool
    cross_tenant_merge_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    runtime_mutation_allowed: bool
    route_ready: bool

    def __post_init__(self) -> None:
        if not self.route_id:
            raise ValueError("route_id must be non-empty")
        if not self.tenant_id:
            raise ValueError("tenant_id must be non-empty")
        if not self.business_id:
            raise ValueError("business_id must be non-empty")
        if not self.country_code:
            raise ValueError("country_code must be non-empty")
        if not self.jurisdiction_id:
            raise ValueError("jurisdiction_id must be non-empty")
        if not self.source_ref:
            raise ValueError("source_ref must be non-empty")
        if self.tenant_bound is not True:
            raise ValueError("tenant_bound must be True")
        if self.business_bound is not True:
            raise ValueError("business_bound must be True")
        if self.jurisdiction_bound is not True:
            raise ValueError("jurisdiction_bound must be True")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.read_only is not True:
            raise ValueError("read_only must be True")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.approval_granted:
            raise ValueError("approval_granted must be False")
        if self.cross_tenant_retrieval_allowed:
            raise ValueError("cross_tenant_retrieval_allowed must be False")
        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_jurisdiction_merge_allowed:
            raise ValueError("cross_jurisdiction_merge_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.route_ready is not True:
            raise ValueError("route_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryMemoryRoutingRegistry:
    registry_id: str
    routes: Tuple[RegulatoryMemoryRoute, ...]
    update_approval_ready: bool
    tenant_scope_required: bool
    business_scope_required: bool
    jurisdiction_scope_required: bool
    source_scope_required: bool
    read_only: bool
    cross_tenant_retrieval_allowed: bool
    cross_tenant_merge_allowed: bool
    cross_jurisdiction_merge_allowed: bool
    auto_routing_merge_allowed: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    registry_ready: bool

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must be non-empty")
        if not self.routes:
            raise ValueError("routes must be non-empty")
        route_ids = {route.route_id for route in self.routes}
        if len(route_ids) != len(self.routes):
            raise ValueError("route_id values must be unique")
        if self.update_approval_ready is not True:
            raise ValueError("update_approval_ready must be True")
        if self.tenant_scope_required is not True:
            raise ValueError("tenant_scope_required must be True")
        if self.business_scope_required is not True:
            raise ValueError("business_scope_required must be True")
        if self.jurisdiction_scope_required is not True:
            raise ValueError("jurisdiction_scope_required must be True")
        if self.source_scope_required is not True:
            raise ValueError("source_scope_required must be True")
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
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if not all(route.route_ready for route in self.routes):
            raise ValueError("all regulatory routes must be ready")
        if self.registry_ready is not True:
            raise ValueError("registry_ready must be True")


def build_regulatory_memory_routing_registry() -> RegulatoryMemoryRoutingRegistry:
    update = build_regulatory_update_approval_preview()

    routes = (
        RegulatoryMemoryRoute(
            route_id="regulatory_route_de_law_read_only_001",
            retrieval_scope="tenant_regulatory_scope",
            route_decision="allow_same_tenant_read_only",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="DE",
            jurisdiction_id="jurisdiction_de_country",
            source_ref="reg_source_de_demo_law_v1",
            tenant_bound=True,
            business_bound=True,
            jurisdiction_bound=True,
            source_bound=True,
            read_only=True,
            approval_required=True,
            approval_granted=False,
            cross_tenant_retrieval_allowed=False,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            route_ready=True,
        ),
        RegulatoryMemoryRoute(
            route_id="regulatory_route_ua_policy_read_only_001",
            retrieval_scope="tenant_compliance_scope",
            route_decision="allow_same_tenant_read_only",
            tenant_id="tenant_demo_ua_001",
            business_id="business_demo_ua_001",
            country_code="UA",
            jurisdiction_id="jurisdiction_ua_country",
            source_ref="reg_source_ua_demo_policy_v1",
            tenant_bound=True,
            business_bound=True,
            jurisdiction_bound=True,
            source_bound=True,
            read_only=True,
            approval_required=True,
            approval_granted=False,
            cross_tenant_retrieval_allowed=False,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            route_ready=True,
        ),
        RegulatoryMemoryRoute(
            route_id="regulatory_route_cross_tenant_denied_001",
            retrieval_scope="approval_audit_scope",
            route_decision="deny_cross_tenant",
            tenant_id="tenant_demo_de_001",
            business_id="business_demo_de_001",
            country_code="DE",
            jurisdiction_id="jurisdiction_de_country",
            source_ref="reg_source_de_demo_law_v1",
            tenant_bound=True,
            business_bound=True,
            jurisdiction_bound=True,
            source_bound=True,
            read_only=True,
            approval_required=True,
            approval_granted=False,
            cross_tenant_retrieval_allowed=False,
            cross_tenant_merge_allowed=False,
            cross_jurisdiction_merge_allowed=False,
            runtime_mutation_allowed=False,
            route_ready=True,
        ),
    )

    return RegulatoryMemoryRoutingRegistry(
        registry_id="regulatory_memory_routing_registry_step_8_001",
        routes=routes,
        update_approval_ready=update["preview_ready"],
        tenant_scope_required=True,
        business_scope_required=True,
        jurisdiction_scope_required=True,
        source_scope_required=True,
        read_only=True,
        cross_tenant_retrieval_allowed=False,
        cross_tenant_merge_allowed=False,
        cross_jurisdiction_merge_allowed=False,
        auto_routing_merge_allowed=False,
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
        registry_ready=update["preview_ready"] is True,
    )
