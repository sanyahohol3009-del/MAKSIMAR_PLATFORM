from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_contract,
)


def test_dashboard_read_only_views_memory_registry_root_binding_smoke() -> None:
    root_contract = build_dashboard_read_only_views_contract()
    memory_registry_views = build_memory_registry_view_contract()

    root_memory_registry_view_ids = {
        entry.view_id
        for entry in root_contract.entries
        if entry.view_kind == "memory_registry_read_only_view"
    }
    memory_registry_view_ids = {
        entry.view_id for entry in memory_registry_views.entries
    }

    assert root_memory_registry_view_ids == memory_registry_view_ids
    assert len(root_memory_registry_view_ids) == memory_registry_views.total_views
