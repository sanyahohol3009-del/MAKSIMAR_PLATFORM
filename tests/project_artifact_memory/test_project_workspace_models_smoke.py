from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_project_workspace_contract


def test_project_workspace_models_smoke() -> None:
    contract = build_project_workspace_contract()

    assert contract.total_workspaces == 3
    assert contract.ready_workspaces == contract.total_workspaces
    assert contract.source_bound_workspaces == contract.total_workspaces
    assert contract.versioned_workspaces == contract.total_workspaces
    assert contract.read_only_workspaces == contract.total_workspaces
    assert contract.runtime_write_allowed_workspaces == 0
    assert contract.dashboard_visible_workspaces == contract.total_workspaces
