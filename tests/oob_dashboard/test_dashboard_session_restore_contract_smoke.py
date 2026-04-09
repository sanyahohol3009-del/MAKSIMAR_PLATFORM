from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_session_restore_contract import (
    DashboardSessionRestoreEntry,
    build_dashboard_session_restore_contract,
)


def test_dashboard_session_restore_contract_builds() -> None:
    contract = build_dashboard_session_restore_contract()

    assert contract.contract_id == "dashboard_session_restore_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_dashboard_session_restore_contract_contains_expected_entry() -> None:
    contract = build_dashboard_session_restore_contract()
    entry = contract.entries[0]

    assert entry.dashboard_session_restore_id == "dashboard_session_restore_001"
    assert entry.workspace_id == "workspace_foundation_monitoring"
    assert entry.dashboard_session_restore_state == "dashboard_session_restore_ready"
    assert entry.dashboard_session_restore_class == "dashboard_session_restore"
    assert entry.workspace_restore_ready is True
    assert entry.display_restore_continuity_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True


def test_dashboard_session_restore_entry_rejects_non_workspace_restore_ready() -> None:
    with pytest.raises(ValueError, match="workspace_restore_ready must remain true"):
        DashboardSessionRestoreEntry(
            dashboard_session_restore_id="invalid_dashboard_session_restore",
            workspace_id="workspace_foundation_monitoring",
            dashboard_session_restore_state="dashboard_session_restore_ready",
            dashboard_session_restore_class="dashboard_session_restore",
            workspace_restore_ready=False,
            display_restore_continuity_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid dashboard session restore entry.",
        )


def test_dashboard_session_restore_entry_rejects_non_display_restore_continuity_ready() -> None:
    with pytest.raises(
        ValueError,
        match="display_restore_continuity_ready must remain true",
    ):
        DashboardSessionRestoreEntry(
            dashboard_session_restore_id="invalid_dashboard_session_restore",
            workspace_id="workspace_foundation_monitoring",
            dashboard_session_restore_state="dashboard_session_restore_ready",
            dashboard_session_restore_class="dashboard_session_restore",
            workspace_restore_ready=True,
            display_restore_continuity_ready=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid dashboard session restore entry.",
        )


def test_dashboard_session_restore_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        DashboardSessionRestoreEntry(
            dashboard_session_restore_id="invalid_dashboard_session_restore",
            workspace_id="workspace_foundation_monitoring",
            dashboard_session_restore_state="dashboard_session_restore_ready",
            dashboard_session_restore_class="dashboard_session_restore",
            workspace_restore_ready=True,
            display_restore_continuity_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid dashboard session restore entry.",
        )
