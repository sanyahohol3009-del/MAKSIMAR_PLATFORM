from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_routing_binding_preview,
)


def test_media_memory_artifact_routing_preview_smoke() -> None:
    preview = build_media_memory_artifact_routing_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["binding_ready"] is True
    assert preview["route_required_entries"] >= 1
    assert preview["route_ready_entries"] == preview["route_required_entries"]
    assert preview["flow"] == (
        "media_memory_read_model",
        "storage_registry_binding",
        "artifact_routing_binding",
        "data_plane_route_reference",
        "dashboard_read_only_preview",
    )
