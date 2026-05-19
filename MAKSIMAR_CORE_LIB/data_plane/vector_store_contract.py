from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.vector_store_models import (
    VectorStoreBackendKind,
    VectorStoreReadinessReadModel,
    VectorStoreReference,
)


def build_vector_store_reference(
    *,
    vector_ref: str,
    vector_store_id: str,
    namespace_id: str,
    backend_kind: VectorStoreBackendKind,
    embedding_model_ref: str,
    dimension: int,
    metadata_ref: str,
    payload_ref: str,
    producer_layer_id: str,
    trace_id: str,
) -> VectorStoreReference:
    return VectorStoreReference(
        vector_ref=vector_ref,
        vector_store_id=vector_store_id,
        namespace_id=namespace_id,
        backend_kind=backend_kind,
        embedding_model_ref=embedding_model_ref,
        dimension=dimension,
        metadata_ref=metadata_ref,
        payload_ref=payload_ref,
        producer_layer_id=producer_layer_id,
        trace_id=trace_id,
    )


def build_vector_store_readiness_read_model(
    reference: VectorStoreReference,
) -> VectorStoreReadinessReadModel:
    if not isinstance(reference, VectorStoreReference):
        raise TypeError("reference must be VectorStoreReference")

    return VectorStoreReadinessReadModel(
        vector_store_id=reference.vector_store_id,
        backend_kind=reference.backend_kind.value,
        namespace_id=reference.namespace_id,
        dimension=reference.dimension,
        reason_codes=("vector_store_reference_validated", "backend_runtime_policy_gated"),
    )
