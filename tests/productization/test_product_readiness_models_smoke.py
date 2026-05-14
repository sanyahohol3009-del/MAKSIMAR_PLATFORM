from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_product_readiness_preview


def test_product_readiness_models_smoke() -> None:
    preview = build_product_readiness_preview()

    assert preview["preview_ready"] is True
    assert preview["missing_required_surfaces"] == ()
    assert preview["sale_ready_packaging_allowed"] is True
    assert preview["operator_acceptance_required"] is True
    assert preview["hidden_autonomy_allowed"] is False
    assert preview["deployment_allowed_now"] is False
