from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_panel_contract,
)


def test_memory_registry_panel_builder_smoke() -> None:
    contract = build_memory_registry_panel_contract()

    assert contract.total_panels == len(contract.entries)
    assert contract.ready_panels == contract.total_panels
    assert contract.read_only_panels == contract.total_panels
    assert contract.action_exposure_allowed_panels == 0
    assert contract.display_orchestration_allowed_panels == 0
