from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_sandbox_owner_review_preview


def test_no_self_expansion_before_owner_review_smoke() -> None:
    preview = build_sandbox_owner_review_preview()

    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed"] is False
    assert preview["auto_apply_allowed"] is False
    assert preview["self_expansion_allowed_now"] is False
    assert preview["productization_allowed_now"] is False
