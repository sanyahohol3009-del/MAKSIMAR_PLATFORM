from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.capability_registry.capability_registry_loader import (
    CapabilityRegistryLoadResult,
    load_canonical_capability_registry,
)
from MAKSIMAR_CORE_LIB.capability_registry.capability_truth_status_models import (
    CapabilityTruthStatusContract,
    CapabilityTruthStatusEntry,
)


def _entry_truth_status(integration_policy: str) -> str:
    if integration_policy == "adapter_only":
        return "ADAPTER_ONLY"
    if integration_policy == "quarantine_only":
        return "QUARANTINE_ONLY"
    if integration_policy == "excluded_from_core":
        return "EXCLUDED"
    return "MANIFEST_ONLY"


def _entry_adapter_paths(linked_surface_paths: tuple[str, ...], integration_policy: str) -> tuple[str, ...]:
    if integration_policy != "adapter_only":
        return ()
    adapter_paths = tuple(path for path in linked_surface_paths if "/adapters/" in path)
    if adapter_paths:
        return adapter_paths
    return linked_surface_paths


def _entry_quarantine_refs(integration_policy: str) -> tuple[str, ...]:
    if integration_policy in {"adapter_only", "quarantine_only"}:
        return ("MAKSIMAR_CORE_LIB/security_layer/repository_quarantine_policy.py",)
    return ()


def _entry_source_paths(linked_surface_paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        path
        for path in linked_surface_paths
        if path.startswith("MAKSIMAR_CORE_LIB/") or path.startswith("MAKSIMAR_SERVER/")
    )


