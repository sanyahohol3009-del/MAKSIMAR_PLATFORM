from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_dataset_artifact_memory


def test_dataset_artifact_models_smoke() -> None:
    memory = build_dataset_artifact_memory()

    assert memory.imported_dataset is True
    assert memory.review_required_before_trust is True
    assert memory.retrieval_index_allowed is True
