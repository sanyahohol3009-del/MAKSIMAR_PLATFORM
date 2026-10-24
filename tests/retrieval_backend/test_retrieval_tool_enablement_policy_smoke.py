from __future__ import annotations

from MAKSIMAR_CORE_LIB.retrieval_backend import build_retrieval_tool_enablement_policy


def test_retrieval_tool_enablement_policy_accepts_only_typed_selection_and_blocks_runtime() -> None:
    policy = build_retrieval_tool_enablement_policy()
    read_model = policy.to_read_model()

    assert read_model["selection_input"] == "typed_plan_step"
    assert read_model["semantic_selection_performed"] is False
    assert read_model["read_only_tool_contracts_allowed"] is True
    assert read_model["backend_runtime_enabled"] is False
    assert read_model["runtime_tool_execution_enabled"] is False
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["output_requires_normalization"] is True
    assert read_model["truth_owner"] == "canonical_semantic_spine"
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert "pc_control_allowed" not in read_model
