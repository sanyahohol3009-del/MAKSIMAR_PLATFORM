from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_routing_binding_contract,
)


def test_storage_artifact_binding_data_plane_ready_smoke() -> None:
    contract = build_storage_artifact_routing_binding_contract()

    required_entries = tuple(
        entry for entry in contract.entries if entry.storage_binding_required
    )

    assert required_entries
    for entry in required_entries:
        assert entry.route_target == "data_plane"
        assert entry.artifact_ref
        assert entry.owner_task_id
        assert entry.storage_registry_id == "storage_registry_artifact_collection"
        assert entry.artifact_collection_id == "artifact_collection_domain_artifacts"
        assert entry.data_plane_binding_ready is True
