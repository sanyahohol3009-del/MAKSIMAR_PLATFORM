from __future__ import annotations

from MAKSIMAR_CORE_LIB.distributed_workload_placement import (
    build_distributed_workload_placement_contract,
)


def test_distributed_workload_placement_contract_builds() -> None:
    """Distributed workload placement contract should build successfully."""
    contract = build_distributed_workload_placement_contract()

    assert contract.total_entries == 3
    assert contract.heavy_execution_entries == 1
    assert contract.control_plane_entries == 1
    assert contract.mobile_proxy_entries == 1
    assert contract.placed_entries == 3


def test_distributed_workload_placement_contract_contains_expected_control_entry() -> None:
    """Distributed workload placement should expose expected control entry."""
    contract = build_distributed_workload_placement_contract()
    entry = contract.entries[0]

    assert entry.placement_entry_id == "placement_control_plane_001"
    assert entry.workload_class == "control_plane_workload"
    assert entry.target_node_id == "dev_001"
    assert entry.linked_topology_entry_id == "nodetopology_dev_001"
    assert entry.linked_health_entry_id == "nodehealth_dev_001"


def test_distributed_workload_placement_contract_contains_expected_heavy_entry() -> None:
    """Distributed workload placement should expose expected heavy entry."""
    contract = build_distributed_workload_placement_contract()
    entry = contract.entries[1]

    assert entry.placement_entry_id == "placement_heavy_execution_001"
    assert entry.workload_class == "heavy_execution_workload"
    assert entry.target_node_id == "home_001"
    assert entry.linked_topology_entry_id == "nodetopology_home_001"
    assert entry.linked_health_entry_id == "nodehealth_home_001"


def test_distributed_workload_placement_contract_contains_expected_mobile_entry() -> None:
    """Distributed workload placement should expose expected mobile entry."""
    contract = build_distributed_workload_placement_contract()
    entry = contract.entries[2]

    assert entry.placement_entry_id == "placement_mobile_entry_001"
    assert entry.workload_class == "mobile_entry_workload"
    assert entry.target_node_id == "mobile_001"
    assert entry.linked_topology_entry_id == "nodetopology_mobile_001"
    assert entry.linked_health_entry_id == "nodehealth_mobile_001"
