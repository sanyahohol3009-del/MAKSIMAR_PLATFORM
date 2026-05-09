from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    MemoryRegistryViewEntry,
)


def test_memory_registry_view_models_smoke() -> None:
    entry = MemoryRegistryViewEntry(
        view_id="view_memory_domain_map",
        panel_id="panel_memory_domain_map",
        source_component="MEMORY_REGISTRY",
        source_ref="read_only://memory_registry",
        visible_count=3,
        read_only=True,
        preview_ready=True,
        dashboard_visible=True,
    )

    assert entry.read_only is True
    assert entry.preview_ready is True
    assert entry.dashboard_visible is True
