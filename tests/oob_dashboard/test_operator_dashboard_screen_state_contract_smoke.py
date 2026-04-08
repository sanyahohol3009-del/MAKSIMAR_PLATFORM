from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_screen_state_contract import (
    OperatorDashboardScreenStateEntry,
    build_operator_dashboard_screen_state_contract,
)


def test_operator_dashboard_screen_state_contract_builds() -> None:
    """Operator dashboard screen-state contract should build successfully."""
    contract = build_operator_dashboard_screen_state_contract()

    assert contract.contract_id == "operator_dashboard_screen_state_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_screen_state_contract_contains_expected_entry() -> None:
    """Operator dashboard screen-state contract should contain expected canonical entry."""
    contract = build_operator_dashboard_screen_state_contract()
    entry = contract.entries[0]

    assert entry.screen_state_id == "operator_dashboard_screen_state_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.screen_state_status == "screen_state_ready"
    assert entry.screen_state_class == "main_operator_screen_state"
    assert entry.visible_state_ready is True
    assert entry.presentation_entries == 3
    assert entry.shared_surface_entries == 1
    assert entry.operator_visible is True


def test_operator_dashboard_screen_state_entry_rejects_not_ready_state() -> None:
    """Operator dashboard screen-state entries must remain visible-state-ready."""
    with pytest.raises(ValueError, match="visible_state_ready must remain true"):
        OperatorDashboardScreenStateEntry(
            screen_state_id="operator_dashboard_screen_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            screen_state_status="screen_state_ready",
            screen_state_class="main_operator_screen_state",
            visible_state_ready=False,
            presentation_entries=3,
            shared_surface_entries=1,
            operator_visible=True,
            description="Invalid operator dashboard screen-state entry.",
        )
