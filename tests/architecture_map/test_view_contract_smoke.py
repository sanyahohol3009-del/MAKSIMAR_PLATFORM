from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_dashboard_view_registry_contract,
)


def test_dashboard_view_registry_contract_builds() -> None:
    """Dashboard view registry contract should build successfully."""
    contract = build_dashboard_view_registry_contract()

    assert contract.total_views == 3
    assert len(contract.views) == 3


def test_dashboard_view_registry_is_read_only() -> None:
    """Dashboard architecture views should remain read-only."""
    contract = build_dashboard_view_registry_contract()

    assert all(view.read_only for view in contract.views)
