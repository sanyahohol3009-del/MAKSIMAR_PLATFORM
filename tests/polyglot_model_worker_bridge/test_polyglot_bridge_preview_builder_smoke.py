from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_polyglot_model_worker_preview


def test_polyglot_bridge_preview_builder_smoke() -> None:
    preview = build_polyglot_model_worker_preview()

    assert preview["preview_ready"] is True
    assert "artifact_language_models" in preview["preview_path"]
    assert "model_worker_bridge_models" in preview["preview_path"]
    assert "productization_next_only" in preview["preview_path"]
    assert preview["productization_allowed_next"] is True
