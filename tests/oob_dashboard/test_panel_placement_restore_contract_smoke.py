from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (
    PanelPlacementRestoreEntry,
    build_panel_placement_restore_contract,
)


def test_panel_placement_restore_contract_builds() -> None:
    contract = build_panel_placement_restore_contract()

    assert contract.contract_id == "panel_placement_restore_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_panel_placement_restore_contract_contains_expected_entry() -> None:
    contract = build_panel_placement_restore_contract()
    entry = contract.entries[0]

    assert entry.panel_placement_restore_id == "panel_placement_restore_001"
    assert entry.workspace_id == "workspace_foundation_monitoring"
    assert entry.panel_placement_restore_state == "panel_placement_restore_ready"
    assert entry.panel_placement_restore_class == "dashboard_panel_placement_restore"
    assert entry.dashboard_session_restore_ready is True
    assert entry.display_assignment_restore_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True


def test_panel_placement_restore_entry_rejects_non_dashboard_session_restore_ready() -> None:
    with pytest.raises(
        ValueError,
        match="dashboard_session_restore_ready must remain true",
    ):
        PanelPlacementRestoreEntry(
            panel_placement_restore_id="invalid_panel_placement_restore",
            workspace_id="workspace_foundation_monitoring",
            panel_placement_restore_state="panel_placement_restore_ready",
            panel_placement_restore_class="dashboard_panel_placement_restore",
            dashboard_session_restore_ready=False,
            display_assignment_restore_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid panel placement restore entry.",
        )


def test_panel_placement_restore_entry_rejects_non_display_assignment_restore_ready() -> None:
    with pytest.raises(
        ValueError,
        match="display_assignment_restore_ready must remain true",
    ):
        PanelPlacementRestoreEntry(
            panel_placement_restore_id="invalid_panel_placement_restore",
            workspace_id="workspace_foundation_monitoring",
            panel_placement_restore_state="panel_placement_restore_ready",
            panel_placement_restore_class="dashboard_panel_placement_restore",
            dashboard_session_restore_ready=True,
            display_assignment_restore_ready=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid panel placement restore entry.",
        )


def test_panel_placement_restore_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        PanelPlacementRestoreEntry(
            panel_placement_restore_id="invalid_panel_placement_restore",
            workspace_id="workspace_foundation_monitoring",
            panel_placement_restore_state="panel_placement_restore_ready",
            panel_placement_restore_class="dashboard_panel_placement_restore",
            dashboard_session_restore_ready=True,
            display_assignment_restore_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid panel placement restore entry.",
        )
