from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_deployment_boundary_review_preview


def test_deployment_boundary_review_smoke() -> None:
    preview = build_deployment_boundary_review_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_required_surfaces"] == ()
    assert preview["deployment_allowed_now"] is False
    assert preview["external_release_allowed_now"] is False
    assert preview["rollback_required"] is True
    assert preview["operator_approval_required"] is True
