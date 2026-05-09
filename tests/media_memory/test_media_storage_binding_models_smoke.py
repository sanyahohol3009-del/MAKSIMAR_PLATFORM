from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    MediaStorageBindingEntry,
)


def test_media_storage_binding_models_smoke() -> None:
    entry = MediaStorageBindingEntry(
        artifact_id="media_artifact_generated_image",
        artifact_ref="artifact://media/generated/image_001.png",
        artifact_kind="generated_image",
        storage_registry_id="storage_registry_media_artifact_store",
        storage_entry_kind="media_artifact_store",
        binary_external=True,
        dashboard_visible=True,
        retrieval_visible=True,
        storage_binding_ready=True,
    )

    assert entry.storage_binding_ready is True
    assert entry.binary_external is True
