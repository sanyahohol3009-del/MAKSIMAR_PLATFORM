from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    MediaMemoryArtifactRoutingEntry,
)


def test_media_memory_artifact_routing_models_smoke() -> None:
    entry = MediaMemoryArtifactRoutingEntry(
        media_artifact_id="media_artifact_project_stl",
        media_artifact_ref="artifact://engineering/stl/part_001.stl",
        storage_registry_id="storage_registry_artifact_collection",
        route_request_id="payload_req_003",
        route_target="data_plane",
        route_binding_required=True,
        route_binding_ready=True,
        dashboard_visible=True,
    )

    assert entry.route_binding_required is True
    assert entry.route_binding_ready is True
