from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_contract,
)


def test_memory_registry_view_builder_smoke() -> None:
    contract = build_memory_registry_view_contract()

    assert contract.total_views == len(contract.entries)
    assert contract.read_only_views == contract.total_views
    assert contract.preview_ready_views == contract.total_views
    assert contract.dashboard_visible_views == contract.total_views
