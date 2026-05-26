from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


CapabilityFamily = Literal[
    "workflow_orchestration",
    "approval_governance",
    "retrieval_memory",
    "codegen_governance",
    "media_artifact",
    "module_dashboard",
    "container_boundary",
    "engine_runtime",
    "worker_runtime",
    "domain_cube",
]

CapabilityIntegrationPolicy = Literal[
    "maksimar_owned",
    "excluded_from_core",
    "adapter_only",
    "quarantine_only",
]

CapabilitySourceKind = Literal[
    "maksimar_surface",
    "open_source_candidate",
    "external_backend_reference",
]

CapabilityContainerProfile = Literal[
    "core_library",
    "server_service",
    "worker_service",
    "product_cube",
    "external_backend",
    "not_loaded",
]

CapabilityRuntimeEnablement = Literal[
    "disabled",
    "read_only_reference",
    "requires_operator_approval",
]


_CAPABILITY_ID_PATTERN = re.compile(r"^cap_[a-z][a-z0-9_]*$")
_SURFACE_PATH_PATTERN = re.compile(r"^[A-Za-z0-9_./-]+$")


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


def _ensure_unique_surface_paths(paths: tuple[str, ...], owner_id: str) -> tuple[str, ...]:
    if not isinstance(paths, tuple):
        raise ValueError("linked_surface_paths must be a tuple")
    if not paths:
        raise ValueError(f"linked_surface_paths must not be empty for {owner_id}")
    if len(set(paths)) != len(paths):
        raise ValueError(f"duplicate linked_surface_paths for {owner_id}")

    normalized_paths: list[str] = []
    for path in paths:
        normalized = _ensure_non_empty_str(path, "linked_surface_path")
        if not _SURFACE_PATH_PATTERN.fullmatch(normalized):
            raise ValueError(f"invalid linked surface path for {owner_id}: {normalized}")
        if normalized.startswith("EXTERNAL_BACKENDS/"):
            raise ValueError(
                f"capability registry must not bind directly to external backend source: {owner_id}"
            )
        if "source/benchmarks" in normalized or "smoke_reports" in normalized:
            raise ValueError(
                f"capability registry must not bind to raw benchmark or smoke report output: {owner_id}"
            )
        normalized_paths.append(normalized)

    return tuple(normalized_paths)


