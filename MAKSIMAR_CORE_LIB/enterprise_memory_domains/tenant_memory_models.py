from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


EnterpriseMemoryDomain = Literal[
    "REGULATORY_MEMORY",
    "COMPLIANCE_MEMORY",
    "ENTERPRISE_POLICY_MEMORY",
    "CUSTOMER_METRICS_MEMORY",
]

_TENANT_ID_PATTERN = re.compile(r"^tenant_[a-z][a-z0-9_]*$")
_BUSINESS_ID_PATTERN = re.compile(r"^business_[a-z][a-z0-9_]*$")
_CLIENT_ID_PATTERN = re.compile(r"^client_[a-z][a-z0-9_]*$")
_JURISDICTION_ID_PATTERN = re.compile(r"^jurisdiction_[a-z][a-z0-9_]*$")
_COUNTRY_CODE_PATTERN = re.compile(r"^[A-Z]{2}$")


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
class TenantMemoryScopeEntry:
    tenant_id: str
    business_id: str
    client_id: str
    country_code: str
    jurisdiction_id: str
    memory_domain: EnterpriseMemoryDomain
    tenant_isolated: bool
    business_isolated: bool
    client_isolated: bool
    country_bound: bool
    read_only: bool
    approved_for_runtime_policy: bool
    scope_ready: bool
    description: str

    def __post_init__(self) -> None:
        tenant_id = _ensure_non_empty_str(self.tenant_id, "tenant_id")
        business_id = _ensure_non_empty_str(self.business_id, "business_id")
        client_id = _ensure_non_empty_str(self.client_id, "client_id")
        country_code = _ensure_non_empty_str(self.country_code, "country_code")
        jurisdiction_id = _ensure_non_empty_str(self.jurisdiction_id, "jurisdiction_id")
        _ensure_non_empty_str(self.description, "description")

        if not _TENANT_ID_PATTERN.fullmatch(tenant_id):
            raise ValueError(f"Invalid tenant_id: {tenant_id}")
        if not _BUSINESS_ID_PATTERN.fullmatch(business_id):
            raise ValueError(f"Invalid business_id: {business_id}")
        if not _CLIENT_ID_PATTERN.fullmatch(client_id):
            raise ValueError(f"Invalid client_id: {client_id}")
        if not _COUNTRY_CODE_PATTERN.fullmatch(country_code):
            raise ValueError(f"Invalid country_code: {country_code}")
        if not _JURISDICTION_ID_PATTERN.fullmatch(jurisdiction_id):
            raise ValueError(f"Invalid jurisdiction_id: {jurisdiction_id}")

        for field_name in (
            "tenant_isolated",
            "business_isolated",
            "client_isolated",
            "country_bound",
            "read_only",
            "approved_for_runtime_policy",
            "scope_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.tenant_isolated:
            raise ValueError("tenant_isolated must be True")
        if not self.business_isolated:
            raise ValueError("business_isolated must be True")
        if not self.client_isolated:
            raise ValueError("client_isolated must be True")
        if not self.country_bound:
            raise ValueError("country_bound must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.approved_for_runtime_policy:
            raise ValueError("approved_for_runtime_policy must be False in Batch 1")
        if not self.scope_ready:
            raise ValueError("scope_ready must be True")


@dataclass(frozen=True, slots=True)
class TenantMemoryScopeContract:
    total_scopes: int
    ready_scopes: int
    tenant_isolated_scopes: int
    business_isolated_scopes: int
    client_isolated_scopes: int
    country_bound_scopes: int
    read_only_scopes: int
    runtime_policy_approved_scopes: int
    entries: tuple[TenantMemoryScopeEntry, ...]

    def __post_init__(self) -> None:
        if self.total_scopes != len(self.entries):
            raise ValueError("total_scopes must match entries length")
        if self.total_scopes <= 0:
            raise ValueError("total_scopes must be >= 1")

        expected = {
            "ready_scopes": sum(1 for entry in self.entries if entry.scope_ready),
            "tenant_isolated_scopes": sum(1 for entry in self.entries if entry.tenant_isolated),
            "business_isolated_scopes": sum(1 for entry in self.entries if entry.business_isolated),
            "client_isolated_scopes": sum(1 for entry in self.entries if entry.client_isolated),
            "country_bound_scopes": sum(1 for entry in self.entries if entry.country_bound),
            "read_only_scopes": sum(1 for entry in self.entries if entry.read_only),
            "runtime_policy_approved_scopes": sum(
                1 for entry in self.entries if entry.approved_for_runtime_policy
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be ready")
        if self.tenant_isolated_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be tenant-isolated")
        if self.business_isolated_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be business-isolated")
        if self.client_isolated_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be client-isolated")
        if self.country_bound_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be country-bound")
        if self.read_only_scopes != self.total_scopes:
            raise ValueError("all tenant memory scopes must be read-only")
        if self.runtime_policy_approved_scopes != 0:
            raise ValueError("runtime policy approval must remain blocked in Batch 1")


def build_tenant_memory_scope_contract() -> TenantMemoryScopeContract:
    entries = (
        TenantMemoryScopeEntry(
            tenant_id="tenant_demo_de",
            business_id="business_demo_compliance",
            client_id="client_demo_germany",
            country_code="DE",
            jurisdiction_id="jurisdiction_de_federal",
            memory_domain="REGULATORY_MEMORY",
            tenant_isolated=True,
            business_isolated=True,
            client_isolated=True,
            country_bound=True,
            read_only=True,
            approved_for_runtime_policy=False,
            scope_ready=True,
            description="Read-only German regulatory tenant memory scope.",
        ),
        TenantMemoryScopeEntry(
            tenant_id="tenant_demo_ua",
            business_id="business_demo_compliance",
            client_id="client_demo_ukraine",
            country_code="UA",
            jurisdiction_id="jurisdiction_ua_national",
            memory_domain="REGULATORY_MEMORY",
            tenant_isolated=True,
            business_isolated=True,
            client_isolated=True,
            country_bound=True,
            read_only=True,
            approved_for_runtime_policy=False,
            scope_ready=True,
            description="Read-only Ukrainian regulatory tenant memory scope.",
        ),
        TenantMemoryScopeEntry(
            tenant_id="tenant_demo_eu",
            business_id="business_demo_saas",
            client_id="client_demo_eu",
            country_code="EU",
            jurisdiction_id="jurisdiction_eu_union",
            memory_domain="COMPLIANCE_MEMORY",
            tenant_isolated=True,
            business_isolated=True,
            client_isolated=True,
            country_bound=True,
            read_only=True,
            approved_for_runtime_policy=False,
            scope_ready=True,
            description="Read-only EU compliance tenant memory scope.",
        ),
    )

    return TenantMemoryScopeContract(
        total_scopes=len(entries),
        ready_scopes=sum(1 for entry in entries if entry.scope_ready),
        tenant_isolated_scopes=sum(1 for entry in entries if entry.tenant_isolated),
        business_isolated_scopes=sum(1 for entry in entries if entry.business_isolated),
        client_isolated_scopes=sum(1 for entry in entries if entry.client_isolated),
        country_bound_scopes=sum(1 for entry in entries if entry.country_bound),
        read_only_scopes=sum(1 for entry in entries if entry.read_only),
        runtime_policy_approved_scopes=sum(
            1 for entry in entries if entry.approved_for_runtime_policy
        ),
        entries=entries,
    )
