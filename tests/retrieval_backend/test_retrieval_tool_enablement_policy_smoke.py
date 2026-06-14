from __future__ import annotations

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    SEMANTIC_INTENT_GROUPS,
    build_retrieval_tool_enablement_policy,
    classify_retrieval_semantic_intent,
)


def test_retrieval_tool_enablement_policy_records_semantic_groups_and_blocks_runtime() -> None:
    policy = build_retrieval_tool_enablement_policy()
    read_model = policy.to_read_model()

    assert read_model["semantic_intent_groups"] == SEMANTIC_INTENT_GROUPS
    assert "project_delta" in read_model["semantic_intent_groups"]
    assert "file_lookup" in read_model["semantic_intent_groups"]
    assert "project_code_search" in read_model["semantic_intent_groups"]
    assert "memory_history" in read_model["semantic_intent_groups"]
    assert "semantic_similarity" in read_model["semantic_intent_groups"]
    assert "backend_status" in read_model["semantic_intent_groups"]
    assert "autonomous_read_only_tool_use" in read_model["semantic_intent_groups"]
    assert read_model["read_only_tool_contracts_allowed"] is True
    assert read_model["auto_routing_contract_allowed"] is True
    assert read_model["runtime_tool_execution_enabled"] is False
    assert read_model["auto_routing_runtime_enabled"] is False
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["output_requires_normalization"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["pc_control_allowed"] is False


def test_retrieval_semantic_classifier_covers_operator_language_and_aliases() -> None:
    examples = {
        "что изменилось после 7.4": "project_delta",
        "где находится qdrant contract": "file_lookup",
        "найди где есть evidence_binding_required": "project_code_search",
        "что мы решили по source of truth": "memory_history",
        "проверь semantic duplicate risk": "semantic_similarity",
        "что по qdrnt": "backend_status",
        "что по aqlite-vec": "backend_status",
        "что по mgreo": "backend_status",
        "7.4 закрыт?": "roadmap_readiness",
        "сколько passed": "test_validation",
        "покажи source ref": "source_evidence_audit",
        "где runtime profile": "architecture_docs",
        "vendor gate passed?": "vendor_quarantine",
        "docker можно запускать?": "container_runtime_boundary",
        "сам выбери инструмент и найди доказательства": "autonomous_read_only_tool_use",
    }

    for text, expected_group in examples.items():
        classification = classify_retrieval_semantic_intent(text)
        read_model = classification.to_read_model()
        assert read_model["matched"] is True, text
        assert read_model["intent_group"] == expected_group
        assert read_model["read_only"] is True
        assert read_model["source_ref_required"] is True
        assert read_model["evidence_binding_required"] is True
        assert read_model["direct_execution_allowed"] is False


def test_retrieval_semantic_policy_exports_full_rule_catalog() -> None:
    read_model = build_retrieval_tool_enablement_policy().to_read_model()
    rules = read_model["semantic_intent_rules"]

    assert len(rules) == len(SEMANTIC_INTENT_GROUPS)
    assert [rule["intent_group"] for rule in rules] == list(SEMANTIC_INTENT_GROUPS)
    assert all(rule["read_only_tools"] for rule in rules)
    assert all(rule["phrases"] for rule in rules)
