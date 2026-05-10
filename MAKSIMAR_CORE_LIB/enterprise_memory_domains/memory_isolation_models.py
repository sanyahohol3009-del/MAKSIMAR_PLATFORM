from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.regulatory_memory_models import (
    build_regulatory_memory_contract,
)

_ISOLATION_ID_PATTERN = re.compile(r"^memory_isolation_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class MemoryIsolationEntry:
    isolation_id: str
    tenant_id: str
    business_id: str
    client_id: str
    country_code: str
    jurisdiction_id: str
    regulatory_record_id: str
    isolated_storage_namespace: str
    evidence_namespace: str
    policy_namespace: str
    dashboard_namespace: str
    cross_tenant_merge_allowed: bool
    cross_business_merge_allowed: bool
    cross_country_merge_allowed: bool
    runtime_policy_binding_allowed: bool
    read_only: bool
    isolation_ready: bool
    description: str

    def __post_init__(self) -> None:
        isolation_id = _ensure_non_empty_str(self.isolation_id, "isolation_id")
        if not _ISOLATION_ID_PATTERN.fullmatch(isolation_id):
            raise ValueError(f"Invalid isolation_id: {isolation_id}")

        for field_name in (
            "tenant_id",
            "business_id",
            "client_id",
            "country_code",
            "jurisdiction_id",
            "regulatory_record_id",
            "isolated_storage_namespace",
            "evidence_namespace",
            "policy_namespace",
            "dashboard_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "cross_tenant_merge_allowed",
            "cross_business_merge_allowed",
            "cross_country_merge_allowed",
            "runtime_policy_binding_allowed",
            "read_only",
            "isolation_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if self.cross_tenant_merge_allowed:
            raise ValueError("cross_tenant_merge_allowed must be False")
        if self.cross_business_merge_allowed:
            raise ValueError("cross_business_merge_allowed must be False")
        if self.cross_country_merge_allowed:
            raise ValueError("cross_country_merge_allowed must be False")
        if self.runtime_policy_binding_allowed:
            raise ValueError("runtime_policy_binding_allowed must be False in Batch 1")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.isolation_ready:
            raise ValueError("isolation_ready must be True")


@dataclass(frozen=True, slots=True)
class MemoryIsolationContract:
    total_isolations: int
    ready_isolations: int
    read_only_isolations: int
    cross_tenant_merge_allowed_isolations: int
    cross_business_merge_allowed_isolations: int
    cross_country_merge_allowed_isolations: int
    runtime_policy_binding_allowed_isolations: int
    entries: tuple[MemoryIsolationEntry, ...]

    def __post_init__(self) -> None:
        if self.total_isolations != len(self.entries):
            raise ValueError("total_isolations must match entries length")
        if self.total_isolations <= 0:
            raise ValueError("total_isolations must be >= 1")

        expected = {
            "ready_isolations": sum(1 for entry in self.entries if entry.isolation_ready),
            "read_only_isolations": sum(1 for entry in self.entries if entry.read_only),
            "cross_tenant_merge_allowed_isolations": sum(
                1 for entry in self.entries if entry.cross_tenant_merge_allowed
            ),
            "cross_business_merge_allowed_isolations": sum(
                1 for entry in self.entries if entry.cross_business_merge_allowed
            ),
            "cross_country_merge_allowed_isolations": sum(
                1 for entry in self.entries if entry.cross_country_merge_allowed
            ),
            "runtime_policy_binding_allowed_isolations": sum(
                1 for entry in self.entries if entry.runtime_policy_binding_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_isolations != self.total_isolations:
            raise ValueError("all memory isolations must be ready")
        if self.read_only_isolations != self.total_isolations:
            raise ValueError("all memory isolations must be read-only")
        if self.cross_tenant_merge_allowed_isolations != 0:
            raise ValueError("cross-tenant merge must remain blocked")
        if self.cross_business_merge_allowed_isolations != 0:
            raise ValueError("cross-business merge must remain blocked")
        if self.cross_country_merge_allowed_isolations != 0:
            raise ValueError("cross-country merge must remain blocked")
        if self.runtime_policy_binding_allowed_isolations != 0:
            raise ValueError("runtime policy binding must remain blocked")


def build_memory_isolation_contract() -> MemoryIsolationContract:
    regulatory = build_regulatory_memory_contract()

    entries = tuple(
        MemoryIsolationEntry(
            isolation_id=f"memory_isolation_{entry.country_code.lower()}_{entry.tenant_id.removeprefix('tenant_')}_001",
            tenant_id=entry.tenant_id,
            business_id=entry.business_id,
            client_id=entry.client_id,
            country_code=entry.country_code,
            jurisdiction_id=entry.jurisdiction_id,
            regulatory_record_id=entry.regulatory_record_id,
            isolated_storage_namespace=f"storage::{entry.tenant_id}::{entry.country_code}",
            evidence_namespace=f"evidence::{entry.tenant_id}::{entry.jurisdiction_id}",
            policy_namespace=f"policy::{entry.business_id}::{entry.country_code}",
            dashboard_namespace=f"dashboard::{entry.client_id}::{entry.country_code}",
            cross_tenant_merge_allowed=False,
            cross_business_merge_allowed=False,
            cross_country_merge_allowed=False,
            runtime_policy_binding_allowed=False,
            read_only=True,
            isolation_ready=True,
            description=f"Read-only memory isolation boundary for {entry.tenant_id}.",
        )
        for entry in regulatory.entries
    )

    return MemoryIsolationContract(
        total_isolations=len(entries),
        ready_isolations=sum(1 for entry in entries if entry.isolation_ready),
        read_only_isolations=sum(1 for entry in entries if entry.read_only),
        cross_tenant_merge_allowed_isolations=sum(
            1 for entry in entries if entry.cross_tenant_merge_allowed
        ),
        cross_business_merge_allowed_isolations=sum(
            1 for entry in entries if entry.cross_business_merge_allowed
        ),
        cross_country_merge_allowed_isolations=sum(
            1 for entry in entries if entry.cross_country_merge_allowed
        ),
        runtime_policy_binding_allowed_isolations=sum(
            1 for entry in entries if entry.runtime_policy_binding_allowed
        ),
        entries=entries,
    )
