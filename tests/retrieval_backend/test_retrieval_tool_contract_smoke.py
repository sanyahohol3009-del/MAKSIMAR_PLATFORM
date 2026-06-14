from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalToolContract,
    build_retrieval_tool_contracts,
)


def test_retrieval_tool_contracts_are_read_only_and_not_registered_runtime() -> None:
    tools = build_retrieval_tool_contracts()
    assert tuple(tool.tool_kind for tool in tools) == ("mgrep_readonly", "sqlite_vec_readonly", "qdrant_readonly")

    for tool in tools:
        read_model = tool.to_read_model()
        assert read_model["read_only"] is True
        assert read_model["auto_selection_allowed"] is True
        assert read_model["source_ref_required"] is True
        assert read_model["evidence_binding_required"] is True
        assert read_model["output_requires_normalization"] is True
        assert read_model["source_of_truth"] is False
        assert read_model["canonical_write_allowed"] is False
        assert read_model["runtime_mutation_allowed"] is False
        assert read_model["direct_execution_allowed"] is False
        assert read_model["network_allowed_by_default"] is False
        assert read_model["approval_required_before_runtime"] is True
        assert read_model["runtime_enabled"] is False
        assert read_model["registered_with_jarvis_runtime"] is False


def test_retrieval_tool_contract_rejects_direct_execution() -> None:
    with pytest.raises(ValueError, match="direct_execution_allowed"):
        RetrievalToolContract(
            tool_id="retrieval_tool_qdrant_readonly",
            tool_kind="qdrant_readonly",
            backend_kind="qdrant",
            policy_gate_ref="MAKSIMAR_CORE_LIB/retrieval_backend/retrieval_tool_enablement_policy.py",
            source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/qdrant_adapter_contract.py",
            direct_execution_allowed=True,
        )
