from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_read_model import (
    build_media_artifact_memory_read_model,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_storage_binding_models import (
    MediaStorageBindingContract,
    MediaStorageBindingEntry,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_contract,
)


def build_media_storage_binding_contract() -> MediaStorageBindingContract:
    """Bind media memory records to existing storage registry entries."""

    read_model = build_media_artifact_memory_read_model()
    storage_registry = build_storage_registry_contract()

    registry_entry_kind_by_id = {
        entry.registry_id: entry.entry_kind
        for entry in storage_registry.entries
    }

    entries: list[MediaStorageBindingEntry] = []

    for record in read_model.records:
        if record.storage_registry_id not in registry_entry_kind_by_id:
            raise ValueError(
                f"storage_registry_id not found: {record.storage_registry_id}"
            )

        entries.append(
            MediaStorageBindingEntry(
                artifact_id=record.artifact_id,
                artifact_ref=record.artifact_ref,
                artifact_kind=record.artifact_kind,
                storage_registry_id=record.storage_registry_id,
                storage_entry_kind=registry_entry_kind_by_id[record.storage_registry_id],
                binary_external=record.binary_external,
                dashboard_visible=record.dashboard_visible,
                retrieval_visible=record.retrieval_visible,
                storage_binding_ready=True,
            )
        )

    return MediaStorageBindingContract(
        total_bindings=len(entries),
        storage_ready_bindings=sum(
            1 for entry in entries if entry.storage_binding_ready
        ),
        dashboard_visible_bindings=sum(
            1 for entry in entries if entry.dashboard_visible
        ),
        retrieval_visible_bindings=sum(
            1 for entry in entries if entry.retrieval_visible
        ),
        binary_external_bindings=sum(
            1 for entry in entries if entry.binary_external
        ),
        binding_ready=(
            len(entries) >= 1
            and all(entry.storage_binding_ready for entry in entries)
            and all(entry.binary_external for entry in entries)
        ),
        entries=tuple(entries),
    )
