from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    CapabilityRegistryLoadResult,
    load_canonical_capability_registry,
)


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class CapabilityRegistrySummaryBucket:
    name: str
    count: int

    def __post_init__(self) -> None:
        name = _ensure_non_empty_str(self.name, "name")
        count = _ensure_non_negative_int(self.count, "count")
        if count <= 0:
            raise ValueError("summary bucket count must be >= 1")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "count", count)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "count": self.count,
        }


@dataclass(frozen=True, slots=True)
class CapabilityRegistrySummary:
    """Read-only capability registry summary prepared for dashboard/container views."""

    schema_version: str
    registry_id: str
    source_path: str
    total_capabilities: int
    family_buckets: tuple[CapabilityRegistrySummaryBucket, ...]
    integration_policy_buckets: tuple[CapabilityRegistrySummaryBucket, ...]
    container_profile_buckets: tuple[CapabilityRegistrySummaryBucket, ...]
    runtime_enablement_buckets: tuple[CapabilityRegistrySummaryBucket, ...]
    maksimar_owned_capabilities: int
    external_adapter_candidates: int
    disable_safe_capabilities: int
    dashboard_read_only_capabilities: int
    container_profile_declared_capabilities: int
    runtime_enablement_declared_capabilities: int
    containerization_ready_capabilities: int
    batch_containerization_readiness_required: bool
    read_only_load: bool
    active_deployment_created: bool
    ports_opened: bool
    containers_started: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    containerization_ready_for_reference: bool

    def __post_init__(self) -> None:
        schema_version = _ensure_non_empty_str(self.schema_version, "schema_version")
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")
        source_path = _ensure_non_empty_str(self.source_path, "source_path")
        total_capabilities = _ensure_non_negative_int(
            self.total_capabilities,
            "total_capabilities",
        )

        if schema_version != "canonical_capability_registry.v1":
            raise ValueError("schema_version must be canonical_capability_registry.v1")
        if registry_id != "phase_1_canonical_capability_registry":
            raise ValueError("registry_id must be phase_1_canonical_capability_registry")
        if total_capabilities <= 0:
            raise ValueError("total_capabilities must be >= 1")

        for field_name in (
            "family_buckets",
            "integration_policy_buckets",
            "container_profile_buckets",
            "runtime_enablement_buckets",
        ):
            buckets = getattr(self, field_name)
            if not isinstance(buckets, tuple):
                raise TypeError(f"{field_name} must be a tuple")
            if not buckets:
                raise ValueError(f"{field_name} must not be empty")
            for bucket in buckets:
                if not isinstance(bucket, CapabilityRegistrySummaryBucket):
                    raise TypeError(f"{field_name} must contain CapabilityRegistrySummaryBucket")

        counted_profiles = sum(bucket.count for bucket in self.container_profile_buckets)
        if counted_profiles != total_capabilities:
            raise ValueError("container_profile_buckets must cover all capabilities")

        for field_name in (
            "maksimar_owned_capabilities",
            "external_adapter_candidates",
            "disable_safe_capabilities",
            "dashboard_read_only_capabilities",
            "container_profile_declared_capabilities",
            "runtime_enablement_declared_capabilities",
            "containerization_ready_capabilities",
        ):
            value = _ensure_non_negative_int(getattr(self, field_name), field_name)
            if value > total_capabilities:
                raise ValueError(f"{field_name} must not exceed total_capabilities")

        if self.disable_safe_capabilities != total_capabilities:
            raise ValueError("all capabilities must be disable-safe")
        if self.dashboard_read_only_capabilities != total_capabilities:
            raise ValueError("all capabilities must be dashboard read-only")
        if self.container_profile_declared_capabilities != total_capabilities:
            raise ValueError("all capabilities must declare container_profile")
        if self.runtime_enablement_declared_capabilities != total_capabilities:
            raise ValueError("all capabilities must declare runtime_enablement")
        if self.containerization_ready_capabilities != total_capabilities:
            raise ValueError("all capabilities must be containerization-ready")
        if not _ensure_bool(
            self.batch_containerization_readiness_required,
            "batch_containerization_readiness_required",
        ):
            raise ValueError("batch_containerization_readiness_required must remain true")

        if not _ensure_bool(self.read_only_load, "read_only_load"):
            raise ValueError("read_only_load must remain true")
        if _ensure_bool(self.active_deployment_created, "active_deployment_created"):
            raise ValueError("active_deployment_created must remain false")
        if _ensure_bool(self.ports_opened, "ports_opened"):
            raise ValueError("ports_opened must remain false")
        if _ensure_bool(self.containers_started, "containers_started"):
            raise ValueError("containers_started must remain false")
        if _ensure_bool(self.runtime_mutation_allowed, "runtime_mutation_allowed"):
            raise ValueError("runtime_mutation_allowed must remain false")
        if _ensure_bool(self.direct_core_import_allowed, "direct_core_import_allowed"):
            raise ValueError("direct_core_import_allowed must remain false")
        if _ensure_bool(
            self.source_of_truth_override_allowed,
            "source_of_truth_override_allowed",
        ):
            raise ValueError("source_of_truth_override_allowed must remain false")
        if not _ensure_bool(
            self.containerization_ready_for_reference,
            "containerization_ready_for_reference",
        ):
            raise ValueError("containerization_ready_for_reference must remain true")

        object.__setattr__(self, "schema_version", schema_version)
        object.__setattr__(self, "registry_id", registry_id)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "total_capabilities", total_capabilities)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_id": self.registry_id,
            "source_path": self.source_path,
            "total_capabilities": self.total_capabilities,
            "family_buckets": [bucket.to_dict() for bucket in self.family_buckets],
            "integration_policy_buckets": [
                bucket.to_dict() for bucket in self.integration_policy_buckets
            ],
            "container_profile_buckets": [
                bucket.to_dict() for bucket in self.container_profile_buckets
            ],
            "runtime_enablement_buckets": [
                bucket.to_dict() for bucket in self.runtime_enablement_buckets
            ],
            "maksimar_owned_capabilities": self.maksimar_owned_capabilities,
            "external_adapter_candidates": self.external_adapter_candidates,
            "disable_safe_capabilities": self.disable_safe_capabilities,
            "dashboard_read_only_capabilities": self.dashboard_read_only_capabilities,
            "container_profile_declared_capabilities": self.container_profile_declared_capabilities,
            "runtime_enablement_declared_capabilities": self.runtime_enablement_declared_capabilities,
            "containerization_ready_capabilities": self.containerization_ready_capabilities,
            "batch_containerization_readiness_required": self.batch_containerization_readiness_required,
            "read_only_load": self.read_only_load,
            "active_deployment_created": self.active_deployment_created,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "containerization_ready_for_reference": self.containerization_ready_for_reference,
        }


