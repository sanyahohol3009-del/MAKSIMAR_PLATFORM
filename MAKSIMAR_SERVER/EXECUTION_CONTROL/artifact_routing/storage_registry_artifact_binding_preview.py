from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.storage_registry_artifact_binding_builder import (
    build_storage_artifact_routing_binding_contract,
)


_STORAGE_ARTIFACT_BINDING_FLOW = (
    "payload_classification",
    "artifact_routing",
    "storage_registry_lookup",
    "artifact_collection_binding",
    "data_plane_route_readiness",
    "dashboard_read_only_preview",
)


def build_storage_artifact_routing_binding_preview() -> Dict[str, object]:
    contract = build_storage_artifact_routing_binding_contract()

    return {
        "flow": _STORAGE_ARTIFACT_BINDING_FLOW,
        "total_entries": contract.total_entries,
        "storage_required_entries": contract.storage_required_entries,
        "storage_ready_entries": contract.storage_ready_entries,
        "data_plane_ready_entries": contract.data_plane_ready_entries,
        "dashboard_visible_entries": contract.dashboard_visible_entries,
        "binding_ready": contract.binding_ready,
        "preview_ready": True,
        "entries": tuple(
            {
                "request_id": entry.request_id,
                "route_target": entry.route_target,
                "routing_status": entry.routing_status,
                "artifact_ref": entry.artifact_ref,
                "owner_task_id": entry.owner_task_id,
                "storage_registry_id": entry.storage_registry_id,
                "artifact_collection_id": entry.artifact_collection_id,
                "storage_binding_required": entry.storage_binding_required,
                "storage_binding_ready": entry.storage_binding_ready,
                "data_plane_binding_ready": entry.data_plane_binding_ready,
                "dashboard_visible": entry.dashboard_visible,
            }
            for entry in contract.entries
        ),
    }
