from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_real_picture_contract import (
    OperatorDashboardFirstRealPictureEntry,
    build_operator_dashboard_first_real_picture_contract,
)


def test_operator_dashboard_first_real_picture_contract_builds() -> None:
    """Operator dashboard first real-picture contract should build successfully."""
    contract = build_operator_dashboard_first_real_picture_contract()

    assert contract.contract_id == "operator_dashboard_first_real_picture_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1


def test_operator_dashboard_first_real_picture_contract_contains_expected_entry() -> None:
    """Operator dashboard first real-picture contract should contain expected canonical entry."""
    contract = build_operator_dashboard_first_real_picture_contract()
    entry = contract.entries[0]

    assert entry.first_real_picture_id == "operator_dashboard_first_real_picture_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.first_real_picture_state == "first_real_picture_ready"
    assert entry.first_real_picture_class == "main_operator_first_real_picture"
    assert entry.visible_output_ready is True
    assert entry.hud_screen_bound is True
    assert entry.operator_visible is True


def test_operator_dashboard_first_real_picture_entry_rejects_unbound_hud_screen() -> None:
    """First real-picture entries must remain HUD-screen-bound."""
    with pytest.raises(ValueError, match="hud_screen_bound must remain true"):
        OperatorDashboardFirstRealPictureEntry(
            first_real_picture_id="operator_dashboard_first_real_picture_invalid",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            first_real_picture_state="first_real_picture_ready",
            first_real_picture_class="main_operator_first_real_picture",
            visible_output_ready=True,
            hud_screen_bound=False,
            operator_visible=True,
            description="Invalid first real picture entry.",
        )
