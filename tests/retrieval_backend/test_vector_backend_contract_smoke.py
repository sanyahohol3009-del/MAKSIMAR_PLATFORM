from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.retrieval_backend import (
    VectorBackendContract,
    build_default_vector_backend_contract,
)


def test_vector_backend_contract_smoke() -> None:
    contract = build_default_vector_backend_contract()
    read_model = contract.to_read_model()

    assert isinstance(contract, VectorBackendContract)
    assert read_model["backend_kind"] == "in_memory_reference"
    assert read_model["vector_store_backend_kind"] == "contract_only"
    assert read_model["supports_embeddings_metadata"] is True
    assert read_model["supports_search_metadata"] is True
    assert read_model["metadata_only"] is True
    assert read_model["source_ref_required"] is True
    assert read_model["evidence_binding_required"] is True
    assert read_model["source_of_truth"] is False
    assert read_model["direct_write_allowed"] is False
    assert read_model["network_allowed_by_default"] is False
    assert read_model["runtime_mutation_allowed"] is False
    assert read_model["canonical_write_allowed"] is False


def test_vector_backend_contract_maps_existing_vector_store_backend_kinds() -> None:
    qdrant = VectorBackendContract(
        vector_backend_id="vector_backend_qdrant",
        backend_kind="qdrant",
        namespace_id="retrieval_backend_contracts",
        embedding_model_ref="model://embedding",
        dimension=384,
        supported_capabilities=("embedding_metadata", "search_metadata"),
    )
    sqlite_vec = VectorBackendContract(
        vector_backend_id="vector_backend_sqlite_vec",
        backend_kind="sqlite_vec",
        namespace_id="retrieval_backend_contracts",
        embedding_model_ref="model://embedding",
        dimension=384,
        supported_capabilities=("embedding_metadata", "search_metadata"),
    )

    assert qdrant.vector_store_backend_kind().value == "qdrant"
    assert sqlite_vec.vector_store_backend_kind().value == "sqlite_vec"


def test_vector_backend_contract_rejects_write_runtime_network_truth() -> None:
    unsafe_fields = (
        "source_of_truth",
        "direct_write_allowed",
        "network_allowed_by_default",
        "runtime_mutation_allowed",
        "canonical_write_allowed",
    )
    for field_name in unsafe_fields:
        with pytest.raises(ValueError, match=field_name):
            VectorBackendContract(
                vector_backend_id=f"vector_backend_bad_{field_name}",
                backend_kind="qdrant",
                namespace_id="retrieval_backend_contracts",
                embedding_model_ref="model://embedding",
                dimension=384,
                supported_capabilities=("embedding_metadata", "search_metadata"),
                **{field_name: True},
            )
