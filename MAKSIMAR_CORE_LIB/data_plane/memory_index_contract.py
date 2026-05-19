from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.memory_index_models import (
    MemoryIndexReadinessReadModel,
    MemoryIndexReference,
)


def build_memory_index_reference(
    *,
    memory_index_id: str,
    domain_id: str,
    source_ref: str,
    evidence_ref: str,
    object_ref: str,
    vector_ref: str,
    producer_layer_id: str,
    trace_id: str,
) -> MemoryIndexReference:
    return MemoryIndexReference(
        memory_index_id=memory_index_id,
        domain_id=domain_id,
        source_ref=source_ref,
        evidence_ref=evidence_ref,
        object_ref=object_ref,
        vector_ref=vector_ref,
        producer_layer_id=producer_layer_id,
        trace_id=trace_id,
    )


def build_memory_index_readiness_read_model(
    reference: MemoryIndexReference,
) -> MemoryIndexReadinessReadModel:
    if not isinstance(reference, MemoryIndexReference):
        raise TypeError("reference must be MemoryIndexReference")

    return MemoryIndexReadinessReadModel(
        memory_index_id=reference.memory_index_id,
        domain_id=reference.domain_id,
        object_ref=reference.object_ref,
        vector_ref=reference.vector_ref,
        reason_codes=("memory_index_reference_validated",),
    )
