from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_model_repository_contract


def test_model_repository_models_smoke() -> None:
    contract = build_model_repository_contract()

    assert contract.total_repositories == 2
    assert contract.ready_repositories == contract.total_repositories
    assert contract.source_bound_repositories == contract.total_repositories
    assert contract.versioned_repositories == contract.total_repositories
    assert contract.read_only_repositories == contract.total_repositories
    assert contract.runtime_load_allowed_repositories == 0
    assert contract.dashboard_visible_repositories == contract.total_repositories
