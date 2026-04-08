from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_state_contract import (
    OperatorDashboardVisibleStateEntry,
    build_operator_dashboard_visible_state_contract,
)


def test_operator_dashboard_visible_state_contract_builds() -> None:
    """Operator dashboard visible-state contract should build successfully."""
    contract = build_operator_dashboard_visible_state_contract()

    assert contract.contract_id == "operator_dashboard_visible_state_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_visible_state_contract_contains_expected_entry() -> None:
    """Operator dashboard visible-state contract should contain expected canonical entry."""
    contract = build_operator_dashboard_visible_state_contract()
    entry = contract.entries[0]

    assert entry.visible_state_id == "operator_dashboard_visible_state_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.visible_dashboard_state == "dashboard_visible_ready"
    assert entry.visible_dashboard_class == "main_operator_visible_dashboard"
    assert entry.bundle_ready is True
    assert entry.presentation_entries == 3
    assert entry.operator_visible is True


def test_operator_dashboard_visible_state_entry_rejects_bundle_not_ready() -> None:
    """Operator dashboard visible-state entries must remain bundle-ready."""
    with pytest.raises(ValueError, match="bundle_ready must remain true"):
        OperatorDashboardVisibleStateEntry(
            visible_state_id="operator_dashboard_visible_state_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            visible_dashboard_state="dashboard_visible_ready",
            visible_dashboard_class="main_operator_visible_dashboard",
            bundle_ready=False,
            presentation_entries=3,
            operator_visible=True,
            description="Invalid operator dashboard visible-state entry.",
        )
