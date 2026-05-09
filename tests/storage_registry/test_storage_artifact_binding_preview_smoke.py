from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_routing_binding_preview,
)


def test_storage_artifact_binding_preview_smoke() -> None:
    preview = build_storage_artifact_routing_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["binding_ready"] is True
    assert preview["total_entries"] == len(preview["entries"])
    assert preview["flow"] == (
        "payload_classification",
        "artifact_routing",
        "storage_registry_lookup",
        "artifact_collection_binding",
        "data_plane_route_readiness",
        "dashboard_read_only_preview",
    )
