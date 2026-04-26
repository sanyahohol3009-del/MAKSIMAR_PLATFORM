from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_models import (
    MainOperatorDashboardContract,
    MainOperatorDashboardEntry,
)


def test_main_operator_dashboard_entry_smoke() -> None:
    entry = MainOperatorDashboardEntry(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        read_only_foundation_reuse=True,
        creates_second_root=False,
        description="Dashboard description.",
    )

    assert entry.dashboard_id == "main_operator_dashboard"


def test_main_operator_dashboard_entry_rejects_second_root() -> None:
    with pytest.raises(ValueError, match="creates_second_root must be False"):
        MainOperatorDashboardEntry(
            dashboard_id="main_operator_dashboard",
            dashboard_role="main_operator",
            primary_workspace_id="workspace_operator_interaction",
            secondary_workspace_ids=("workspace_foundation_monitoring",),
            read_only_foundation_reuse=True,
            creates_second_root=True,
            description="Dashboard description.",
        )


def test_main_operator_dashboard_contract_rejects_duplicates() -> None:
    entry_a = MainOperatorDashboardEntry(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        read_only_foundation_reuse=True,
        creates_second_root=False,
        description="A",
    )
    entry_b = MainOperatorDashboardEntry(
        dashboard_id="main_operator_dashboard",
        dashboard_role="main_operator",
        primary_workspace_id="workspace_operator_interaction",
        secondary_workspace_ids=("workspace_foundation_monitoring",),
        read_only_foundation_reuse=True,
        creates_second_root=False,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate dashboard_id detected"):
        MainOperatorDashboardContract(entries=(entry_a, entry_b))
