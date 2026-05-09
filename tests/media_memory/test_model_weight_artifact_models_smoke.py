from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import build_model_weight_artifact_memory


def test_model_weight_artifact_models_smoke() -> None:
    memory = build_model_weight_artifact_memory()

    assert memory.binary_external is True
    assert memory.checksum_required is True
    assert memory.license_review_required is True
