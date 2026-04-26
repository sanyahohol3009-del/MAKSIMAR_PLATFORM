from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_contract import (
    build_node_topology_panel_contract,
)


def test_node_topology_panel_contract_builds() -> None:
    contract = build_node_topology_panel_contract()

    assert contract.panel_id == "panel_node_topology"
    assert contract.total_entries == 3
    assert contract.read_only_entries == 3
    assert contract.main_dashboard_visible_entries == 3
    assert contract.oob_visible_entries == 3
    assert contract.operator_visible is True


def test_node_topology_panel_contract_contains_expected_nodes() -> None:
    contract = build_node_topology_panel_contract()

    node_ids = tuple(entry.node_id for entry in contract.entries)
    role_types = tuple(entry.role_type for entry in contract.entries)

    assert node_ids == ("mobile_001", "dev_001", "home_001")
    assert role_types == ("mobile_node", "dev_node", "home_node")

    dev_entry = next(entry for entry in contract.entries if entry.node_id == "dev_001")
    assert dev_entry.security_root is True
    assert dev_entry.heavy_execution_allowed is True
    assert dev_entry.core_write_allowed is False
    assert dev_entry.operator_visible is True
