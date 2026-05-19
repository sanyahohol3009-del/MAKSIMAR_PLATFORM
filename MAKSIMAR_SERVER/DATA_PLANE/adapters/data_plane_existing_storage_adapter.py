from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.data_plane.storage_backend_contract import StorageBackendRegistry


@dataclass(frozen=True, slots=True)
class DataPlaneExistingStorageAdapterBinding:
    binding_id: str
    registry_id: str
    backend_count: int
    reference_only: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.binding_id:
            raise ValueError("binding_id must not be empty")
        if not self.registry_id:
            raise ValueError("registry_id must not be empty")
        if self.backend_count < 0:
            raise ValueError("backend_count must not be negative")
        if not self.reference_only:
            raise ValueError("reference_only must remain true")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")


def build_existing_storage_adapter_binding(
    registry: StorageBackendRegistry,
) -> DataPlaneExistingStorageAdapterBinding:
    if not isinstance(registry, StorageBackendRegistry):
        raise TypeError("registry must be StorageBackendRegistry")

    return DataPlaneExistingStorageAdapterBinding(
        binding_id="data_plane_existing_storage_adapter_binding_v1",
        registry_id=registry.registry_id,
        backend_count=len(registry.backends),
        reference_only=True,
        reason_codes=(
            "existing_storage_registry_bound_reference_only",
            "runtime_connection_requires_explicit_adapter_gate",
        ),
    )
