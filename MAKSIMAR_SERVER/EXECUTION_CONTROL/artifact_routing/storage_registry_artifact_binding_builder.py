from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_artifact_collection_reference,
    build_storage_registry_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.artifact_routing_binding import (
    build_artifact_routing_binding_contract,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.storage_registry_artifact_binding_models import (
    StorageArtifactRoutingBindingContract,
    StorageArtifactRoutingBindingEntry,
)


def _artifact_collection_storage_registry_id() -> str:
    storage_registry = build_storage_registry_contract()

    for entry in storage_registry.entries:
        if entry.entry_kind == "artifact_collection":
            return entry.registry_id

    raise ValueError("artifact_collection storage registry entry not found")


def build_storage_artifact_routing_binding_contract() -> StorageArtifactRoutingBindingContract:
    """Bind artifact routing to storage registry without writing data-plane state."""

    routing_contract = build_artifact_routing_binding_contract()
    artifact_collection = build_artifact_collection_reference()
    storage_registry_id = _artifact_collection_storage_registry_id()

    entries: list[StorageArtifactRoutingBindingEntry] = []

    for routing_entry in routing_contract.entries:
        storage_required = routing_entry.binding_status == "bound_to_data_plane"

        entries.append(
            StorageArtifactRoutingBindingEntry(
                request_id=routing_entry.request_id,
                route_target=str(routing_entry.route_target),
                routing_status=routing_entry.binding_status,
                artifact_ref=routing_entry.artifact_ref,
                owner_task_id=routing_entry.owner_task_id,
                storage_registry_id=storage_registry_id if storage_required else "",
                artifact_collection_id=(
                    artifact_collection.collection_id if storage_required else ""
                ),
                storage_binding_required=storage_required,
                storage_binding_ready=(
                    storage_required
                    and routing_entry.artifact_declared
                    and bool(routing_entry.artifact_ref)
                    and bool(routing_entry.owner_task_id)
                )
                or not storage_required,
                data_plane_binding_ready=(
                    storage_required and routing_entry.binding_status == "bound_to_data_plane"
                )
                or not storage_required,
                dashboard_visible=True,
            )
        )

    required_entries = tuple(entry for entry in entries if entry.storage_binding_required)

    return StorageArtifactRoutingBindingContract(
        total_entries=len(entries),
        storage_required_entries=len(required_entries),
        storage_ready_entries=sum(
            1
            for entry in required_entries
            if entry.storage_binding_ready
        ),
        data_plane_ready_entries=sum(
            1
            for entry in required_entries
            if entry.data_plane_binding_ready
        ),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        binding_ready=all(
            entry.storage_binding_ready and entry.data_plane_binding_ready
            for entry in required_entries
        ),
        entries=tuple(entries),
    )
