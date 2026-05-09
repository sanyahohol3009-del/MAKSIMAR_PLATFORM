from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_routing_binding_contract,
)


def test_storage_artifact_binding_builder_smoke() -> None:
    contract = build_storage_artifact_routing_binding_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.storage_required_entries >= 1
    assert contract.storage_ready_entries == contract.storage_required_entries
    assert contract.data_plane_ready_entries == contract.storage_required_entries
    assert contract.binding_ready is True
