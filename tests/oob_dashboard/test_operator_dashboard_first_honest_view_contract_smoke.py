from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_honest_view_contract import (
    OperatorDashboardFirstHonestViewEntry,
    build_operator_dashboard_first_honest_view_contract,
)


def test_operator_dashboard_first_honest_view_contract_builds() -> None:
    """Operator dashboard first honest-view contract should build successfully."""
    contract = build_operator_dashboard_first_honest_view_contract()

    assert contract.contract_id == "operator_dashboard_first_honest_view_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_first_honest_view_contract_contains_expected_entry() -> None:
    """Operator dashboard first honest-view contract should contain expected canonical entry."""
    contract = build_operator_dashboard_first_honest_view_contract()
    entry = contract.entries[0]

    assert entry.honest_view_id == "operator_dashboard_first_honest_view_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.honest_view_state == "first_honest_view_ready"
    assert entry.honest_view_class == "main_operator_first_honest_view"
    assert entry.visible_snapshot_ready is True
    assert entry.foundation_view_bound is True
    assert entry.operator_visible is True


def test_operator_dashboard_first_honest_view_entry_rejects_unbound_foundation() -> None:
    """First honest-view entries must remain foundation-bound."""
    with pytest.raises(ValueError, match="foundation_view_bound must remain true"):
        OperatorDashboardFirstHonestViewEntry(
            honest_view_id="operator_dashboard_first_honest_view_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            honest_view_state="first_honest_view_ready",
            honest_view_class="main_operator_first_honest_view",
            visible_snapshot_ready=True,
            foundation_view_bound=False,
            operator_visible=True,
            description="Invalid first honest-view entry.",
        )
