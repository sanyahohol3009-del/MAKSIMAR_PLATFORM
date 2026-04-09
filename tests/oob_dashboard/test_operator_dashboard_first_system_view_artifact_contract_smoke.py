from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_system_view_artifact_contract import (
    OperatorDashboardFirstSystemViewArtifactEntry,
    build_operator_dashboard_first_system_view_artifact_contract,
)


def test_operator_dashboard_first_system_view_artifact_contract_builds() -> None:
    contract = build_operator_dashboard_first_system_view_artifact_contract()

    assert contract.contract_id == (
        "operator_dashboard_first_system_view_artifact_contract_001"
    )
    assert contract.total_entries == 1
    assert contract.ready_entries == 1
    assert contract.operator_visible_entries == 1
    assert contract.truth_bound_entries == 1


def test_operator_dashboard_first_system_view_artifact_contract_contains_expected_entry() -> None:
    contract = build_operator_dashboard_first_system_view_artifact_contract()
    entry = contract.entries[0]

    assert entry.system_view_artifact_id == (
        "operator_dashboard_first_system_view_artifact_001"
    )
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.system_view_artifact_state == "system_view_artifact_ready"
    assert entry.system_view_artifact_class == "main_operator_system_view_artifact"
    assert entry.final_assembled_state_ready is True
    assert entry.operator_visible is True
    assert entry.truth_bound is True
    assert entry.read_only_boundary is True
    assert entry.oob_safe is True


def test_operator_dashboard_first_system_view_artifact_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(ValueError, match="truth_bound must remain true"):
        OperatorDashboardFirstSystemViewArtifactEntry(
            system_view_artifact_id="invalid_system_view_artifact",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            system_view_artifact_state="system_view_artifact_ready",
            system_view_artifact_class="main_operator_system_view_artifact",
            final_assembled_state_ready=True,
            operator_visible=True,
            truth_bound=False,
            read_only_boundary=True,
            oob_safe=True,
            description="Invalid system-view artifact entry.",
        )


def test_operator_dashboard_first_system_view_artifact_entry_rejects_non_read_only_boundary() -> None:
    with pytest.raises(ValueError, match="read_only_boundary must remain true"):
        OperatorDashboardFirstSystemViewArtifactEntry(
            system_view_artifact_id="invalid_system_view_artifact",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            system_view_artifact_state="system_view_artifact_ready",
            system_view_artifact_class="main_operator_system_view_artifact",
            final_assembled_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=False,
            oob_safe=True,
            description="Invalid system-view artifact entry.",
        )


def test_operator_dashboard_first_system_view_artifact_entry_rejects_non_oob_safe() -> None:
    with pytest.raises(ValueError, match="oob_safe must remain true"):
        OperatorDashboardFirstSystemViewArtifactEntry(
            system_view_artifact_id="invalid_system_view_artifact",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            system_view_artifact_state="system_view_artifact_ready",
            system_view_artifact_class="main_operator_system_view_artifact",
            final_assembled_state_ready=True,
            operator_visible=True,
            truth_bound=True,
            read_only_boundary=True,
            oob_safe=False,
            description="Invalid system-view artifact entry.",
        )
