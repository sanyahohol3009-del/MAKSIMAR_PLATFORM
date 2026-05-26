from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal


CapabilityTruthStatus = Literal[
    "SPEC_ONLY",
    "MANIFEST_ONLY",
    "ADAPTER_ONLY",
    "QUARANTINE_ONLY",
    "IMPLEMENTED",
    "EXCLUDED",
]

RuntimeEvidenceLevel = Literal[
    "none",
    "read_model_only",
    "runtime_verified",
]

ContainerProfile = Literal[
    "core_library",
    "server_service",
    "worker_service",
    "product_cube",
    "external_backend",
    "not_loaded",
]

RuntimeEnablement = Literal[
    "disabled",
    "read_only_reference",
    "requires_operator_approval",
]

_ALLOWED_STATUSES = {
    "SPEC_ONLY",
    "MANIFEST_ONLY",
    "ADAPTER_ONLY",
    "QUARANTINE_ONLY",
    "IMPLEMENTED",
    "EXCLUDED",
}

_CAPABILITY_ID_PATTERN = re.compile(r"^cap_[a-z][a-z0-9_]*$")
_PATH_PATTERN = re.compile(r"^[A-Za-z0-9_./-]+$")


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


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _validate_paths(paths: tuple[str, ...], field_name: str, owner_id: str) -> tuple[str, ...]:
    if not isinstance(paths, tuple):
        raise ValueError(f"{field_name} must be a tuple")

    normalized_paths: list[str] = []
    for path in paths:
        normalized = _ensure_non_empty_str(path, field_name)
        if not _PATH_PATTERN.fullmatch(normalized):
            raise ValueError(f"invalid path in {field_name} for {owner_id}: {normalized}")
        if "__pycache__" in normalized or normalized.endswith((".pyc", ".pyo")):
            raise ValueError(f"{field_name} must not reference compiled cache files: {owner_id}")
        if "source/benchmarks" in normalized or "smoke_reports" in normalized:
            raise ValueError(f"{field_name} must not reference raw benchmark/smoke outputs: {owner_id}")
        normalized_paths.append(normalized)

    if len(set(normalized_paths)) != len(normalized_paths):
        raise ValueError(f"duplicate paths in {field_name} for {owner_id}")

    return tuple(normalized_paths)


