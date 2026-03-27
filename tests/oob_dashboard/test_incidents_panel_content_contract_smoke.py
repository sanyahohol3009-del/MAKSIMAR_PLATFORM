from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_incidents_panel_content_contract,
)


def test_incidents_panel_content_contract_builds() -> None:
    """Incidents panel content contract should build successfully."""
    contract = build_incidents_panel_content_contract()

    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.main_dashboard_visible_entries == 1
    assert contract.oob_visible_entries == 1


def test_incidents_panel_content_entry() -> None:
    """Incidents panel content entry should remain canonical."""
    contract = build_incidents_panel_content_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_incidents_001"
    assert entry.total_incident_entries == 4
    assert entry.visible_in_main_dashboard is True
    assert entry.visible_in_oob_dashboard is True
    assert entry.read_only is True
