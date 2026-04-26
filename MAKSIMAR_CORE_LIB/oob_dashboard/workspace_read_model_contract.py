from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_models import (
    WorkspaceReadModelContract,
    WorkspaceReadRow,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def build_workspace_read_model_contract() -> WorkspaceReadModelContract:
    """Build the canonical workspace read-model contract."""
    registry = build_workspace_registry_contract()

    rows = tuple(
        WorkspaceReadRow(
            workspace_id=entry.workspace_id,
            workspace_role=entry.workspace_role,
            primary_display_target_id=entry.primary_display_target_id,
            panel_count=len(entry.included_panel_ids),
            panel_ids=entry.included_panel_ids,
            description=f"Read-model row for {entry.workspace_id}.",
        )
        for entry in registry.entries
    )

    return WorkspaceReadModelContract(rows=rows)
