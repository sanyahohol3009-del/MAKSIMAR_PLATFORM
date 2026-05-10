from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.legal_jurisdiction_models import (
    build_legal_jurisdiction_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.tenant_memory_models import (
    build_tenant_memory_scope_contract,
)

SourceStatus = Literal["placeholder_source_bound", "pending_source_review"]
ApprovalStatus = Literal["pending_governance_approval"]

_RECORD_ID_PATTERN = re.compile(r"^regulatory_record_[a-z][a-z0-9_]*_[0-9]{3}$")
_DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


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
class RegulatoryMemoryEntry:
    regulatory_record_id: str
    tenant_id: str
    business_id: str
    client_id: str
    country_code: str
    jurisdiction_id: str
    legal_domain: str
    applicability_scope: str
    source_ref: str
    effective_date: str
    record_version: str
    source_status: SourceStatus
    approval_status: ApprovalStatus
    source_bound: bool
    versioned: bool
    conflict_marker_allowed: bool
    read_only: bool
    runtime_policy_binding_allowed: bool
    regulatory_ready: bool
    description: str

    def __post_init__(self) -> None:
        record_id = _ensure_non_empty_str(self.regulatory_record_id, "regulatory_record_id")
        if not _RECORD_ID_PATTERN.fullmatch(record_id):
            raise ValueError(f"Invalid regulatory_record_id: {record_id}")

        for field_name in (
            "tenant_id",
            "business_id",
            "client_id",
            "country_code",
            "jurisdiction_id",
            "legal_domain",
            "applicability_scope",
            "source_ref",
            "effective_date",
            "record_version",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        if not _DATE_PATTERN.fullmatch(self.effective_date):
            raise ValueError(f"Invalid effective_date: {self.effective_date}")

        for field_name in (
            "source_bound",
            "versioned",
            "conflict_marker_allowed",
            "read_only",
            "runtime_policy_binding_allowed",
            "regulatory_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.versioned:
            raise ValueError("versioned must be True")
        if not self.conflict_marker_allowed:
            raise ValueError("conflict_marker_allowed must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.runtime_policy_binding_allowed:
            raise ValueError("runtime_policy_binding_allowed must be False in Batch 1")
        if not self.regulatory_ready:
            raise ValueError("regulatory_ready must be True")


@dataclass(frozen=True, slots=True)
class RegulatoryMemoryContract:
    total_records: int
    ready_records: int
    source_bound_records: int
    versioned_records: int
    conflict_marker_allowed_records: int
    read_only_records: int
    runtime_policy_binding_allowed_records: int
    pending_approval_records: int
    country_bound_records: int
    entries: tuple[RegulatoryMemoryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_records != len(self.entries):
            raise ValueError("total_records must match entries length")
        if self.total_records <= 0:
            raise ValueError("total_records must be >= 1")

        expected = {
            "ready_records": sum(1 for entry in self.entries if entry.regulatory_ready),
            "source_bound_records": sum(1 for entry in self.entries if entry.source_bound),
            "versioned_records": sum(1 for entry in self.entries if entry.versioned),
            "conflict_marker_allowed_records": sum(
                1 for entry in self.entries if entry.conflict_marker_allowed
            ),
            "read_only_records": sum(1 for entry in self.entries if entry.read_only),
            "runtime_policy_binding_allowed_records": sum(
                1 for entry in self.entries if entry.runtime_policy_binding_allowed
            ),
            "pending_approval_records": sum(
                1 for entry in self.entries if entry.approval_status == "pending_governance_approval"
            ),
            "country_bound_records": len({entry.country_code for entry in self.entries}),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_records != self.total_records:
            raise ValueError("all regulatory records must be ready")
        if self.source_bound_records != self.total_records:
            raise ValueError("all regulatory records must be source-bound")
        if self.versioned_records != self.total_records:
            raise ValueError("all regulatory records must be versioned")
        if self.conflict_marker_allowed_records != self.total_records:
            raise ValueError("all regulatory records must allow conflict markers")
        if self.read_only_records != self.total_records:
            raise ValueError("all regulatory records must be read-only")
        if self.runtime_policy_binding_allowed_records != 0:
            raise ValueError("runtime policy binding must remain blocked in Batch 1")
        if self.pending_approval_records != self.total_records:
            raise ValueError("all regulatory records must be pending governance approval")
        if self.country_bound_records < 3:
            raise ValueError("regulatory memory must cover separate country/jurisdiction scopes")


def build_regulatory_memory_contract() -> RegulatoryMemoryContract:
    tenants = build_tenant_memory_scope_contract()
    jurisdictions = build_legal_jurisdiction_contract()

    jurisdiction_ids = {entry.jurisdiction_id for entry in jurisdictions.entries}

    entries = tuple(
        RegulatoryMemoryEntry(
            regulatory_record_id=f"regulatory_record_{tenant.country_code.lower()}_{tenant.tenant_id.removeprefix('tenant_')}_001",
            tenant_id=tenant.tenant_id,
            business_id=tenant.business_id,
            client_id=tenant.client_id,
            country_code=tenant.country_code,
            jurisdiction_id=tenant.jurisdiction_id,
            legal_domain="business_compliance",
            applicability_scope=f"{tenant.country_code}:{tenant.memory_domain}",
            source_ref=f"source_ref_{tenant.country_code.lower()}_regulatory_placeholder_v1",
            effective_date="2026-01-01",
            record_version="v1",
            source_status="placeholder_source_bound",
            approval_status="pending_governance_approval",
            source_bound=True,
            versioned=True,
            conflict_marker_allowed=True,
            read_only=True,
            runtime_policy_binding_allowed=False,
            regulatory_ready=tenant.jurisdiction_id in jurisdiction_ids,
            description=f"Read-only regulatory memory placeholder for {tenant.country_code}.",
        )
        for tenant in tenants.entries
    )

    return RegulatoryMemoryContract(
        total_records=len(entries),
        ready_records=sum(1 for entry in entries if entry.regulatory_ready),
        source_bound_records=sum(1 for entry in entries if entry.source_bound),
        versioned_records=sum(1 for entry in entries if entry.versioned),
        conflict_marker_allowed_records=sum(
            1 for entry in entries if entry.conflict_marker_allowed
        ),
        read_only_records=sum(1 for entry in entries if entry.read_only),
        runtime_policy_binding_allowed_records=sum(
            1 for entry in entries if entry.runtime_policy_binding_allowed
        ),
        pending_approval_records=sum(
            1 for entry in entries if entry.approval_status == "pending_governance_approval"
        ),
        country_bound_records=len({entry.country_code for entry in entries}),
        entries=entries,
    )
