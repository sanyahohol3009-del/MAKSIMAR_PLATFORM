from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_node_topology_panel_contract,
)


def test_node_topology_panel_contract_builds() -> None:
    """Node topology panel contract should build successfully."""
    contract = build_node_topology_panel_contract()

    assert contract.panel_id == "panel_node_topology"
    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_node_topology_panel_contains_mobile_and_home_nodes() -> None:
    """Node topology panel should expose mobile and home nodes."""
    contract = build_node_topology_panel_contract()

    node_ids = {entry.node_id for entry in contract.entries}

    assert "mobile_001" in node_ids
    assert "home_001" in node_ids