@dataclass(frozen=True, slots=True)
class CapabilityRegistryEntry:
    """Canonical capability entry.

    This model is a registry/read-model contract. It is not a runtime executor.
    """

    capability_id: str
    title: str
    family: CapabilityFamily
    integration_policy: CapabilityIntegrationPolicy
    source_kind: CapabilitySourceKind
    owner_surface: str
    linked_surface_paths: tuple[str, ...]
    container_profile: CapabilityContainerProfile
    runtime_enablement: CapabilityRuntimeEnablement
    disable_safe: bool
    dashboard_read_only: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool
    runtime_mutation_allowed: bool
    description: str

    def __post_init__(self) -> None:
        capability_id = _ensure_non_empty_str(self.capability_id, "capability_id")
        title = _ensure_non_empty_str(self.title, "title")
        owner_surface = _ensure_non_empty_str(self.owner_surface, "owner_surface")
        description = _ensure_non_empty_str(self.description, "description")

        if not _CAPABILITY_ID_PATTERN.fullmatch(capability_id):
            raise ValueError(f"invalid capability_id: {capability_id}")

        linked_surface_paths = _ensure_unique_surface_paths(
            self.linked_surface_paths,
            capability_id,
        )

        if self.source_kind == "maksimar_surface":
            if self.integration_policy not in {"maksimar_owned", "excluded_from_core"}:
                raise ValueError(
                    f"maksimar_surface must be maksimar_owned or excluded_from_core: {capability_id}"
                )

        if self.source_kind != "maksimar_surface":
            if self.integration_policy not in {"adapter_only", "quarantine_only"}:
                raise ValueError(
                    f"external capability must be adapter_only or quarantine_only: {capability_id}"
                )
            if self.container_profile != "external_backend":
                raise ValueError(
                    f"external capability must use external_backend container profile: {capability_id}"
                )

        if self.integration_policy == "excluded_from_core":
            if self.container_profile not in {"not_loaded", "external_backend"}:
                raise ValueError(
                    f"excluded capability must be not_loaded or external_backend: {capability_id}"
                )

        if self.runtime_enablement == "disabled" and self.container_profile == "core_library":
            raise ValueError(
                f"disabled capability cannot claim core_library container profile: {capability_id}"
            )

        if not _ensure_bool(self.disable_safe, "disable_safe"):
            raise ValueError(f"disable_safe must remain true: {capability_id}")
        if not _ensure_bool(self.dashboard_read_only, "dashboard_read_only"):
            raise ValueError(f"dashboard_read_only must remain true: {capability_id}")
        if _ensure_bool(self.direct_core_import_allowed, "direct_core_import_allowed"):
            raise ValueError(f"direct_core_import_allowed must remain false: {capability_id}")
        if _ensure_bool(
            self.source_of_truth_override_allowed,
            "source_of_truth_override_allowed",
        ):
            raise ValueError(
                f"source_of_truth_override_allowed must remain false: {capability_id}"
            )
        if _ensure_bool(self.runtime_mutation_allowed, "runtime_mutation_allowed"):
            raise ValueError(f"runtime_mutation_allowed must remain false: {capability_id}")

        object.__setattr__(self, "capability_id", capability_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "owner_surface", owner_surface)
        object.__setattr__(self, "linked_surface_paths", linked_surface_paths)
        object.__setattr__(self, "description", description)


@dataclass(frozen=True, slots=True)
class CapabilityRegistryContract:
    """Unified canonical capability registry contract."""

    schema_version: str
    registry_id: str
    total_capabilities: int
    entries: tuple[CapabilityRegistryEntry, ...]

    def __post_init__(self) -> None:
        schema_version = _ensure_non_empty_str(self.schema_version, "schema_version")
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")

        if schema_version != "canonical_capability_registry.v1":
            raise ValueError("schema_version must be canonical_capability_registry.v1")
        if registry_id != "phase_1_canonical_capability_registry":
            raise ValueError("registry_id must be phase_1_canonical_capability_registry")
        if not isinstance(self.entries, tuple):
            raise ValueError("entries must be a tuple")
        if self.total_capabilities != len(self.entries):
            raise ValueError("total_capabilities must match entries length")
        if self.total_capabilities <= 0:
            raise ValueError("total_capabilities must be >= 1")

        capability_ids = tuple(entry.capability_id for entry in self.entries)
        if len(set(capability_ids)) != len(capability_ids):
            raise ValueError("duplicate capability_id values detected")

        for entry in self.entries:
            if not entry.disable_safe:
                raise ValueError(f"capability must be disable-safe: {entry.capability_id}")
            if not entry.dashboard_read_only:
                raise ValueError(
                    f"capability must remain dashboard read-only: {entry.capability_id}"
                )
            if entry.direct_core_import_allowed:
                raise ValueError(
                    f"capability cannot allow direct core import: {entry.capability_id}"
                )
            if entry.source_of_truth_override_allowed:
                raise ValueError(
                    f"capability cannot override source of truth: {entry.capability_id}"
                )
            if entry.runtime_mutation_allowed:
                raise ValueError(
                    f"capability cannot mutate runtime: {entry.capability_id}"
                )

        object.__setattr__(self, "schema_version", schema_version)
        object.__setattr__(self, "registry_id", registry_id)


