from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_visible_state_contract import (
    DashboardVisibleStateContract,
    DashboardVisibleStateEntry,
    build_dashboard_visible_state_contract,
)


def test_dashboard_visible_state_contract_builds() -> None:
    """Dashboard visible state contract should build successfully."""
    contract = build_dashboard_visible_state_contract()

    assert contract.contract_id == "dashboard_visible_state_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_dashboard_visible_state_contract_contains_expected_entry() -> None:
    """Dashboard visible state contract should contain expected canonical entry."""
    contract = build_dashboard_visible_state_contract()
    entry = contract.entries[0]

    assert entry.dashboard_visible_state_id == "dashboard_visible_state_001"
    assert entry.dashboard_visible_state == "dashboard_visible_state_ready"
    assert (
        entry.dashboard_visible_state_class
        == "main_operator_dashboard_visible_state"
    )
    assert entry.preview_surface_ready is True
    assert entry.rollback_readiness_ready is True
    assert entry.workspace_restore_ready is True


def test_dashboard_visible_state_entry_rejects_non_truth_bound() -> None:
    """Dashboard visible state entry must remain truth-bound."""
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical dashboard visible state.",
    ):
        DashboardVisibleStateEntry(
            dashboard_visible_state_id="dashboard_visible_state_invalid",
            workspace_id="workspace_operator_main",
            dashboard_visible_state="dashboard_visible_state_ready",
            dashboard_visible_state_class="main_operator_dashboard_visible_state",
            preview_surface_ready=True,
            rollback_readiness_ready=True,
            workspace_restore_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid dashboard visible state entry.",
        )


def test_dashboard_visible_state_manual_contract_builds() -> None:
    """Dashboard visible state manual contract should build successfully."""
    entries = (
        DashboardVisibleStateEntry(
            dashboard_visible_state_id="dashboard_visible_state_001",
            workspace_id="workspace_operator_main",
            dashboard_visible_state="dashboard_visible_state_ready",
            dashboard_visible_state_class="main_operator_dashboard_visible_state",
            preview_surface_ready=True,
            rollback_readiness_ready=True,
            workspace_restore_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical dashboard visible state entry.",
        ),
    )

    contract = DashboardVisibleStateContract(
        contract_id="dashboard_visible_state_contract_001",
        total_entries=1,
        ready_entries=1,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1
    assert contract.ready_entries == 1
