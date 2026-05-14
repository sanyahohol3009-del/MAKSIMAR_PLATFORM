from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_polyglot_model_worker_read_model


def test_build_test_bridge_read_model_smoke() -> None:
    read_model = build_polyglot_model_worker_read_model()

    assert read_model["read_model_ready"] is True
    assert read_model["phase_id"] == "PHASE 6.7"
    assert read_model["artifact_language_models_ready"] is True
    assert read_model["language_bridge_models_ready"] is True
    assert read_model["model_worker_bridge_models_ready"] is True
    assert read_model["productization_allowed_now"] is False
