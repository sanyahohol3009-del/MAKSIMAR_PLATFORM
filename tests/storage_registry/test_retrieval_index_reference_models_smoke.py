from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_retrieval_index_reference,
)


def test_retrieval_index_reference_models_smoke() -> None:
    reference = build_retrieval_index_reference()

    assert reference.retrieval_index_id == "retrieval_index_semantic_memory"
    assert reference.backend_kind == "sqlite_vec_or_vector_backend"
    assert reference.portable is True
