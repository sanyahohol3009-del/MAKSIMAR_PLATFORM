from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_panel_contract,
    build_memory_registry_view_contract,
    build_memory_registry_view_preview,
)


def test_memory_registry_views_ready_smoke() -> None:
    panels = build_memory_registry_panel_contract()
    views = build_memory_registry_view_contract()
    preview = build_memory_registry_view_preview()

    assert panels.total_panels >= 1
    assert views.total_views == panels.total_panels
    assert preview["preview_ready"] is True
    assert preview["total_panels"] == panels.total_panels
    assert preview["total_views"] == views.total_views
