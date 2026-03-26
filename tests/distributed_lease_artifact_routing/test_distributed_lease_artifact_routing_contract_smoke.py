from __future__ import annotations

from MAKSIMAR_CORE_LIB.distributed_lease_artifact_routing import (
    build_distributed_lease_artifact_routing_contract,
)


def test_distributed_lease_artifact_routing_contract_builds() -> None:
    """Distributed lease artifact routing contract should build successfully."""
    contract = build_distributed_lease_artifact_routing_contract()

    assert contract.total_entries == 3
    assert contract.local_route_entries == 2
    assert contract.cross_node_route_entries == 1
    assert contract.approval_required_entries == 1
    assert contract.routed_entries == 3


def test_distributed_lease_artifact_routing_contract_contains_expected_control_entry() -> None:
    """Lease artifact routing should expose expected control entry."""
    contract = build_distributed_lease_artifact_routing_contract()
    entry = contract.entries[0]

    assert entry.lease_routing_entry_id == "leaseartifact_control_plane_001"
    assert entry.artifact_class == "control_contract_artifact"
    assert entry.lease_owner_node_id == "dev_001"
    assert entry.target_node_id == "dev_001"
    assert entry.routing_mode == "local_authoritative_route"


def test_distributed_lease_artifact_routing_contract_contains_expected_heavy_entry() -> None:
    """Lease artifact routing should expose expected heavy entry."""
    contract = build_distributed_lease_artifact_routing_contract()
    entry = contract.entries[1]

    assert entry.lease_routing_entry_id == "leaseartifact_heavy_execution_001"
    assert entry.artifact_class == "heavy_execution_artifact"
    assert entry.lease_owner_node_id == "dev_001"
    assert entry.target_node_id == "home_001"
    assert entry.routing_mode == "cross_node_authoritative_route"
    assert entry.approval_required_before_route is True


def test_distributed_lease_artifact_routing_contract_contains_expected_mobile_entry() -> None:
    """Lease artifact routing should expose expected mobile entry."""
    contract = build_distributed_lease_artifact_routing_contract()
    entry = contract.entries[2]

    assert entry.lease_routing_entry_id == "leaseartifact_mobile_entry_001"
    assert entry.artifact_class == "mobile_request_artifact"
    assert entry.lease_owner_node_id == "mobile_001"
    assert entry.target_node_id == "mobile_001"
    assert entry.routing_mode == "local_authoritative_route"
