from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_snapshot_contract import (
    OperatorDashboardVisibleSnapshotEntry,
    build_operator_dashboard_visible_snapshot_contract,
)


def test_operator_dashboard_visible_snapshot_contract_builds() -> None:
    """Operator dashboard visible-snapshot contract should build successfully."""
    contract = build_operator_dashboard_visible_snapshot_contract()

    assert contract.contract_id == "operator_dashboard_visible_snapshot_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_visible_snapshot_contract_contains_expected_entry() -> None:
    """Operator dashboard visible-snapshot contract should contain expected canonical entry."""
    contract = build_operator_dashboard_visible_snapshot_contract()
    entry = contract.entries[0]

    assert entry.visible_snapshot_id == "operator_dashboard_visible_snapshot_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.visible_snapshot_state == "visible_snapshot_ready"
    assert entry.visible_snapshot_class == "main_operator_visible_snapshot"
    assert entry.screen_state_ready is True
    assert entry.render_handoff_ready is True
    assert entry.operator_visible is True


def test_operator_dashboard_visible_snapshot_entry_rejects_not_ready_handoff() -> None:
    """Visible snapshot entries must remain render-handoff-ready."""
    with pytest.raises(ValueError, match="render_handoff_ready must remain true"):
        OperatorDashboardVisibleSnapshotEntry(
            visible_snapshot_id="operator_dashboard_visible_snapshot_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            visible_snapshot_state="visible_snapshot_ready",
            visible_snapshot_class="main_operator_visible_snapshot",
            screen_state_ready=True,
            render_handoff_ready=False,
            operator_visible=True,
            description="Invalid visible snapshot entry.",
        )
