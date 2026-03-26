from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_artifact_routing_binding_contract,
)


def test_artifact_routing_binding_contract_builds() -> None:
    """Artifact routing binding contract should build successfully."""
    contract = build_artifact_routing_binding_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_artifact_routing_binding_contract_keeps_control_payload_inline() -> None:
    """Control-plane payloads should remain inline."""
    contract = build_artifact_routing_binding_contract()

    first = contract.entries[0]

    assert first.request_id == "payload_req_001"
    assert first.route_target == "control_plane"
    assert first.binding_status == "inline_control_route"
    assert first.artifact_declared is False


def test_artifact_routing_binding_contract_binds_heavy_artifact_to_data_plane() -> None:
    """Heavy artifact should be bound to data plane by artifact reference."""
    contract = build_artifact_routing_binding_contract()

    heavy = contract.entries[2]

    assert heavy.request_id == "payload_req_003"
    assert heavy.detected_payload_class == "heavy_artifact"
    assert heavy.route_target == "data_plane"
    assert heavy.binding_status == "bound_to_data_plane"
    assert heavy.artifact_declared is True
    assert heavy.artifact_ref == "artifact://simulation/output_001"
    assert heavy.owner_task_id == "task_art_001"
