from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (
    WorkspaceRestoreEntry,
    build_workspace_restore_contract,
)


def test_workspace_restore_contract_builds() -> None:
    contract = build_workspace_restore_contract()

    assert contract.contract_id == "workspace_restore_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_workspace_restore_contract_contains_expected_entry() -> None:
    contract = build_workspace_restore_contract()
    entry = contract.entries[0]

    assert entry.workspace_restore_id == "workspace_restore_001"
    assert entry.workspace_id == "workspace_foundation_monitoring"
    assert entry.workspace_restore_state == "workspace_restore_ready"
    assert entry.workspace_restore_class == "dashboard_workspace_restore"
    assert entry.workspace_read_model_ready is True
    assert entry.display_assignment_restore_ready is True
    assert entry.display_restore_continuity_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True


def test_workspace_restore_entry_rejects_non_workspace_read_model_ready() -> None:
    with pytest.raises(ValueError, match="workspace_read_model_ready must remain true"):
        WorkspaceRestoreEntry(
            workspace_restore_id="invalid_workspace_restore",
            workspace_id="workspace_foundation_monitoring",
            workspace_restore_state="workspace_restore_ready",
            workspace_restore_class="dashboard_workspace_restore",
            workspace_read_model_ready=False,
            display_assignment_restore_ready=True,
            display_restore_continuity_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid workspace restore entry.",
        )


def test_workspace_restore_entry_rejects_non_display_assignment_restore_ready() -> None:
    with pytest.raises(
        ValueError,
        match="display_assignment_restore_ready must remain true",
    ):
        WorkspaceRestoreEntry(
            workspace_restore_id="invalid_workspace_restore",
            workspace_id="workspace_foundation_monitoring",
            workspace_restore_state="workspace_restore_ready",
            workspace_restore_class="dashboard_workspace_restore",
            workspace_read_model_ready=True,
            display_assignment_restore_ready=False,
            display_restore_continuity_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid workspace restore entry.",
        )


def test_workspace_restore_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        WorkspaceRestoreEntry(
            workspace_restore_id="invalid_workspace_restore",
            workspace_id="workspace_foundation_monitoring",
            workspace_restore_state="workspace_restore_ready",
            workspace_restore_class="dashboard_workspace_restore",
            workspace_read_model_ready=True,
            display_assignment_restore_ready=True,
            display_restore_continuity_ready=True,
            operator_visible=True,
            truth_bound=False,
            description="Invalid workspace restore entry.",
        )
