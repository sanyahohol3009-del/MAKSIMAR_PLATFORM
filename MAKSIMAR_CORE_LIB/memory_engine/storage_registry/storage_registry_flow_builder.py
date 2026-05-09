from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_registry_preview_builder import (
    build_storage_registry_preview,
)


_STORAGE_REGISTRY_FLOW = (
    "history_ingestion_storage_primitives",
    "storage_registry_contract",
    "artifact_collection_reference",
    "model_store_reference",
    "media_artifact_reference",
    "retrieval_index_reference",
    "portability_policy",
    "dashboard_read_only_preview",
)


def build_storage_registry_flow_preview() -> Dict[str, object]:
    preview = build_storage_registry_preview()

    return {
        "flow": _STORAGE_REGISTRY_FLOW,
        "total_entries": preview["total_entries"],
        "storage_ready_for_m2_nas": preview["storage_ready_for_m2_nas"],
        "preview_ready": preview["preview_ready"],
        "flow_ready": True,
    }
