from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_operator_acceptance_preview


def test_operator_acceptance_package_smoke() -> None:
    preview = build_operator_acceptance_preview()

    assert preview["preview_ready"] is True
    assert preview["acceptance_item_count"] >= 8
    assert preview["operator_approval_required"] is True
    assert preview["operator_approval_granted"] is False
    assert preview["hidden_autonomy_allowed"] is False
