from __future__ import annotations

from MAKSIMAR_SERVER.CODEGEN_CONTEXT import build_codegen_preview


def test_codegen_preview_builder_smoke() -> None:
    preview = build_codegen_preview()

    assert preview["preview_ready"] is True
    assert "codegen_intent_models" in preview["preview_path"]
    assert "sandbox_owner_review_next_only" in preview["preview_path"]
    assert preview["direct_core_write_allowed"] is False
    assert preview["sandbox_owner_review_allowed_next"] is True
