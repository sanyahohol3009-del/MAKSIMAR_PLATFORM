from __future__ import annotations

from MAKSIMAR_SERVER.SANDBOX_REVIEW import build_owner_review_package


def test_owner_review_package_builder_smoke() -> None:
    package = build_owner_review_package()

    assert package["owner_review_package_ready"] is True
    assert package["missing_surfaces"] == ()
    assert package["owner_review_required"] is True
    assert package["owner_approval_required"] is True
    assert package["owner_approval_granted"] is False
    assert package["owner_approval_granted_by_default"] is False
