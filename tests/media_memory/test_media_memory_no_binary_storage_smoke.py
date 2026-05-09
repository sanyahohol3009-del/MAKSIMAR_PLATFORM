from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_artifact_memory_read_model,
    build_media_storage_binding_preview,
)


def test_media_memory_no_binary_storage_smoke() -> None:
    read_model = build_media_artifact_memory_read_model()
    binding_preview = build_media_storage_binding_preview()

    assert read_model.binary_external_records == read_model.total_records
    assert binding_preview["binary_external_bindings"] == binding_preview["total_bindings"]

    for record in read_model.records:
        assert record.binary_external is True
        assert record.artifact_ref.startswith("artifact://")
