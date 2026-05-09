from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_panel_contract,
    build_memory_registry_view_preview,
)


def test_memory_registry_read_only_no_actions_smoke() -> None:
    contract = build_memory_registry_panel_contract()
    preview = build_memory_registry_view_preview()

    assert preview["read_only"] is True
    assert preview["action_exposure_allowed"] is False
    assert preview["display_orchestration_allowed"] is False
    assert contract.action_exposure_allowed_panels == 0
    assert contract.display_orchestration_allowed_panels == 0
