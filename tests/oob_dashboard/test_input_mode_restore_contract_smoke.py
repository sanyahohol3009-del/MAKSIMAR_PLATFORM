from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.input_mode_restore_contract import (
    InputModeRestoreEntry,
    build_input_mode_restore_contract,
)


def test_input_mode_restore_contract_builds() -> None:
    contract = build_input_mode_restore_contract()

    assert contract.contract_id == "input_mode_restore_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_input_mode_restore_contract_contains_expected_entry() -> None:
    contract = build_input_mode_restore_contract()
    entry = contract.entries[0]

    assert entry.input_mode_restore_id == "input_mode_restore_001"
    assert entry.workspace_id == "workspace_foundation_monitoring"
    assert entry.input_mode_restore_state == "input_mode_restore_ready"
    assert entry.input_mode_restore_class == "dashboard_input_mode_restore"
    assert entry.restored_input_mode == "operator_interaction_mode"
    assert entry.dashboard_session_restore_ready is True
    assert entry.panel_placement_restore_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True


def test_input_mode_restore_entry_rejects_non_dashboard_session_restore_ready() -> None:
    with pytest.raises(
        ValueError,
        match="dashboard_session_restore_ready must remain true",
    ):
        InputModeRestoreEntry(
            input_mode_restore_id="invalid_input_mode_restore",
            workspace_id="workspace_foundation_monitoring",
            input_mode_restore_state="input_mode_restore_ready",
            input_mode_restore_class="dashboard_input_mode_restore",
            restored_input_mode="operator_interaction_mode",
            dashboard_session_restore_ready=False,
            panel_placement_restore_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid input-mode restore entry.",
        )


def test_input_mode_restore_entry_rejects_non_panel_placement_restore_ready() -> None:
    with pytest.raises(
        ValueError,
        match="panel_placement_restore_ready must remain true",
    ):
        InputModeRestoreEntry(
            input_mode_restore_id="invalid_input_mode_restore",
            workspace_id="workspace_foundation_monitoring",
            input_mode_restore_state="input_mode_restore_ready",
            input_mode_restore_class="dashboard_input_mode_restore",
            restored_input_mode="operator_interaction_mode",
            dashboard_session_restore_ready=True,
            panel_placement_restore_ready=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid input-mode restore entry.",
        )


def test_input_mode_restore_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        InputModeRestoreEntry(
            input_mode_restore_id="invalid_input_mode_restore",
            workspace_id="workspace_foundation_monitoring",
            input_mode_restore_state="input_mode_restore_ready",
            input_mode_restore_class="dashboard_input_mode_restore",
            restored_input_mode="operator_interaction_mode",
            dashboard_session_restore_ready=True,
            panel_placement_restore_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid input-mode restore entry.",
        )
