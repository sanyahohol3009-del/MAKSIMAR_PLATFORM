from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_artifact_collection_reference,
)


def test_artifact_collection_models_smoke() -> None:
    reference = build_artifact_collection_reference()

    assert reference.collection_id == "artifact_collection_domain_artifacts"
    assert reference.portable is True
    assert reference.dashboard_ready is True
