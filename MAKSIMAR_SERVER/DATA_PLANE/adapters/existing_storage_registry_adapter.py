from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.storage_backend_contract import StorageBackendRegistry
from MAKSIMAR_SERVER.DATA_PLANE.adapters.data_plane_existing_storage_adapter import (
    DataPlaneExistingStorageAdapterBinding,
    build_existing_storage_adapter_binding,
)


def bind_existing_storage_registry(
    registry: StorageBackendRegistry,
) -> DataPlaneExistingStorageAdapterBinding:
    return build_existing_storage_adapter_binding(registry)
