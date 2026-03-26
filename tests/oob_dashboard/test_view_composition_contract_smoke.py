from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_view_composition_contract,
)


def test_view_composition_contract_builds() -> None:
    """View composition contract should build successfully."""
    contract = build_dashboard_view_composition_contract()

    assert contract.total_panels == 7
    assert len(contract.composed_panels) == 7


def test_view_composition_contract_has_active_panel() -> None:
    """View composition contract should expose active panel."""
    contract = build_dashboard_view_composition_contract()

    assert contract.active_panel_id == "panel_consistency"
