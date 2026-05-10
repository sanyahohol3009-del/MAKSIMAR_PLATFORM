from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.regulatory_memory_models import (
    build_regulatory_memory_contract,
)

EnterprisePolicyType = Literal[
    "regulatory_interpretation_policy",
    "compliance_sop_policy",
    "tenant_policy_overlay",
]

PolicyApprovalStatus = Literal["pending_governance_approval"]

_POLICY_RECORD_ID_PATTERN = re.compile(r"^enterprise_policy_record_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class EnterprisePolicyMemoryEntry:
    policy_record_id: str
    regulatory_record_id: str
    tenant_id: str
    business_id: str
    client_id: str
    country_code: str
    jurisdiction_id: str
    policy_type: EnterprisePolicyType
    policy_namespace: str
    approval_status: PolicyApprovalStatus
    source_bound: bool
    versioned: bool
    governance_gate_required: bool
    approval_required: bool
    read_only: bool
    auto_enforcement_allowed: bool
    runtime_policy_binding_allowed: bool
    policy_ready: bool
    description: str

    def __post_init__(self) -> None:
        policy_record_id = _ensure_non_empty_str(self.policy_record_id, "policy_record_id")
        if not _POLICY_RECORD_ID_PATTERN.fullmatch(policy_record_id):
            raise ValueError(f"Invalid policy_record_id: {policy_record_id}")

        for field_name in (
            "regulatory_record_id",
            "tenant_id",
            "business_id",
            "client_id",
            "country_code",
            "jurisdiction_id",
            "policy_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "source_bound",
            "versioned",
            "governance_gate_required",
            "approval_required",
            "read_only",
            "auto_enforcement_allowed",
            "runtime_policy_binding_allowed",
            "policy_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.governance_gate_required:
            raise ValueError("governance_gate_required must be True")
        if not self.approval_required:
            raise ValueError("approval_required must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.auto_enforcement_allowed:
            raise ValueError("auto_enforcement_allowed must be False")
        if self.runtime_policy_binding_allowed:
            raise ValueError("runtime_policy_binding_allowed must be False")
        if not self.policy_ready:
            raise ValueError("policy_ready must be True")


@dataclass(frozen=True, slots=True)
class EnterprisePolicyMemoryContract:
    total_policies: int
    ready_policies: int
    source_bound_policies: int
    versioned_policies: int
    governance_gate_required_policies: int
    approval_required_policies: int
    read_only_policies: int
    auto_enforcement_allowed_policies: int
    runtime_policy_binding_allowed_policies: int
    pending_approval_policies: int
    entries: tuple[EnterprisePolicyMemoryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_policies != len(self.entries):
            raise ValueError("total_policies must match entries length")
        if self.total_policies <= 0:
            raise ValueError("total_policies must be >= 1")

        expected = {
            "ready_policies": sum(1 for entry in self.entries if entry.policy_ready),
            "source_bound_policies": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_policies": sum(1 for entry in self.entries if entry.versioned),
            "governance_gate_required_policies": sum(
                1 for entry in self.entries if entry.governance_gate_required
            ),
            "approval_required_policies": sum(1 for entry in self.entries if entry.approval_required),
            "read_only_policies": sum(1 for entry in self.entries if entry.read_only),
            "auto_enforcement_allowed_policies": sum(
                1 for entry in self.entries if entry.auto_enforcement_allowed
            ),
            "runtime_policy_binding_allowed_policies": sum(
                1 for entry in self.entries if entry.runtime_policy_binding_allowed
            ),
            "pending_approval_policies": sum(
                1 for entry in self.entries if entry.approval_status == "pending_governance_approval"
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_policies != self.total_policies:
            raise ValueError("all enterprise policy records must be ready")
        if self.source_bound_policies != self.total_policies:
            raise ValueError("all enterprise policy records must be source-bound")
        if self.versioned_policies != self.total_policies:
            raise ValueError("all enterprise policy records must be versioned")
        if self.governance_gate_required_policies != self.total_policies:
            raise ValueError("all enterprise policy records must require governance gate")
        if self.approval_required_policies != self.total_policies:
            raise ValueError("all enterprise policy records must require approval")
        if self.read_only_policies != self.total_policies:
            raise ValueError("all enterprise policy records must be read-only")
        if self.auto_enforcement_allowed_policies != 0:
            raise ValueError("auto enforcement must remain blocked")
        if self.runtime_policy_binding_allowed_policies != 0:
            raise ValueError("runtime policy binding must remain blocked")
        if self.pending_approval_policies != self.total_policies:
            raise ValueError("all enterprise policies must be pending governance approval")


def build_enterprise_policy_memory_contract() -> EnterprisePolicyMemoryContract:
    regulatory = build_regulatory_memory_contract()

    entries = tuple(
        EnterprisePolicyMemoryEntry(
            policy_record_id=f"enterprise_policy_record_{entry.country_code.lower()}_{entry.tenant_id.removeprefix('tenant_')}_001",
            regulatory_record_id=entry.regulatory_record_id,
            tenant_id=entry.tenant_id,
            business_id=entry.business_id,
            client_id=entry.client_id,
            country_code=entry.country_code,
            jurisdiction_id=entry.jurisdiction_id,
            policy_type="compliance_sop_policy" if entry.country_code == "EU" else "regulatory_interpretation_policy",
            policy_namespace=f"enterprise_policy::{entry.business_id}::{entry.country_code}",
            approval_status="pending_governance_approval",
            source_bound=True,
            versioned=True,
            governance_gate_required=True,
            approval_required=True,
            read_only=True,
            auto_enforcement_allowed=False,
            runtime_policy_binding_allowed=False,
            policy_ready=True,
            description=f"Read-only enterprise policy memory placeholder for {entry.country_code}.",
        )
        for entry in regulatory.entries
    )

    return EnterprisePolicyMemoryContract(
        total_policies=len(entries),
        ready_policies=sum(1 for entry in entries if entry.policy_ready),
        source_bound_policies=sum(1 for entry in entries if entry.source_bound),
        versioned_policies=sum(1 for entry in entries if entry.versioned),
        governance_gate_required_policies=sum(
            1 for entry in entries if entry.governance_gate_required
        ),
        approval_required_policies=sum(1 for entry in entries if entry.approval_required),
        read_only_policies=sum(1 for entry in entries if entry.read_only),
        auto_enforcement_allowed_policies=sum(
            1 for entry in entries if entry.auto_enforcement_allowed
        ),
        runtime_policy_binding_allowed_policies=sum(
            1 for entry in entries if entry.runtime_policy_binding_allowed
        ),
        pending_approval_policies=sum(
            1 for entry in entries if entry.approval_status == "pending_governance_approval"
        ),
        entries=entries,
    )
