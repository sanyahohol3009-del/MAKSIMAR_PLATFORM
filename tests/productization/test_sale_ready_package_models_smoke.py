from __future__ import annotations

from MAKSIMAR_SERVER.PRODUCTIZATION import build_sale_ready_package


def test_sale_ready_package_models_smoke() -> None:
    package = build_sale_ready_package()

    assert package.sale_ready_package_ready is True
    assert len(package.package_items) >= 7
    assert package.operator_visible is True
    assert package.approval_required is True
    assert package.external_deploy_allowed is False
    assert package.productization_claim_allowed is True
