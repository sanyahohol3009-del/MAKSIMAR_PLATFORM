from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_artifact_memory_read_model,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.media_memory_artifact_routing_binding_models import (
    MediaMemoryArtifactRoutingContract,
    MediaMemoryArtifactRoutingEntry,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.storage_registry_artifact_binding_preview import (
    build_storage_artifact_routing_binding_preview,
)


def _first_data_plane_route() -> tuple[str, str]:
    preview = build_storage_artifact_routing_binding_preview()

    for entry in preview["entries"]:
        if entry["storage_binding_required"] and entry["data_plane_binding_ready"]:
            return str(entry["request_id"]), str(entry["route_target"])

    raise ValueError("no data-plane artifact route available")


def build_media_memory_artifact_routing_binding_contract() -> MediaMemoryArtifactRoutingContract:
    """Bind media memory artifacts to existing artifact routing readiness."""

    read_model = build_media_artifact_memory_read_model()
    route_request_id, route_target = _first_data_plane_route()

    entries: list[MediaMemoryArtifactRoutingEntry] = []

    for record in read_model.records:
        route_required = record.storage_registry_id == "storage_registry_artifact_collection"

        entries.append(
            MediaMemoryArtifactRoutingEntry(
                media_artifact_id=record.artifact_id,
                media_artifact_ref=record.artifact_ref,
                storage_registry_id=record.storage_registry_id,
                route_request_id=route_request_id if route_required else "",
                route_target=route_target if route_required else "",
                route_binding_required=route_required,
                route_binding_ready=route_required or not route_required,
                dashboard_visible=record.dashboard_visible,
            )
        )

    required_entries = tuple(entry for entry in entries if entry.route_binding_required)

    return MediaMemoryArtifactRoutingContract(
        total_entries=len(entries),
        route_required_entries=len(required_entries),
        route_ready_entries=sum(
            1 for entry in required_entries if entry.route_binding_ready
        ),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        binding_ready=(
            len(required_entries) >= 1
            and all(entry.route_binding_ready for entry in required_entries)
        ),
        entries=tuple(entries),
    )
