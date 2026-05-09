from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_routing_binding_contract,
)


def test_media_memory_artifact_routing_builder_smoke() -> None:
    contract = build_media_memory_artifact_routing_binding_contract()

    assert contract.total_entries == len(contract.entries)
    assert contract.route_required_entries >= 1
    assert contract.route_ready_entries == contract.route_required_entries
    assert contract.dashboard_visible_entries == contract.total_entries
    assert contract.binding_ready is True