def build_canonical_capability_registry_contract() -> CapabilityRegistryContract:
    entries = (
        CapabilityRegistryEntry(
            capability_id="cap_module_manifest_surface",
            title="Module manifest surface",
            family="module_dashboard",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/module_manifest/module_manifest_schema.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/module_manifest/module_manifest_schema.py",
                "MAKSIMAR_CORE_LIB/oob_dashboard/module_manifest_contract.py",
                "MAKSIMAR_CORE_LIB/oob_dashboard/module_permission_matrix_contract.py",
            ),
            container_profile="core_library",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Canonical module manifest and dashboard permission capability surface.",
        ),
        CapabilityRegistryEntry(
            capability_id="cap_container_boundary_surface",
            title="Container boundary surface",
            family="container_boundary",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/network_containerization/container_contract_models.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/network_containerization/container_contract_models.py",
                "MAKSIMAR_CORE_LIB/network_containerization/container_exposure_policy.py",
                "MAKSIMAR_CORE_LIB/network_containerization/network_trust_boundary_binding_models.py",
            ),
            container_profile="core_library",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Container and trust-boundary capability surface for future adapters and cubes.",
        ),
        CapabilityRegistryEntry(
            capability_id="cap_engine_runtime_surface",
            title="Engine runtime capability surface",
            family="engine_runtime",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/engine_capability_contract/engine_capability_contract.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/engine_capability_contract/engine_capability_contract.py",
                "MAKSIMAR_CORE_LIB/engine_adapter_boundary/engine_adapter_boundary_contract.py",
                "MAKSIMAR_SERVER/WORKERS/simulation_worker/capability_contract.py",
            ),
            container_profile="worker_service",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Engine capability surface bound to engine adapter boundaries.",
        ),
        CapabilityRegistryEntry(
            capability_id="cap_worker_runtime_surface",
            title="Worker runtime capability surface",
            family="worker_runtime",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/workers_registry/worker_capability_models.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/workers_registry/worker_capability_models.py",
                "MAKSIMAR_CORE_LIB/workers_registry/worker_capability_contract.py",
                "MAKSIMAR_CORE_LIB/workers_registry/worker_registry_contract.py",
            ),
            container_profile="worker_service",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Worker capability registry surface for execution workers.",
        ),
        CapabilityRegistryEntry(
            capability_id="cap_domain_cube_surface",
            title="Domain cube capability surface",
            family="domain_cube",
            integration_policy="maksimar_owned",
            source_kind="maksimar_surface",
            owner_surface="MAKSIMAR_CORE_LIB/skill_domain_binding/cube_binding_models.py",
            linked_surface_paths=(
                "MAKSIMAR_CORE_LIB/skill_domain_binding/cube_binding_models.py",
                "MAKSIMAR_CORE_LIB/skill_domain_binding/skill_binding_models.py",
                "MAKSIMAR_CORE_LIB/skill_domain_binding/shell_adapter_binding_models.py",
            ),
            container_profile="product_cube",
            runtime_enablement="read_only_reference",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="Domain cube capability surface bound to skill/domain/shell adapters.",
        ),
        CapabilityRegistryEntry(
            capability_id="cap_external_retrieval_adapter_candidate",
            title="External retrieval adapter candidate",
            family="retrieval_memory",
            integration_policy="adapter_only",
            source_kind="external_backend_reference",
            owner_surface="docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json",
            linked_surface_paths=(
                "docs/architecture/open_source_integration/open_source_exclusion_registry_v1.json",
                "MAKSIMAR_CORE_LIB/security_layer/repository_quarantine_policy.py",
                "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/adapters/mempalace_adapter.py",
            ),
            container_profile="external_backend",
            runtime_enablement="requires_operator_approval",
            disable_safe=True,
            dashboard_read_only=True,
            direct_core_import_allowed=False,
            source_of_truth_override_allowed=False,
            runtime_mutation_allowed=False,
            description="External retrieval systems can only be adapter-bound and approval-gated.",
        ),
    )

    return CapabilityRegistryContract(
        schema_version="canonical_capability_registry.v1",
        registry_id="phase_1_canonical_capability_registry",
        total_capabilities=len(entries),
        entries=entries,
    )
