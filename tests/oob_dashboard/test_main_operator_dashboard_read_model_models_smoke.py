from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_models import (
    MainOperatorDashboardReadModelContract,
    MainOperatorDashboardReadRow,
)


def test_main_operator_dashboard_read_row_smoke() -> None:
    row = MainOperatorDashboardReadRow(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        total_workspace_count=2,
        total_panel_count=8,
        read_only_foundation_reuse=True,
        supports_multimonitor_layout=True,
        supports_voice_gesture_addressing=True,
        description="Read-model description.",
    )

    assert row.dashboard_id == "main_operator_dashboard"


def test_main_operator_dashboard_read_row_rejects_disabled_multimonitor() -> None:
    with pytest.raises(ValueError, match="supports_multimonitor_layout must be True"):
        MainOperatorDashboardReadRow(
            dashboard_id="main_operator_dashboard",
            dashboard_role="main_operator",
            primary_workspace_id="workspace_operator_interaction",
            secondary_workspace_ids=("workspace_foundation_monitoring",),
            total_workspace_count=2,
            total_panel_count=8,
            read_only_foundation_reuse=True,
            supports_multimonitor_layout=False,
            supports_voice_gesture_addressing=True,
            description="Read-model description.",
        )


def test_main_operator_dashboard_read_model_contract_rejects_duplicates() -> None:
    row_a = MainOperatorDashboardReadRow(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        total_workspace_count=2,
        total_panel_count=8,
        read_only_foundation_reuse=True,
        supports_multimonitor_layout=True,
        supports_voice_gesture_addressing=True,
        description="A",
    )
    row_b = MainOperatorDashboardReadRow(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        total_workspace_count=2,
        total_panel_count=8,
        read_only_foundation_reuse=True,
        supports_multimonitor_layout=True,
        supports_voice_gesture_addressing=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate dashboard_id detected"):
        MainOperatorDashboardReadModelContract(rows=(row_a, row_b))
