from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    MemoryRegistryPanelEntry,
)


def test_memory_registry_panel_models_smoke() -> None:
    entry = MemoryRegistryPanelEntry(
        panel_id="panel_memory_domain_map",
        panel_kind="memory_domain_map",
        title="Memory Domain Map",
        source_component="MEMORY_REGISTRY",
        source_entries=3,
        visible_entries=3,
        read_only=True,
        action_exposure_allowed=False,
        display_orchestration_allowed=False,
        status="ready",
    )

    assert entry.read_only is True
    assert entry.action_exposure_allowed is False
    assert entry.display_orchestration_allowed is False
