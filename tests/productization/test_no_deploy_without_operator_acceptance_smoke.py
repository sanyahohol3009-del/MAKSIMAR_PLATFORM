from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_productization_preview


def test_no_deploy_without_operator_acceptance_smoke() -> None:
    preview = build_productization_preview()

    assert preview["operator_approval_required"] is True
    assert preview["operator_approval_granted"] is False
    assert preview["deployment_allowed_now"] is False
    assert preview["external_release_allowed_now"] is False
    assert preview["direct_core_write_allowed"] is False