def _build_buckets(values: tuple[str, ...]) -> tuple[CapabilityRegistrySummaryBucket, ...]:
    counter = Counter(values)
    return tuple(
        CapabilityRegistrySummaryBucket(name=name, count=count)
        for name, count in sorted(counter.items())
    )


def build_capability_registry_summary(
    load_result: CapabilityRegistryLoadResult | None = None,
) -> CapabilityRegistrySummary:
    result = load_result or load_canonical_capability_registry()
    entries = result.contract.entries

    total_capabilities = len(entries)

    return CapabilityRegistrySummary(
        schema_version=result.schema_version,
        registry_id=result.registry_id,
        source_path=result.source_path,
        total_capabilities=total_capabilities,
        family_buckets=_build_buckets(tuple(entry.family for entry in entries)),
        integration_policy_buckets=_build_buckets(
            tuple(entry.integration_policy for entry in entries)
        ),
        container_profile_buckets=_build_buckets(
            tuple(entry.container_profile for entry in entries)
        ),
        runtime_enablement_buckets=_build_buckets(
            tuple(entry.runtime_enablement for entry in entries)
        ),
        maksimar_owned_capabilities=sum(
            1 for entry in entries if entry.integration_policy == "maksimar_owned"
        ),
        external_adapter_candidates=sum(
            1 for entry in entries if entry.integration_policy == "adapter_only"
        ),
        disable_safe_capabilities=sum(1 for entry in entries if entry.disable_safe),
        dashboard_read_only_capabilities=sum(
            1 for entry in entries if entry.dashboard_read_only
        ),
        container_profile_declared_capabilities=sum(
            1 for entry in entries if entry.container_profile
        ),
        runtime_enablement_declared_capabilities=sum(
            1 for entry in entries if entry.runtime_enablement
        ),
        containerization_ready_capabilities=sum(
            1
            for entry in entries
            if entry.container_profile
            and entry.runtime_enablement
            and entry.disable_safe
            and entry.dashboard_read_only
            and not entry.direct_core_import_allowed
            and not entry.source_of_truth_override_allowed
            and not entry.runtime_mutation_allowed
        ),
        batch_containerization_readiness_required=True,
        read_only_load=result.read_only_load,
        active_deployment_created=result.active_deployment_created,
        ports_opened=result.ports_opened,
        containers_started=result.containers_started,
        runtime_mutation_allowed=result.runtime_mutation_allowed,
        direct_core_import_allowed=result.direct_core_import_allowed,
        source_of_truth_override_allowed=result.source_of_truth_override_allowed,
        containerization_ready_for_reference=True,
    )
