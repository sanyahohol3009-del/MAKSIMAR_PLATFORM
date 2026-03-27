from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_topology_panel_content_contract,
)


def test_topology_panel_content_contract_builds() -> None:
    """Topology panel content contract should build successfully."""
    contract = build_topology_panel_content_contract()

    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1


def test_topology_panel_content_entry() -> None:
    """Topology panel content entry should remain canonical."""
    contract = build_topology_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_topology_001"
    assert entry.total_topology_entries == 3
    assert entry.mobile_nodes == 1
    assert entry.home_nodes == 1
    assert entry.operator_visible_entries == 3
    assert entry.topology_panel_status == "topology_visible"
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
