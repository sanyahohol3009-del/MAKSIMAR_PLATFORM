from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_panel_registry_contract,
)


def test_panel_registry_contract_builds() -> None:
    """Panel registry contract should build successfully."""
    contract = build_dashboard_panel_registry_contract()

    assert contract.total_panels == 7
    assert len(contract.panels) == 7
    assert contract.visible_in_sidebar_panels == 7


def test_panel_registry_contains_settings_and_gesture() -> None:
    """Panel registry should contain settings and gesture control panels."""
    contract = build_dashboard_panel_registry_contract()

    panel_ids = {panel.panel_id for panel in contract.panels}

    assert "panel_settings" in panel_ids
    assert "panel_gesture_control" in panel_ids


def test_panel_registry_consistency_entry_uses_canonical_metadata() -> None:
    """Consistency panel should expose canonical normalized metadata."""
    contract = build_dashboard_panel_registry_contract()
    panel = next(
        panel for panel in contract.panels if panel.panel_id == "panel_consistency"
    )

    assert panel.label == "Consistency"
    assert panel.category == "core"
    assert panel.panel_family == "read_only_monitoring"
    assert panel.panel_kind == "summary"
    assert panel.panel_role == "read_only_monitoring"


def test_panel_registry_gesture_entry_uses_canonical_metadata() -> None:
    """Gesture control panel should expose canonical normalized metadata."""
    contract = build_dashboard_panel_registry_contract()
    panel = next(
        panel for panel in contract.panels if panel.panel_id == "panel_gesture_control"
    )

    assert panel.label == "Gesture Control"
    assert panel.category == "control"
    assert panel.panel_family == "control"
    assert panel.panel_kind == "gesture"
    assert panel.panel_role == "control_surface"
