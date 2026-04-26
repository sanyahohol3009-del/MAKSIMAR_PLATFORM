from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_models import (
    OperatorWorkspaceBindingContract,
    OperatorWorkspaceBindingEntry,
)


def test_operator_workspace_binding_entry_smoke() -> None:
    entry = OperatorWorkspaceBindingEntry(
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_interaction",
        binding_role="primary_operator_workspace",
        workspace_order=0,
        is_primary_workspace=True,
        read_only_binding=True,
        description="Binding description.",
    )

    assert entry.dashboard_id == "main_operator_dashboard"


def test_operator_workspace_binding_entry_rejects_non_read_only() -> None:
    with pytest.raises(ValueError, match="read_only_binding must be True"):
        OperatorWorkspaceBindingEntry(
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_interaction",
            binding_role="primary_operator_workspace",
            workspace_order=0,
            is_primary_workspace=True,
            read_only_binding=False,
            description="Binding description.",
        )


def test_operator_workspace_binding_contract_rejects_invalid_primary_count() -> None:
    entry_a = OperatorWorkspaceBindingEntry(
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_interaction",
        binding_role="secondary_foundation_workspace",
        workspace_order=0,
        is_primary_workspace=False,
        read_only_binding=True,
        description="A",
    )
    entry_b = OperatorWorkspaceBindingEntry(
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_foundation_monitoring",
        binding_role="secondary_foundation_workspace",
        workspace_order=1,
        is_primary_workspace=False,
        read_only_binding=True,
        description="B",
    )

    with pytest.raises(ValueError, match="exactly one primary workspace must be defined"):
        OperatorWorkspaceBindingContract(entries=(entry_a, entry_b))
