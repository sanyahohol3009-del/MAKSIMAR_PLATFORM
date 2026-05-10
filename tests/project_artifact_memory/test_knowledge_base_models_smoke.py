from __future__ import annotations

from MAKSIMAR_CORE_LIB.project_artifact_memory import build_knowledge_base_contract


def test_knowledge_base_models_smoke() -> None:
    contract = build_knowledge_base_contract()

    assert contract.total_knowledge_bases == 3
    assert contract.ready_knowledge_bases == contract.total_knowledge_bases
    assert contract.source_bound_knowledge_bases == contract.total_knowledge_bases
    assert contract.versioned_knowledge_bases == contract.total_knowledge_bases
    assert contract.read_only_knowledge_bases == contract.total_knowledge_bases
    assert contract.retrieval_enabled_knowledge_bases == contract.total_knowledge_bases
    assert contract.runtime_write_allowed_knowledge_bases == 0
    assert contract.dashboard_visible_knowledge_bases == contract.total_knowledge_bases
