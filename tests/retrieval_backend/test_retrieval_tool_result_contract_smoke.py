from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalToolResultContract,
    build_default_evidence_binding_contract,
)


def test_retrieval_tool_result_requires_source_and_evidence() -> None:
    result = RetrievalToolResultContract(
        result_id="retrieval_tool_result_qdrant_status",
        tool_kind="qdrant_readonly",
        source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/qdrant_adapter_contract.py",
        evidence_binding=build_default_evidence_binding_contract(),
        output_text="qdrant is contract-ready and runtime-disabled.",
    )
    read_model = result.to_read_model()

    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["output_requires_normalization"] is True
    assert read_model["normalized_output_required"] is True
    assert read_model["read_only"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["evidence_binding"]["source_ref_required"] is True


def test_retrieval_tool_result_rejects_missing_evidence_binding() -> None:
    with pytest.raises(TypeError, match="evidence_binding"):
        RetrievalToolResultContract(
            result_id="retrieval_tool_result_bad",
            tool_kind="mgrep_readonly",
            source_ref="MAKSIMAR_CORE_LIB/retrieval_backend/mgrep_adapter_contract.py",
            evidence_binding=object(),  # type: ignore[arg-type]
            output_text="bad result",
        )
