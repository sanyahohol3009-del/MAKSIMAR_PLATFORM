from __future__ import annotations

from MAKSIMAR_SERVER.RUNTIME.node_topology import (
    build_distributed_routing_contract,
)


def test_distributed_routing_contract_builds() -> None:
    """Distributed routing contract should build successfully."""
    contract = build_distributed_routing_contract()

    assert contract.total_lease_routes == 2
    assert contract.total_artifact_routes == 2
    assert len(contract.lease_routes) == 2
    assert len(contract.artifact_routes) == 2


def test_distributed_routing_contract_contains_expected_routes() -> None:
    """Distributed routing contract should expose expected route entries."""
    contract = build_distributed_routing_contract()

    assert contract.lease_routes[0].lease_id == "lease_001"
    assert contract.lease_routes[-1].lease_id == "lease_002"
    assert contract.artifact_routes[0].artifact_type == "simulation_output"
    assert contract.artifact_routes[-1].artifact_type == "runtime_log_bundle"


def test_distributed_routing_contract_uses_valid_statuses() -> None:
    """Distributed routing contract should use valid route statuses."""
    contract = build_distributed_routing_contract()

    valid_statuses = {"local_route", "remote_route", "degraded_route"}

    assert all(route.route_status in valid_statuses for route in contract.lease_routes)
    assert all(route.route_status in valid_statuses for route in contract.artifact_routes)
