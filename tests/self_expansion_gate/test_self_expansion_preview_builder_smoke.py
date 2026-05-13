from __future__ import annotations

from MAKSIMAR_SERVER.SELF_EXPANSION_GATE import build_self_expansion_preview


def test_self_expansion_preview_builder_smoke() -> None:
    preview = build_self_expansion_preview()

    assert preview["preview_ready"] is True
    assert "self_expansion_readiness" in preview["preview_path"]
    assert "client_metrics_learning_next_only" in preview["preview_path"]
    assert preview["proposal_only_self_expansion_allowed"] is True
    assert preview["autonomous_self_expansion_allowed"] is False
    assert preview["client_metrics_learning_allowed_next"] is True
