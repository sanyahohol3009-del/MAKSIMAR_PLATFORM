from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.memory_index_contract import (
    build_memory_index_readiness_read_model,
    build_memory_index_reference,
)
from MAKSIMAR_CORE_LIB.data_plane.memory_index_models import MemoryIndexReference


def test_memory_index_reference_links_object_and_vector_refs() -> None:
    reference = build_memory_index_reference(
        memory_index_id="memory_index_technical",
        domain_id="technical_memory",
        source_ref="source://doc/1",
        evidence_ref="evidence://pack/1",
        object_ref="object://payload/1",
        vector_ref="vector://memory/1",
        producer_layer_id="DATA_PLANE",
        trace_id="trace-memory-index-1",
    )
    read_model = build_memory_index_readiness_read_model(reference)

    assert reference.inline_memory_payload_allowed is False
    assert reference.canonical_write_allowed is False
    assert read_model.memory_index_id == "memory_index_technical"
    assert read_model.vector_ref == "vector://memory/1"


def test_memory_index_rejects_inline_memory_payload() -> None:
    with pytest.raises(ValueError, match="inline_memory_payload_allowed"):
        MemoryIndexReference(
            memory_index_id="bad",
            domain_id="technical_memory",
            source_ref="source://doc/1",
            evidence_ref="evidence://pack/1",
            object_ref="object://payload/1",
            vector_ref="vector://memory/1",
            producer_layer_id="DATA_PLANE",
            trace_id="trace-bad",
            inline_memory_payload_allowed=True,
        )
