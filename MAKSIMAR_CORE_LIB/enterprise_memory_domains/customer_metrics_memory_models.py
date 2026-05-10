from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.tenant_memory_models import (
    build_tenant_memory_scope_contract,
)

_METRICS_RECORD_ID_PATTERN = re.compile(r"^customer_metrics_record_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class CustomerMetricsMemoryEntry:
    metrics_record_id: str
    tenant_id: str
    business_id: str
    client_id: str
    country_code: str
    metrics_namespace: str
    metrics_categories: tuple[str, ...]
    tenant_isolated: bool
    client_isolated: bool
    country_bound: bool
    read_only: bool
    pii_exposure_allowed: bool
    cross_tenant_aggregation_allowed: bool
    runtime_policy_binding_allowed: bool
    metrics_ready: bool
    description: str

    def __post_init__(self) -> None:
        metrics_record_id = _ensure_non_empty_str(self.metrics_record_id, "metrics_record_id")
        if not _METRICS_RECORD_ID_PATTERN.fullmatch(metrics_record_id):
            raise ValueError(f"Invalid metrics_record_id: {metrics_record_id}")

        for field_name in (
            "tenant_id",
            "business_id",
            "client_id",
            "country_code",
            "metrics_namespace",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        if not isinstance(self.metrics_categories, tuple) or not self.metrics_categories:
            raise ValueError("metrics_categories must be a non-empty tuple")
        if len(set(self.metrics_categories)) != len(self.metrics_categories):
            raise ValueError("metrics_categories must contain unique values")
        for category in self.metrics_categories:
            _ensure_non_empty_str(category, "metrics_category")

        for field_name in (
            "tenant_isolated",
            "client_isolated",
            "country_bound",
            "read_only",
            "pii_exposure_allowed",
            "cross_tenant_aggregation_allowed",
            "runtime_policy_binding_allowed",
            "metrics_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.tenant_isolated:
            raise ValueError("tenant_isolated must be True")
        if not self.client_isolated:
            raise ValueError("client_isolated must be True")
        if not self.country_bound:
            raise ValueError("country_bound must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.pii_exposure_allowed:
            raise ValueError("pii_exposure_allowed must be False")
        if self.cross_tenant_aggregation_allowed:
            raise ValueError("cross_tenant_aggregation_allowed must be False")
        if self.runtime_policy_binding_allowed:
            raise ValueError("runtime_policy_binding_allowed must be False")
        if not self.metrics_ready:
            raise ValueError("metrics_ready must be True")


@dataclass(frozen=True, slots=True)
class CustomerMetricsMemoryContract:
    total_metrics: int
    ready_metrics: int
    tenant_isolated_metrics: int
    client_isolated_metrics: int
    country_bound_metrics: int
    read_only_metrics: int
    pii_exposure_allowed_metrics: int
    cross_tenant_aggregation_allowed_metrics: int
    runtime_policy_binding_allowed_metrics: int
    entries: tuple[CustomerMetricsMemoryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_metrics != len(self.entries):
            raise ValueError("total_metrics must match entries length")
        if self.total_metrics <= 0:
            raise ValueError("total_metrics must be >= 1")

        expected = {
            "ready_metrics": sum(1 for entry in self.entries if entry.metrics_ready),
            "tenant_isolated_metrics": sum(1 for entry in self.entries if entry.tenant_isolated),
            "client_isolated_metrics": sum(1 for entry in self.entries if entry.client_isolated),
            "country_bound_metrics": sum(1 for entry in self.entries if entry.country_bound),
            "read_only_metrics": sum(1 for entry in self.entries if entry.read_only),
            "pii_exposure_allowed_metrics": sum(
                1 for entry in self.entries if entry.pii_exposure_allowed
            ),
            "cross_tenant_aggregation_allowed_metrics": sum(
                1 for entry in self.entries if entry.cross_tenant_aggregation_allowed
            ),
            "runtime_policy_binding_allowed_metrics": sum(
                1 for entry in self.entries if entry.runtime_policy_binding_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_metrics != self.total_metrics:
            raise ValueError("all customer metrics records must be ready")
        if self.tenant_isolated_metrics != self.total_metrics:
            raise ValueError("all customer metrics records must be tenant-isolated")
        if self.client_isolated_metrics != self.total_metrics:
            raise ValueError("all customer metrics records must be client-isolated")
        if self.country_bound_metrics != self.total_metrics:
            raise ValueError("all customer metrics records must be country-bound")
        if self.read_only_metrics != self.total_metrics:
            raise ValueError("all customer metrics records must be read-only")
        if self.pii_exposure_allowed_metrics != 0:
            raise ValueError("PII exposure must remain blocked")
        if self.cross_tenant_aggregation_allowed_metrics != 0:
            raise ValueError("cross-tenant aggregation must remain blocked")
        if self.runtime_policy_binding_allowed_metrics != 0:
            raise ValueError("runtime policy binding must remain blocked")


def build_customer_metrics_memory_contract() -> CustomerMetricsMemoryContract:
    tenants = build_tenant_memory_scope_contract()

    entries = tuple(
        CustomerMetricsMemoryEntry(
            metrics_record_id=f"customer_metrics_record_{tenant.country_code.lower()}_{tenant.tenant_id.removeprefix('tenant_')}_001",
            tenant_id=tenant.tenant_id,
            business_id=tenant.business_id,
            client_id=tenant.client_id,
            country_code=tenant.country_code,
            metrics_namespace=f"customer_metrics::{tenant.client_id}::{tenant.country_code}",
            metrics_categories=("usage_summary", "readiness_status", "support_context"),
            tenant_isolated=True,
            client_isolated=True,
            country_bound=True,
            read_only=True,
            pii_exposure_allowed=False,
            cross_tenant_aggregation_allowed=False,
            runtime_policy_binding_allowed=False,
            metrics_ready=True,
            description=f"Read-only customer metrics memory placeholder for {tenant.client_id}.",
        )
        for tenant in tenants.entries
    )

    return CustomerMetricsMemoryContract(
        total_metrics=len(entries),
        ready_metrics=sum(1 for entry in entries if entry.metrics_ready),
        tenant_isolated_metrics=sum(1 for entry in entries if entry.tenant_isolated),
        client_isolated_metrics=sum(1 for entry in entries if entry.client_isolated),
        country_bound_metrics=sum(1 for entry in entries if entry.country_bound),
        read_only_metrics=sum(1 for entry in entries if entry.read_only),
        pii_exposure_allowed_metrics=sum(1 for entry in entries if entry.pii_exposure_allowed),
        cross_tenant_aggregation_allowed_metrics=sum(
            1 for entry in entries if entry.cross_tenant_aggregation_allowed
        ),
        runtime_policy_binding_allowed_metrics=sum(
            1 for entry in entries if entry.runtime_policy_binding_allowed
        ),
        entries=entries,
    )
