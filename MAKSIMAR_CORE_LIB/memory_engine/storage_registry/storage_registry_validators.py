from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_registry_models import (
    StorageRegistryContract,
)


def validate_storage_registry_ready(contract: StorageRegistryContract) -> bool:
    if contract.total_entries <= 0:
        raise ValueError("storage registry must contain at least one entry")

    if contract.dashboard_visible_entries <= 0:
        raise ValueError("storage registry must expose at least one dashboard entry")

    if contract.nas_ready_entries != contract.total_entries:
        raise ValueError("all storage registry entries must be NAS-ready")

    if contract.relocation_ready_entries != contract.total_entries:
        raise ValueError("all storage registry entries must be relocation-ready")

    registry_ids = tuple(entry.registry_id for entry in contract.entries)
    if len(set(registry_ids)) != len(registry_ids):
        raise ValueError("storage registry ids must be unique")

    return True
