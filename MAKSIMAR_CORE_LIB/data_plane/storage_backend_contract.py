from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.data_plane.storage_backend_models import (
    POSTGRES_MAIN_BACKEND_MARKER,
    StorageBackendDescriptor,
    StorageBackendKind,
    StorageBackendReadinessReadModel,
    StorageBackendStatus,
)


@dataclass(frozen=True, slots=True)
class StorageBackendRegistry:
    registry_id: str
    backends: tuple[StorageBackendDescriptor, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.registry_id:
            raise ValueError("registry_id must not be empty")
        if not isinstance(self.backends, tuple):
            raise TypeError("backends must be a tuple")
        seen_ids: set[str] = set()
        for backend in self.backends:
            if not isinstance(backend, StorageBackendDescriptor):
                raise TypeError("backends must contain StorageBackendDescriptor")
            if backend.backend_id in seen_ids:
                raise ValueError("backend_id values must be unique")
            seen_ids.add(backend.backend_id)
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def require_backend(self, backend_id: str) -> StorageBackendDescriptor:
        if not backend_id:
            raise ValueError("backend_id must not be empty")
        for backend in self.backends:
            if backend.backend_id == backend_id:
                return backend
        raise ValueError(f"backend not registered: {backend_id}")


def build_postgres_main_descriptor(*, backend_id: str, endpoint_ref: str) -> StorageBackendDescriptor:
    return StorageBackendDescriptor(
        backend_id=backend_id,
        backend_kind=StorageBackendKind.POSTGRES_MAIN,
        status=StorageBackendStatus.POLICY_GATED,
        endpoint_ref=endpoint_ref,
        capability_ids=(
            POSTGRES_MAIN_BACKEND_MARKER,
            "transactional_metadata_store",
            "policy_gated_runtime_binding",
        ),
        reason_codes=(
            "postgres_main_declared_as_contract_surface",
            "runtime_connection_requires_separate_adapter_gate",
        ),
    )


def build_storage_backend_readiness_read_model(
    backend: StorageBackendDescriptor,
) -> StorageBackendReadinessReadModel:
    if not isinstance(backend, StorageBackendDescriptor):
        raise TypeError("backend must be StorageBackendDescriptor")

    return StorageBackendReadinessReadModel(
        backend_id=backend.backend_id,
        backend_kind=backend.backend_kind.value,
        status=backend.status.value,
        capability_count=len(backend.capability_ids),
        reason_codes=backend.reason_codes,
    )
