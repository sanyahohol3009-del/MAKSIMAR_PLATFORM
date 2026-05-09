from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.media_memory_artifact_routing_binding_builder import (
    build_media_memory_artifact_routing_binding_contract,
)


_MEDIA_MEMORY_ARTIFACT_ROUTING_FLOW = (
    "media_memory_read_model",
    "storage_registry_binding",
    "artifact_routing_binding",
    "data_plane_route_reference",
    "dashboard_read_only_preview",
)


def build_media_memory_artifact_routing_binding_preview() -> Dict[str, object]:
    contract = build_media_memory_artifact_routing_binding_contract()

    return {
        "flow": _MEDIA_MEMORY_ARTIFACT_ROUTING_FLOW,
        "total_entries": contract.total_entries,
        "route_required_entries": contract.route_required_entries,
        "route_ready_entries": contract.route_ready_entries,
        "dashboard_visible_entries": contract.dashboard_visible_entries,
        "binding_ready": contract.binding_ready,
        "preview_ready": True,
        "entries": tuple(
            {
                "media_artifact_id": entry.media_artifact_id,
                "media_artifact_ref": entry.media_artifact_ref,
                "storage_registry_id": entry.storage_registry_id,
                "route_request_id": entry.route_request_id,
                "route_target": entry.route_target,
                "route_binding_required": entry.route_binding_required,
                "route_binding_ready": entry.route_binding_ready,
                "dashboard_visible": entry.dashboard_visible,
            }
            for entry in contract.entries
        ),
    }
