from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    RetrievalToolRegistryContract,
    build_retrieval_tool_contracts,
    build_retrieval_tool_registry_contract,
)


def test_retrieval_tool_registry_enables_readonly_router_without_backend_runtime() -> None:
    registry = build_retrieval_tool_registry_contract()
    read_model = registry.to_read_model()

    assert read_model["registry_id"] == "retrieval_tool_registry_contract_v1"
    assert read_model["read_only"] is True
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["output_requires_normalization"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["direct_execution_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["readonly_router_registration_enabled"] is True
    assert read_model["auto_routing_readonly_enabled"] is True
    assert read_model["runtime_registration_enabled"] is False
    assert read_model["auto_routing_runtime_enabled"] is False
    assert [tool["tool_kind"] for tool in read_model["tools"]] == [
        "mgrep_readonly",
        "sqlite_vec_readonly",
        "qdrant_readonly",
    ]


def test_retrieval_tool_registry_rejects_backend_runtime_registration() -> None:
    with pytest.raises(ValueError, match="runtime_registration_enabled"):
        RetrievalToolRegistryContract(
            registry_id="retrieval_tool_registry_contract_v1",
            tools=build_retrieval_tool_contracts(),
            runtime_registration_enabled=True,
        )
