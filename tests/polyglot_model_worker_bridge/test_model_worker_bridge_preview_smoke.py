from __future__ import annotations

from MAKSIMAR_SERVER.POLYGLOT_MODEL_WORKER_BRIDGE import build_model_worker_bridge_preview


def test_model_worker_bridge_preview_smoke() -> None:
    preview = build_model_worker_bridge_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_required_surfaces"] == ()
    assert preview["language_bridge_ready"] is True
    assert preview["client_learning_input_ready"] is True
    assert preview["productization_allowed_next"] is True
