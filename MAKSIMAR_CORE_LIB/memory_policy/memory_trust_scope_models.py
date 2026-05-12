from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple


TrustScopeKind = Literal[
    "canonical_memory",
    "regulatory_memory",
    "enterprise_policy_memory",
    "tenant_memory",
    "personal_memory",
    "project_notes",
    "subordinate_backend",
]


@dataclass(frozen=True, slots=True)
class MemoryTrustScopeEntry:
    scope_id: str
    scope_kind: TrustScopeKind
    label: str
    read_allowed: bool
    write_requires_approval: bool
    source_bound: bool
    tenant_boundary_required: bool
    personal_boundary_required: bool
    canonical_truth_allowed: bool
    runtime_mutation_allowed: bool
    scope_ready: bool

    def __post_init__(self) -> None:
        if not self.scope_id:
            raise ValueError("scope_id must be non-empty")
        if not self.label:
            raise ValueError("label must be non-empty")
        if self.source_bound is not True:
            raise ValueError("source_bound must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.scope_kind in {"regulatory_memory", "enterprise_policy_memory", "tenant_memory"}:
            if self.tenant_boundary_required is not True:
                raise ValueError(f"{self.scope_kind} requires tenant boundary")
        if self.scope_kind == "personal_memory" and self.personal_boundary_required is not True:
            raise ValueError("personal_memory requires personal boundary")
        if self.scope_kind == "subordinate_backend" and self.canonical_truth_allowed:
            raise ValueError("subordinate_backend cannot be canonical truth")
        if self.scope_ready is not True:
            raise ValueError("scope_ready must be True")


@dataclass(frozen=True, slots=True)
class MemoryTrustScopeContract:
    contract_id: str
    scopes: Tuple[MemoryTrustScopeEntry, ...]
    canonical_scope_present: bool
    regulatory_scope_present: bool
    enterprise_policy_scope_present: bool
    tenant_scope_present: bool
    personal_scope_present: bool
    subordinate_backend_scope_present: bool
    tenant_personal_separation_ready: bool
    runtime_mutation_allowed: bool
    trust_scope_ready: bool

    def __post_init__(self) -> None:
        if not self.contract_id:
            raise ValueError("contract_id must be non-empty")
        if not self.scopes:
            raise ValueError("scopes must be non-empty")
        scope_ids = {scope.scope_id for scope in self.scopes}
        if len(scope_ids) != len(self.scopes):
            raise ValueError("scope_id values must be unique")
        if not self.canonical_scope_present:
            raise ValueError("canonical_scope_present must be True")
        if not self.regulatory_scope_present:
            raise ValueError("regulatory_scope_present must be True")
        if not self.enterprise_policy_scope_present:
            raise ValueError("enterprise_policy_scope_present must be True")
        if not self.tenant_scope_present:
            raise ValueError("tenant_scope_present must be True")
        if not self.personal_scope_present:
            raise ValueError("personal_scope_present must be True")
        if not self.subordinate_backend_scope_present:
            raise ValueError("subordinate_backend_scope_present must be True")
        if not self.tenant_personal_separation_ready:
            raise ValueError("tenant_personal_separation_ready must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not all(scope.scope_ready for scope in self.scopes):
            raise ValueError("all trust scopes must be ready")
        if self.trust_scope_ready is not True:
            raise ValueError("trust_scope_ready must be True")


def build_memory_trust_scope_contract() -> MemoryTrustScopeContract:
    scopes = (
        MemoryTrustScopeEntry(
            scope_id="trust_scope_canonical_memory",
            scope_kind="canonical_memory",
            label="Canonical source-bound project memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=False,
            personal_boundary_required=False,
            canonical_truth_allowed=True,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_regulatory_memory",
            scope_kind="regulatory_memory",
            label="Country / jurisdiction regulatory memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=True,
            personal_boundary_required=False,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_enterprise_policy_memory",
            scope_kind="enterprise_policy_memory",
            label="Enterprise policy memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=True,
            personal_boundary_required=False,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_tenant_memory",
            scope_kind="tenant_memory",
            label="Tenant-bounded business memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=True,
            personal_boundary_required=False,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_personal_memory",
            scope_kind="personal_memory",
            label="Personal owner context memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=False,
            personal_boundary_required=True,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_project_notes",
            scope_kind="project_notes",
            label="Project notes memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=False,
            personal_boundary_required=False,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
        MemoryTrustScopeEntry(
            scope_id="trust_scope_subordinate_backend",
            scope_kind="subordinate_backend",
            label="Subordinate backend adapter memory",
            read_allowed=True,
            write_requires_approval=True,
            source_bound=True,
            tenant_boundary_required=False,
            personal_boundary_required=False,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            scope_ready=True,
        ),
    )

    kinds = {scope.scope_kind for scope in scopes}

    return MemoryTrustScopeContract(
        contract_id="memory_trust_scope_contract_001",
        scopes=scopes,
        canonical_scope_present="canonical_memory" in kinds,
        regulatory_scope_present="regulatory_memory" in kinds,
        enterprise_policy_scope_present="enterprise_policy_memory" in kinds,
        tenant_scope_present="tenant_memory" in kinds,
        personal_scope_present="personal_memory" in kinds,
        subordinate_backend_scope_present="subordinate_backend" in kinds,
        tenant_personal_separation_ready=True,
        runtime_mutation_allowed=False,
        trust_scope_ready=True,
    )
