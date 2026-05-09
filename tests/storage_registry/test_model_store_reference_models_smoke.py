from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_model_store_reference,
)


def test_model_store_reference_models_smoke() -> None:
    reference = build_model_store_reference()

    assert reference.model_store_id == "model_store_local_weights"
    assert reference.weights_external is True
    assert reference.portable is True
