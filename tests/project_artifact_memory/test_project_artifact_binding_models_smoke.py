from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_project_artifact_binding_contract


def test_project_artifact_binding_models_smoke() -> None:
    contract = build_project_artifact_binding_contract()

    assert contract.total_bindings == 8
    assert contract.ready_bindings == contract.total_bindings
    assert contract.source_bound_bindings == contract.total_bindings
    assert contract.storage_node_bound_bindings == contract.total_bindings
    assert contract.versioned_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
    assert contract.dashboard_visible_bindings == contract.total_bindings
    assert contract.runtime_load_allowed_bindings == 0
    assert contract.runtime_write_allowed_bindings == 0
    assert contract.runtime_execution_allowed_bindings == 0
    assert contract.model_repository_bindings == 2
    assert contract.knowledge_base_bindings == 3
    assert contract.project_workspace_bindings == 3
