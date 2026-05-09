from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_flow_preview,
)


def test_storage_registry_flow_builder_smoke() -> None:
    flow = build_storage_registry_flow_preview()

    assert flow["flow_ready"] is True
    assert flow["storage_ready_for_m2_nas"] is True
    assert flow["flow"] == (
        "history_ingestion_storage_primitives",
        "storage_registry_contract",
        "artifact_collection_reference",
        "model_store_reference",
        "media_artifact_reference",
        "retrieval_index_reference",
        "portability_policy",
        "dashboard_read_only_preview",
    )
