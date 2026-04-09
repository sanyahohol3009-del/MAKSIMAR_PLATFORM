from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_visual_shell_ready_contract import (
    OperatorDashboardVisualShellReadyEntry,
    build_operator_dashboard_visual_shell_ready_contract,
)


def test_operator_dashboard_visual_shell_ready_contract_builds() -> None:
    contract = build_operator_dashboard_visual_shell_ready_contract()

    assert contract.contract_id == "operator_dashboard_visual_shell_ready_contract_001"
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.shell_bound_entries == 1


def test_operator_dashboard_visual_shell_ready_contract_contains_expected_entry() -> None:
    contract = build_operator_dashboard_visual_shell_ready_contract()
    entry = contract.entries[0]

    assert entry.visual_shell_ready_id == "operator_dashboard_visual_shell_ready_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.visual_shell_ready_state == "visual_shell_ready"
    assert entry.visual_shell_ready_class == "main_operator_visual_shell_ready"
    assert entry.operator_surface_export_ready is True
    assert entry.visual_shell_bound is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True
    assert entry.read_only_boundary is True
    assert entry.oob_safe is True


def test_operator_dashboard_visual_shell_ready_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        OperatorDashboardVisualShellReadyEntry(
            visual_shell_ready_id="invalid_visual_shell_ready",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            visual_shell_ready_state="visual_shell_ready",
            visual_shell_ready_class="main_operator_visual_shell_ready",
            operator_surface_export_ready=True,
            visual_shell_bound=True,
            operator_visible=True,
            truth_bound=False,
            read_only_boundary=True,
            oob_safe=True,
            description="Invalid visual-shell-ready entry.",
        )


def test_operator_dashboard_visual_shell_ready_entry_rejects_non_read_only_boundary() -> None:
    with pytest.raises(ValueError, match="read_only_boundary must remain true"):
        OperatorDashboardVisualShellReadyEntry(
            visual_shell_ready_id="invalid_visual_shell_ready",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            visual_shell_ready_state="visual_shell_ready",
            visual_shell_ready_class="main_operator_visual_shell_ready",
            operator_surface_export_ready=True,
            visual_shell_bound=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=False,
            oob_safe=True,
            description="Invalid visual-shell-ready entry.",
        )


def test_operator_dashboard_visual_shell_ready_entry_rejects_non_shell_bound() -> None:
    with pytest.raises(ValueError, match="visual_shell_bound must remain true"):
        OperatorDashboardVisualShellReadyEntry(
            visual_shell_ready_id="invalid_visual_shell_ready",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            visual_shell_ready_state="visual_shell_ready",
            visual_shell_ready_class="main_operator_visual_shell_ready",
            operator_surface_export_ready=True,
            visual_shell_bound=False,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=True,
            description="Invalid visual-shell-ready entry.",
        )
