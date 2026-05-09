from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_artifact_memory_read_model,
    build_media_storage_binding_contract,
)


def test_media_storage_binding_builder_smoke() -> None:
    read_model = build_media_artifact_memory_read_model()
    contract = build_media_storage_binding_contract()

    assert contract.total_bindings == read_model.total_records
    assert contract.storage_ready_bindings == contract.total_bindings
    assert contract.binary_external_bindings == contract.total_bindings
    assert contract.binding_ready is True
