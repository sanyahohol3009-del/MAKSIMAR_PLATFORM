from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_panel_registry_contract,
)


def test_panel_registry_contract_builds() -> None:
    """Panel registry contract should build successfully."""
    contract = build_dashboard_panel_registry_contract()

    assert contract.total_panels == 7
    assert len(contract.panels) == 7


def test_panel_registry_contains_settings_and_gesture() -> None:
    """Panel registry should contain settings and gesture control panels."""
    contract = build_dashboard_panel_registry_contract()

    panel_ids = {panel.panel_id for panel in contract.panels}

    assert "panel_settings" in panel_ids
    assert "panel_gesture_control" in panel_ids
