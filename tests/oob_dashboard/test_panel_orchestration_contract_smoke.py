from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_panel_orchestration_contract,
)


def test_panel_orchestration_contract_builds() -> None:
    """Panel orchestration contract should build successfully."""
    contract = build_dashboard_panel_orchestration_contract()

    assert len(contract.panels) >= 1
    assert contract.navigation_enabled is True
    assert contract.input_routing_enabled is True


def test_panel_orchestration_has_active_panel() -> None:
    """Panel orchestration contract should expose active panel."""
    contract = build_dashboard_panel_orchestration_contract()

    assert isinstance(contract.active_panel_id, str)
    assert contract.active_panel_id != ""
