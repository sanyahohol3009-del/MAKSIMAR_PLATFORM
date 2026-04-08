from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visible_output_contract import (
    OperatorDashboardVisibleOutputEntry,
    build_operator_dashboard_visible_output_contract,
)


def test_operator_dashboard_visible_output_contract_builds() -> None:
    """Operator dashboard visible-output contract should build successfully."""
    contract = build_operator_dashboard_visible_output_contract()

    assert contract.contract_id == "operator_dashboard_visible_output_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_visible_output_contract_contains_expected_entry() -> None:
    """Operator dashboard visible-output contract should contain expected canonical entry."""
    contract = build_operator_dashboard_visible_output_contract()
    entry = contract.entries[0]

    assert entry.visible_output_id == "operator_dashboard_visible_output_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.visible_output_state == "visible_output_ready"
    assert entry.visible_output_class == "main_operator_visible_output"
    assert entry.honest_view_ready is True
    assert entry.render_handoff_ready is True
    assert entry.operator_visible is True


def test_operator_dashboard_visible_output_entry_rejects_not_ready_honest_view() -> None:
    """Visible output entries must remain honest-view-ready."""
    with pytest.raises(ValueError, match="honest_view_ready must remain true"):
        OperatorDashboardVisibleOutputEntry(
            visible_output_id="operator_dashboard_visible_output_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            visible_output_state="visible_output_ready",
            visible_output_class="main_operator_visible_output",
            honest_view_ready=False,
            render_handoff_ready=True,
            operator_visible=True,
            description="Invalid visible output entry.",
        )
