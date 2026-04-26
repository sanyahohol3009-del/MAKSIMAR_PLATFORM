from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_models import (
    WorkspaceReadModelContract,
    WorkspaceReadRow,
)


def test_workspace_read_row_smoke() -> None:
    row = WorkspaceReadRow(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        panel_count=1,
        panel_ids=("system_status",),
        description="Workspace row description.",
    )

    assert row.workspace_id == "workspace_foundation_monitoring"


def test_workspace_read_row_rejects_mismatched_panel_count() -> None:
    with pytest.raises(ValueError, match="panel_count must match len\\(panel_ids\\)"):
        WorkspaceReadRow(
            workspace_id="workspace_foundation_monitoring",
            workspace_role="foundation_monitoring",
            primary_display_target_id="display_foundation_primary",
            panel_count=2,
            panel_ids=("system_status",),
            description="Workspace row description.",
        )


def test_workspace_read_model_contract_rejects_duplicates() -> None:
    row_a = WorkspaceReadRow(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        panel_count=1,
        panel_ids=("system_status",),
        description="A",
    )
    row_b = WorkspaceReadRow(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        panel_count=1,
        panel_ids=("guard_chain",),
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate workspace_id detected"):
        WorkspaceReadModelContract(rows=(row_a, row_b))
