from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_topology_runtime import (
    build_node_topology_runtime_contract,
)


def test_node_topology_runtime_contract_builds() -> None:
    """Node topology runtime contract should build successfully."""
    contract = build_node_topology_runtime_contract()

    assert contract.total_entries == 3
    assert contract.heavy_execution_entries == 1
    assert contract.control_plane_entries == 1
    assert contract.mobile_proxy_entries == 1
    assert contract.wrist_linked_entries == 1
    assert contract.defined_entries == 3


def test_node_topology_runtime_contract_contains_expected_dev_entry() -> None:
    """Node topology runtime should expose expected DEV entry."""
    contract = build_node_topology_runtime_contract()
    entry = contract.entries[0]

    assert entry.topology_entry_id == "nodetopology_dev_001"
    assert entry.node_id == "dev_001"
    assert entry.node_role == "DEV_NODE"
    assert entry.runtime_connectivity_mode == "orchestration_and_validation"
    assert entry.heavy_execution_allowed is False
    assert entry.control_plane_allowed is True


def test_node_topology_runtime_contract_contains_expected_home_entry() -> None:
    """Node topology runtime should expose expected HOME entry."""
    contract = build_node_topology_runtime_contract()
    entry = contract.entries[1]

    assert entry.topology_entry_id == "nodetopology_home_001"
    assert entry.node_id == "home_001"
    assert entry.node_role == "HOME_NODE"
    assert entry.runtime_connectivity_mode == "heavy_compute_execution"
    assert entry.heavy_execution_allowed is True
    assert entry.control_plane_allowed is False


def test_node_topology_runtime_contract_contains_expected_mobile_entry() -> None:
    """Node topology runtime should expose expected MOBILE entry."""
    contract = build_node_topology_runtime_contract()
    entry = contract.entries[2]

    assert entry.topology_entry_id == "nodetopology_mobile_001"
    assert entry.node_id == "mobile_001"
    assert entry.node_role == "MOBILE_NODE"
    assert entry.runtime_connectivity_mode == "mobile_entry_and_proxy"
    assert entry.mobile_proxy_allowed is True
    assert entry.wrist_terminal_linked is True
    assert entry.linked_wrist_terminal_id == "wrist_terminal_core_001"
