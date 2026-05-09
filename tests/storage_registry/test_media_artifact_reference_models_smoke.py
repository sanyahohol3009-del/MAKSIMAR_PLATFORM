from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_media_artifact_reference,
)


def test_media_artifact_reference_models_smoke() -> None:
    reference = build_media_artifact_reference()

    assert reference.media_store_id == "media_store_generated_media"
    assert reference.raw_binary_external is True
    assert reference.retrieval_indexed is True
