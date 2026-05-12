from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_owner_review_preview


def test_sandbox_owner_review_preview_builder_smoke() -> None:
    preview = build_sandbox_owner_review_preview()

    assert preview["preview_ready"] is True
    assert "sandbox_binding" in preview["preview_path"]
    assert "owner_review_package" in preview["preview_path"]
    assert "self_expansion_next_only" in preview["preview_path"]
    assert preview["self_expansion_allowed_next"] is True
