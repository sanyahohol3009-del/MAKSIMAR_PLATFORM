from __future__ import annotations

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_client_learning_input_preview


def test_client_learning_input_preview_builder_smoke() -> None:
    preview = build_client_learning_input_preview()

    assert preview["preview_ready"] is True
    assert "client_metrics_filter_policy" in preview["preview_path"]
    assert "learning_input_pack" in preview["preview_path"]
    assert "polyglot_model_worker_next_only" in preview["preview_path"]
    assert preview["polyglot_model_worker_allowed_next"] is True
