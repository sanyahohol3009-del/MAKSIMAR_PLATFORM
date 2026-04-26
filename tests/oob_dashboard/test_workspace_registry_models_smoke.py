from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_models import (
    WorkspaceRegistryContract,
    WorkspaceRegistryEntry,
)


def test_workspace_registry_entry_smoke() -> None:
    entry = WorkspaceRegistryEntry(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        included_panel_ids=("system_status",),
        description="Workspace description.",
    )

    assert entry.workspace_id == "workspace_foundation_monitoring"


def test_workspace_registry_contract_rejects_duplicates() -> None:
    entry_a = WorkspaceRegistryEntry(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        included_panel_ids=("system_status",),
        description="A",
    )
    entry_b = WorkspaceRegistryEntry(
        workspace_id="workspace_foundation_monitoring",
        workspace_role="foundation_monitoring",
        primary_display_target_id="display_foundation_primary",
        included_panel_ids=("guard_chain",),
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate workspace_id detected"):
        WorkspaceRegistryContract(entries=(entry_a, entry_b))