@dataclass(frozen=True, slots=True)
class CapabilityTruthStatusEntry:
    """Truth status for one capability.

    Runtime is considered real only when IMPLEMENTED status has real runtime evidence,
    runtime tests and verified runtime execution. Docs, YAML, manifests, registry entries
    and adapter candidates never count as runtime by themselves.
    """

    capability_id: str
    truth_status: CapabilityTruthStatus
    evidence_level: RuntimeEvidenceLevel
    container_profile: ContainerProfile
    runtime_enablement: RuntimeEnablement
    spec_paths: tuple[str, ...]
    manifest_paths: tuple[str, ...]
    source_paths: tuple[str, ...]
    adapter_paths: tuple[str, ...]
    quarantine_policy_refs: tuple[str, ...]
    runtime_evidence_paths: tuple[str, ...]
    runtime_test_paths: tuple[str, ...]
    runtime_implemented: bool
    runtime_execution_verified: bool
    disable_safe: bool
    dashboard_read_only: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    runtime_mutation_allowed: bool
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    containerization_ready: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        capability_id = _ensure_non_empty_str(self.capability_id, "capability_id")
        if not _CAPABILITY_ID_PATTERN.fullmatch(capability_id):
            raise ValueError(f"invalid capability_id: {capability_id}")

        if self.truth_status not in _ALLOWED_STATUSES:
            raise ValueError(f"unknown truth_status for {capability_id}: {self.truth_status}")

        spec_paths = _validate_paths(self.spec_paths, "spec_paths", capability_id)
        manifest_paths = _validate_paths(self.manifest_paths, "manifest_paths", capability_id)
        source_paths = _validate_paths(self.source_paths, "source_paths", capability_id)
        adapter_paths = _validate_paths(self.adapter_paths, "adapter_paths", capability_id)
        quarantine_policy_refs = _validate_paths(
            self.quarantine_policy_refs,
            "quarantine_policy_refs",
            capability_id,
        )
        runtime_evidence_paths = _validate_paths(
            self.runtime_evidence_paths,
            "runtime_evidence_paths",
            capability_id,
        )
        runtime_test_paths = _validate_paths(
            self.runtime_test_paths,
            "runtime_test_paths",
            capability_id,
        )
        reason_codes = _validate_paths(self.reason_codes, "reason_codes", capability_id)

        if not reason_codes:
            raise ValueError(f"reason_codes must not be empty for {capability_id}")

        runtime_implemented = _ensure_bool(self.runtime_implemented, "runtime_implemented")
        runtime_execution_verified = _ensure_bool(
            self.runtime_execution_verified,
            "runtime_execution_verified",
        )

        if self.truth_status == "SPEC_ONLY":
            if not spec_paths:
                raise ValueError(f"SPEC_ONLY requires spec_paths for {capability_id}")
            if manifest_paths or source_paths or adapter_paths or runtime_evidence_paths or runtime_test_paths:
                raise ValueError(f"SPEC_ONLY must not include implementation evidence for {capability_id}")

        if self.truth_status == "MANIFEST_ONLY":
            if not manifest_paths:
                raise ValueError(f"MANIFEST_ONLY requires manifest_paths for {capability_id}")
            if runtime_evidence_paths or runtime_test_paths:
                raise ValueError(f"MANIFEST_ONLY must not include runtime evidence for {capability_id}")

        if self.truth_status == "ADAPTER_ONLY":
            if not adapter_paths:
                raise ValueError(f"ADAPTER_ONLY requires adapter_paths for {capability_id}")
            if runtime_evidence_paths or runtime_test_paths:
                raise ValueError(f"ADAPTER_ONLY must not include runtime evidence for {capability_id}")

        if self.truth_status == "QUARANTINE_ONLY":
            if not quarantine_policy_refs:
                raise ValueError(f"QUARANTINE_ONLY requires quarantine policy refs for {capability_id}")
            if runtime_evidence_paths or runtime_test_paths:
                raise ValueError(f"QUARANTINE_ONLY must not include runtime evidence for {capability_id}")

        if self.truth_status == "EXCLUDED":
            if runtime_implemented or runtime_execution_verified:
                raise ValueError(f"EXCLUDED cannot be runtime implemented for {capability_id}")
            if runtime_evidence_paths or runtime_test_paths:
                raise ValueError(f"EXCLUDED must not include runtime evidence for {capability_id}")

        if self.truth_status == "IMPLEMENTED":
            if self.evidence_level != "runtime_verified":
                raise ValueError(f"IMPLEMENTED requires runtime_verified evidence for {capability_id}")
            if self.runtime_enablement == "disabled":
                raise ValueError(f"IMPLEMENTED cannot use disabled runtime_enablement for {capability_id}")
            if not runtime_implemented:
                raise ValueError(f"IMPLEMENTED requires runtime_implemented true for {capability_id}")
            if not runtime_execution_verified:
                raise ValueError(f"IMPLEMENTED requires runtime_execution_verified true for {capability_id}")
            if not source_paths:
                raise ValueError(f"IMPLEMENTED requires source_paths for {capability_id}")
            if not runtime_evidence_paths:
                raise ValueError(f"IMPLEMENTED requires runtime_evidence_paths for {capability_id}")
            if not runtime_test_paths:
                raise ValueError(f"IMPLEMENTED requires runtime_test_paths for {capability_id}")
        else:
            if self.evidence_level == "runtime_verified":
                raise ValueError(f"{self.truth_status} cannot use runtime_verified evidence for {capability_id}")
            if runtime_implemented:
                raise ValueError(f"{self.truth_status} cannot be runtime_implemented for {capability_id}")
            if runtime_execution_verified:
                raise ValueError(f"{self.truth_status} cannot be runtime_execution_verified for {capability_id}")

        if not _ensure_bool(self.disable_safe, "disable_safe"):
            raise ValueError(f"disable_safe must remain true for {capability_id}")
        if not _ensure_bool(self.dashboard_read_only, "dashboard_read_only"):
            raise ValueError(f"dashboard_read_only must remain true for {capability_id}")
        if _ensure_bool(self.direct_core_import_allowed, "direct_core_import_allowed"):
            raise ValueError(f"direct_core_import_allowed must remain false for {capability_id}")
        if _ensure_bool(self.source_of_truth_override_allowed, "source_of_truth_override_allowed"):
            raise ValueError(f"source_of_truth_override_allowed must remain false for {capability_id}")
        if _ensure_bool(self.runtime_mutation_allowed, "runtime_mutation_allowed"):
            raise ValueError(f"runtime_mutation_allowed must remain false for {capability_id}")
        if _ensure_bool(self.ports_opened, "ports_opened"):
            raise ValueError(f"ports_opened must remain false for {capability_id}")
        if _ensure_bool(self.containers_started, "containers_started"):
            raise ValueError(f"containers_started must remain false for {capability_id}")
        if _ensure_bool(self.active_deployment_created, "active_deployment_created"):
            raise ValueError(f"active_deployment_created must remain false for {capability_id}")
        if not _ensure_bool(self.containerization_ready, "containerization_ready"):
            raise ValueError(f"containerization_ready must remain true for {capability_id}")

        object.__setattr__(self, "capability_id", capability_id)
        object.__setattr__(self, "spec_paths", spec_paths)
        object.__setattr__(self, "manifest_paths", manifest_paths)
        object.__setattr__(self, "source_paths", source_paths)
        object.__setattr__(self, "adapter_paths", adapter_paths)
        object.__setattr__(self, "quarantine_policy_refs", quarantine_policy_refs)
        object.__setattr__(self, "runtime_evidence_paths", runtime_evidence_paths)
        object.__setattr__(self, "runtime_test_paths", runtime_test_paths)
        object.__setattr__(self, "reason_codes", reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "truth_status": self.truth_status,
            "evidence_level": self.evidence_level,
            "container_profile": self.container_profile,
            "runtime_enablement": self.runtime_enablement,
            "spec_paths": list(self.spec_paths),
            "manifest_paths": list(self.manifest_paths),
            "source_paths": list(self.source_paths),
            "adapter_paths": list(self.adapter_paths),
            "quarantine_policy_refs": list(self.quarantine_policy_refs),
            "runtime_evidence_paths": list(self.runtime_evidence_paths),
            "runtime_test_paths": list(self.runtime_test_paths),
            "runtime_implemented": self.runtime_implemented,
            "runtime_execution_verified": self.runtime_execution_verified,
            "disable_safe": self.disable_safe,
            "dashboard_read_only": self.dashboard_read_only,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "containerization_ready": self.containerization_ready,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(frozen=True, slots=True)
class CapabilityTruthStatusContract:
    schema_version: str
    registry_id: str
    total_statuses: int
    implemented_runtime_statuses: int
    non_runtime_statuses: int
    containerization_ready_statuses: int
    entries: tuple[CapabilityTruthStatusEntry, ...]

    def __post_init__(self) -> None:
        schema_version = _ensure_non_empty_str(self.schema_version, "schema_version")
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")

        if schema_version != "capability_truth_status.v1":
            raise ValueError("schema_version must be capability_truth_status.v1")
        if registry_id != "phase_1_capability_truth_status_registry":
            raise ValueError("registry_id must be phase_1_capability_truth_status_registry")
        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be a tuple")
        if self.total_statuses != len(self.entries):
            raise ValueError("total_statuses must match entries length")
        if self.total_statuses <= 0:
            raise ValueError("total_statuses must be >= 1")

        capability_ids = tuple(entry.capability_id for entry in self.entries)
        if len(set(capability_ids)) != len(capability_ids):
            raise ValueError("duplicate capability_id values detected")

        computed_implemented = sum(1 for entry in self.entries if entry.truth_status == "IMPLEMENTED")
        computed_non_runtime = self.total_statuses - computed_implemented
        computed_container_ready = sum(1 for entry in self.entries if entry.containerization_ready)

        if self.implemented_runtime_statuses != computed_implemented:
            raise ValueError("implemented_runtime_statuses must match computed value")
        if self.non_runtime_statuses != computed_non_runtime:
            raise ValueError("non_runtime_statuses must match computed value")
        if self.containerization_ready_statuses != computed_container_ready:
            raise ValueError("containerization_ready_statuses must match computed value")
        if self.containerization_ready_statuses != self.total_statuses:
            raise ValueError("all truth statuses must be containerization-ready")

        for entry in self.entries:
            if entry.truth_status != "IMPLEMENTED":
                if entry.runtime_implemented:
                    raise ValueError(f"non-runtime status cannot be implemented: {entry.capability_id}")
                if entry.runtime_execution_verified:
                    raise ValueError(f"non-runtime status cannot be runtime verified: {entry.capability_id}")

        object.__setattr__(self, "schema_version", schema_version)
        object.__setattr__(self, "registry_id", registry_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_id": self.registry_id,
            "total_statuses": self.total_statuses,
            "implemented_runtime_statuses": self.implemented_runtime_statuses,
            "non_runtime_statuses": self.non_runtime_statuses,
            "containerization_ready_statuses": self.containerization_ready_statuses,
            "entries": [entry.to_dict() for entry in self.entries],
        }


def make_implemented_runtime_entry() -> CapabilityTruthStatusEntry:
    return CapabilityTruthStatusEntry(
        capability_id="cap_real_runtime_example",
        truth_status="IMPLEMENTED",
        evidence_level="runtime_verified",
        container_profile="worker_service",
        runtime_enablement="requires_operator_approval",
        spec_paths=("docs/architecture/open_source_integration/canonical_capability_registry_v1.yaml",),
        manifest_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_registry_models.py",),
        source_paths=("MAKSIMAR_CORE_LIB/capability_registry/capability_truth_status_models.py",),
        adapter_paths=(),
        quarantine_policy_refs=(),
        runtime_evidence_paths=("tests/capability_registry/test_capability_truth_status_models_smoke.py",),
        runtime_test_paths=("tests/capability_registry/test_capability_truth_status_models_smoke.py",),
        runtime_implemented=True,
        runtime_execution_verified=True,
        disable_safe=True,
        dashboard_read_only=True,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
        runtime_mutation_allowed=False,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        containerization_ready=True,
        reason_codes=("real_runtime_requires_source_tests_and_runtime_evidence",),
    )
