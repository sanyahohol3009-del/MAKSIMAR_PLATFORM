from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    StorageArtifactRoutingBindingEntry,
)


def test_storage_artifact_binding_models_smoke() -> None:
    entry = StorageArtifactRoutingBindingEntry(
        request_id="payload_req_003",
        route_target="data_plane",
        routing_status="bound_to_data_plane",
        artifact_ref="artifact://simulation/output_001",
        owner_task_id="task_art_001",
        storage_registry_id="storage_registry_artifact_collection",
        artifact_collection_id="artifact_collection_domain_artifacts",
        storage_binding_required=True,
        storage_binding_ready=True,
        data_plane_binding_ready=True,
        dashboard_visible=True,
    )

    assert entry.storage_binding_required is True
    assert entry.storage_binding_ready is True
