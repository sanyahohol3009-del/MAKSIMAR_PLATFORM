from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


FederationBoundaryKind = Literal[
    "tenant_boundary",
    "personal_boundary",
    "jurisdiction_boundary",
    "enterprise_policy_boundary",
    "subordinate_backend_boundary",
]


@dataclass(frozen=True, slots=True)
class MemoryFederationBoundary:
    boundary_id: str
    boundary_kind: FederationBoundaryKind
    from_scope: str
    to_scope: str
    crossing_allowed: bool
    approval_required: bool
    evidence_required: bool
    automatic_merge_allowed: bool
    boundary_ready: bool

    def __post_init__(self) -> None:
        if not self.boundary_id:
            raise ValueError("boundary_id must be non-empty")
        if not self.from_scope:
            raise ValueError("from_scope must be non-empty")
        if not self.to_scope:
            raise ValueError("to_scope must be non-empty")
        if self.from_scope == self.to_scope:
            raise ValueError("from_scope and to_scope must differ")
        if self.approval_required is not True:
            raise ValueError("approval_required must be True")
        if self.evidence_required is not True:
            raise ValueError("evidence_required must be True")
        if self.automatic_merge_allowed:
            raise ValueError("automatic_merge_allowed must be False")
        if self.boundary_ready is not True:
            raise ValueError("boundary_ready must be True")


@dataclass(frozen=True, slots=True)
class MemoryFederationPolicy:
    policy_id: str
    boundaries: Tuple[MemoryFederationBoundary, ...]
    tenant_isolation_required: bool
    personal_memory_isolation_required: bool
    jurisdiction_isolation_required: bool
    cross_tenant_merge_allowed_without_approval: bool
    automatic_federation_write_allowed: bool
    runtime_mutation_allowed: bool
    federation_policy_ready: bool

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError("policy_id must be non-empty")
        if not self.boundaries:
            raise ValueError("boundaries must be non-empty")
        boundary_ids = {boundary.boundary_id for boundary in self.boundaries}
        if len(boundary_ids) != len(self.boundaries):
            raise ValueError("boundary_id values must be unique")
        if self.tenant_isolation_required is not True:
            raise ValueError("tenant_isolation_required must be True")
        if self.personal_memory_isolation_required is not True:
            raise ValueError("personal_memory_isolation_required must be True")
        if self.jurisdiction_isolation_required is not True:
            raise ValueError("jurisdiction_isolation_required must be True")
        if self.cross_tenant_merge_allowed_without_approval:
            raise ValueError("cross_tenant_merge_allowed_without_approval must be False")
        if self.automatic_federation_write_allowed:
            raise ValueError("automatic_federation_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(boundary.boundary_ready for boundary in self.boundaries):
            raise ValueError("all boundaries must be ready")
        if self.federation_policy_ready is not True:
            raise ValueError("federation_policy_ready must be True")


def build_memory_federation_policy() -> MemoryFederationPolicy:
    boundaries = (
        MemoryFederationBoundary(
            boundary_id="boundary_tenant_to_tenant",
            boundary_kind="tenant_boundary",
            from_scope="tenant_memory_a",
            to_scope="tenant_memory_b",
            crossing_allowed=False,
            approval_required=True,
            evidence_required=True,
            automatic_merge_allowed=False,
            boundary_ready=True,
        ),
        MemoryFederationBoundary(
            boundary_id="boundary_personal_to_tenant",
            boundary_kind="personal_boundary",
            from_scope="personal_memory",
            to_scope="tenant_memory",
            crossing_allowed=False,
            approval_required=True,
            evidence_required=True,
            automatic_merge_allowed=False,
            boundary_ready=True,
        ),
        MemoryFederationBoundary(
            boundary_id="boundary_country_to_country",
            boundary_kind="jurisdiction_boundary",
            from_scope="jurisdiction_de",
            to_scope="jurisdiction_ua",
            crossing_allowed=False,
            approval_required=True,
            evidence_required=True,
            automatic_merge_allowed=False,
            boundary_ready=True,
        ),
        MemoryFederationBoundary(
            boundary_id="boundary_enterprise_policy_to_runtime",
            boundary_kind="enterprise_policy_boundary",
            from_scope="enterprise_policy_memory",
            to_scope="runtime_policy",
            crossing_allowed=False,
            approval_required=True,
            evidence_required=True,
            automatic_merge_allowed=False,
            boundary_ready=True,
        ),
        MemoryFederationBoundary(
            boundary_id="boundary_subordinate_backend_to_canonical",
            boundary_kind="subordinate_backend_boundary",
            from_scope="subordinate_backend",
            to_scope="canonical_memory",
            crossing_allowed=False,
            approval_required=True,
            evidence_required=True,
            automatic_merge_allowed=False,
            boundary_ready=True,
        ),
    )

    return MemoryFederationPolicy(
        policy_id="memory_federation_policy_001",
        boundaries=boundaries,
        tenant_isolation_required=True,
        personal_memory_isolation_required=True,
        jurisdiction_isolation_required=True,
        cross_tenant_merge_allowed_without_approval=False,
        automatic_federation_write_allowed=False,
        runtime_mutation_allowed=False,
        federation_policy_ready=True,
    )