@dataclass(frozen=True, slots=True)
class CapabilityTruthStatusLoadResult:
    schema_version: str
    registry_id: str
    source_registry_id: str
    capability_registry_source_path: str
    contract: CapabilityTruthStatusContract
    read_only_load: bool
    implemented_runtime_count: int
    non_runtime_count: int
    runtime_false_positive_count: int
    containerization_ready_count: int
    ports_opened: bool
    containers_started: bool
    active_deployment_created: bool
    runtime_mutation_allowed: bool
    direct_core_import_allowed: bool
    source_of_truth_override_allowed: bool

    def __post_init__(self) -> None:
        if self.schema_version != "capability_truth_status_load_result.v1":
            raise ValueError("schema_version must be capability_truth_status_load_result.v1")
        if self.registry_id != "phase_1_capability_truth_status_load_result":
            raise ValueError("registry_id must be phase_1_capability_truth_status_load_result")
        if self.source_registry_id != "phase_1_canonical_capability_registry":
            raise ValueError("unexpected source_registry_id")
        if not self.capability_registry_source_path:
            raise ValueError("capability_registry_source_path must not be empty")
        if not isinstance(self.contract, CapabilityTruthStatusContract):
            raise TypeError("contract must be CapabilityTruthStatusContract")
        if not self.read_only_load:
            raise ValueError("read_only_load must remain true")
        if self.implemented_runtime_count != self.contract.implemented_runtime_statuses:
            raise ValueError("implemented_runtime_count must match contract")
        if self.non_runtime_count != self.contract.non_runtime_statuses:
            raise ValueError("non_runtime_count must match contract")
        if self.runtime_false_positive_count != 0:
            raise ValueError("runtime_false_positive_count must remain 0")
        if self.containerization_ready_count != self.contract.total_statuses:
            raise ValueError("all truth statuses must be containerization-ready")
        if self.ports_opened:
            raise ValueError("ports_opened must remain false")
        if self.containers_started:
            raise ValueError("containers_started must remain false")
        if self.active_deployment_created:
            raise ValueError("active_deployment_created must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.direct_core_import_allowed:
            raise ValueError("direct_core_import_allowed must remain false")
        if self.source_of_truth_override_allowed:
            raise ValueError("source_of_truth_override_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_id": self.registry_id,
            "source_registry_id": self.source_registry_id,
            "capability_registry_source_path": self.capability_registry_source_path,
            "read_only_load": self.read_only_load,
            "implemented_runtime_count": self.implemented_runtime_count,
            "non_runtime_count": self.non_runtime_count,
            "runtime_false_positive_count": self.runtime_false_positive_count,
            "containerization_ready_count": self.containerization_ready_count,
            "ports_opened": self.ports_opened,
            "containers_started": self.containers_started,
            "active_deployment_created": self.active_deployment_created,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_core_import_allowed": self.direct_core_import_allowed,
            "source_of_truth_override_allowed": self.source_of_truth_override_allowed,
            "contract": self.contract.to_dict(),
        }


def build_capability_truth_status_contract(
    load_result: CapabilityRegistryLoadResult | None = None,
) -> CapabilityTruthStatusContract:
    result = load_result or load_canonical_capability_registry()

    entries: list[CapabilityTruthStatusEntry] = []
    for capability in result.contract.entries:
        truth_status = _entry_truth_status(capability.integration_policy)
        adapter_paths = _entry_adapter_paths(
            capability.linked_surface_paths,
            capability.integration_policy,
        )

        entries.append(
            CapabilityTruthStatusEntry(
                capability_id=capability.capability_id,
                truth_status=truth_status,
                evidence_level="read_model_only",
                container_profile=capability.container_profile,
                runtime_enablement=capability.runtime_enablement,
                spec_paths=(result.source_path,),
                manifest_paths=capability.linked_surface_paths,
                source_paths=_entry_source_paths(capability.linked_surface_paths),
                adapter_paths=adapter_paths,
                quarantine_policy_refs=_entry_quarantine_refs(capability.integration_policy),
                runtime_evidence_paths=(),
                runtime_test_paths=(),
                runtime_implemented=False,
                runtime_execution_verified=False,
                disable_safe=capability.disable_safe,
                dashboard_read_only=capability.dashboard_read_only,
                direct_core_import_allowed=capability.direct_core_import_allowed,
                source_of_truth_override_allowed=capability.source_of_truth_override_allowed,
                runtime_mutation_allowed=capability.runtime_mutation_allowed,
                ports_opened=False,
                containers_started=False,
                active_deployment_created=False,
                containerization_ready=True,
                reason_codes=(
                    "truth_status_built_from_read_only_capability_registry",
                    "runtime_evidence_absent",
                    "manifest_or_adapter_is_not_runtime",
                ),
            )
        )

    implemented_count = sum(1 for entry in entries if entry.truth_status == "IMPLEMENTED")

    return CapabilityTruthStatusContract(
        schema_version="capability_truth_status.v1",
        registry_id="phase_1_capability_truth_status_registry",
        total_statuses=len(entries),
        implemented_runtime_statuses=implemented_count,
        non_runtime_statuses=len(entries) - implemented_count,
        containerization_ready_statuses=sum(1 for entry in entries if entry.containerization_ready),
        entries=tuple(entries),
    )


def load_capability_truth_status_registry() -> CapabilityTruthStatusLoadResult:
    source_result = load_canonical_capability_registry()
    contract = build_capability_truth_status_contract(source_result)

    runtime_false_positive_count = sum(
        1
        for entry in contract.entries
        if entry.truth_status != "IMPLEMENTED"
        and (entry.runtime_implemented or entry.runtime_execution_verified)
    )

    return CapabilityTruthStatusLoadResult(
        schema_version="capability_truth_status_load_result.v1",
        registry_id="phase_1_capability_truth_status_load_result",
        source_registry_id=source_result.registry_id,
        capability_registry_source_path=source_result.source_path,
        contract=contract,
        read_only_load=True,
        implemented_runtime_count=contract.implemented_runtime_statuses,
        non_runtime_count=contract.non_runtime_statuses,
        runtime_false_positive_count=runtime_false_positive_count,
        containerization_ready_count=contract.containerization_ready_statuses,
        ports_opened=False,
        containers_started=False,
        active_deployment_created=False,
        runtime_mutation_allowed=False,
        direct_core_import_allowed=False,
        source_of_truth_override_allowed=False,
    )
