from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_storage_binding_builder import (
    build_media_storage_binding_contract,
)


_MEDIA_STORAGE_BINDING_FLOW = (
    "media_memory_read_model",
    "storage_registry_lookup",
    "storage_binding_contract",
    "dashboard_rag_read_only_preview",
)


def build_media_storage_binding_preview() -> Dict[str, object]:
    contract = build_media_storage_binding_contract()

    return {
        "flow": _MEDIA_STORAGE_BINDING_FLOW,
        "total_bindings": contract.total_bindings,
        "storage_ready_bindings": contract.storage_ready_bindings,
        "dashboard_visible_bindings": contract.dashboard_visible_bindings,
        "retrieval_visible_bindings": contract.retrieval_visible_bindings,
        "binary_external_bindings": contract.binary_external_bindings,
        "binding_ready": contract.binding_ready,
        "preview_ready": True,
        "entries": tuple(
            {
                "artifact_id": entry.artifact_id,
                "artifact_ref": entry.artifact_ref,
                "artifact_kind": entry.artifact_kind,
                "storage_registry_id": entry.storage_registry_id,
                "storage_entry_kind": entry.storage_entry_kind,
                "binary_external": entry.binary_external,
                "dashboard_visible": entry.dashboard_visible,
                "retrieval_visible": entry.retrieval_visible,
                "storage_binding_ready": entry.storage_binding_ready,
            }
            for entry in contract.entries
        ),
    }
