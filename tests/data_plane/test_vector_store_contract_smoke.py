from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.vector_store_contract import (
    build_vector_store_readiness_read_model,
    build_vector_store_reference,
)
from MAKSIMAR_CORE_LIB.data_plane.vector_store_models import (
    VectorStoreBackendKind,
    VectorStoreReference,
)


def test_vector_store_reference_keeps_backend_policy_gated() -> None:
    reference = build_vector_store_reference(
        vector_ref="vector://memory/1",
        vector_store_id="vector_store_policy_surface",
        namespace_id="technical_memory",
        backend_kind=VectorStoreBackendKind.SQLITE_VEC,
        embedding_model_ref="embedding-model://local/policy",
        dimension=1024,
        metadata_ref="object://metadata/1",
        payload_ref="object://payload/1",
        producer_layer_id="DATA_PLANE",
        trace_id="trace-vector-1",
    )
    read_model = build_vector_store_readiness_read_model(reference)

    assert reference.backend_kind is VectorStoreBackendKind.SQLITE_VEC
    assert reference.backend_runtime_enabled is False
    assert reference.vector_payload_inline_allowed is False
    assert read_model.backend_kind == "sqlite_vec"
    assert read_model.backend_runtime_enabled is False


def test_vector_store_rejects_runtime_enabled_contract() -> None:
    with pytest.raises(ValueError, match="backend_runtime_enabled"):
        VectorStoreReference(
            vector_ref="vector://bad",
            vector_store_id="vector_store_policy_surface",
            namespace_id="technical_memory",
            backend_kind=VectorStoreBackendKind.QDRANT,
            embedding_model_ref="embedding-model://local/policy",
            dimension=1024,
            metadata_ref="object://metadata/1",
            payload_ref="object://payload/1",
            producer_layer_id="DATA_PLANE",
            trace_id="trace-bad",
            backend_runtime_enabled=True,
        )
