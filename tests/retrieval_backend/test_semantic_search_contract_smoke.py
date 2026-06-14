from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    SemanticSearchContract,
    build_default_semantic_search_contract,
)


def test_semantic_search_contract_smoke() -> None:
    contract = build_default_semantic_search_contract()
    read_model = contract.to_read_model()

    assert isinstance(contract, SemanticSearchContract)
    assert read_model["query_text"]
    assert read_model["top_k"] == 10
    assert read_model["requested_domains"] == ("project_history", "technical_memory")
    assert read_model["source_scope"]
    assert read_model["evidence_required"] is True
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["normalized_request_metadata_only"] is True
    assert read_model["backend_execution_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["source_of_truth"] is False


def test_semantic_search_contract_rejects_empty_query_and_unbounded_top_k() -> None:
    with pytest.raises(ValueError, match="query_text"):
        SemanticSearchContract(
            query_id="semantic_search_query_empty",
            query_text="",
            requested_domains=("technical_memory",),
            top_k=10,
            filters=(),
            source_scope=("MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",),
        )

    with pytest.raises(ValueError, match="top_k"):
        SemanticSearchContract(
            query_id="semantic_search_query_unbounded",
            query_text="memory",
            requested_domains=("technical_memory",),
            top_k=51,
            filters=(),
            source_scope=("MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",),
        )


def test_semantic_search_contract_is_metadata_not_backend_execution() -> None:
    unsafe_fields = ("backend_execution_allowed", "direct_execution_allowed", "source_of_truth")
    for field_name in unsafe_fields:
        with pytest.raises(ValueError, match=field_name):
            SemanticSearchContract(
                query_id=f"semantic_search_query_bad_{field_name}",
                query_text="memory",
                requested_domains=("technical_memory",),
                top_k=10,
                filters=(),
                source_scope=("MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing",),
                **{field_name: True},
            )
