from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    build_panel_id_vocabulary_normalization_model,
    normalize_panel_id,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_models import (
    DashboardPanelRegistryContract,
    RegisteredPanel,
)


def build_dashboard_panel_registry_contract() -> DashboardPanelRegistryContract:
    """Build unified dashboard panel registry contract."""

    vocabulary_model = build_panel_id_vocabulary_normalization_model()
    vocabulary_entries = {
        entry.canonical_panel_id: entry for entry in vocabulary_model.entries
    }

    panel_specs = (
        ("panel_consistency", "core", True),
        ("panel_snapshot", "core", True),
        ("panel_incident", "diagnostics", True),
        ("panel_diagnostics", "diagnostics", True),
        ("panel_chat", "interaction", True),
        ("panel_settings", "settings", True),
        ("panel_gesture_control", "control", True),
    )

    panels = tuple(
        RegisteredPanel(
            panel_id=canonical_panel_id,
            label=vocabulary_entries[canonical_panel_id].display_title,
            category=category,
            visible_in_sidebar=visible_in_sidebar,
            panel_family=vocabulary_entries[canonical_panel_id].panel_family,
            panel_kind=vocabulary_entries[canonical_panel_id].panel_kind,
            panel_role=vocabulary_entries[canonical_panel_id].panel_role,
        )
        for panel_id, category, visible_in_sidebar in panel_specs
        for canonical_panel_id in (normalize_panel_id(panel_id),)
    )

    return DashboardPanelRegistryContract(
        total_panels=len(panels),
        panels=panels,
        visible_in_sidebar_panels=sum(
            1 for panel in panels if panel.visible_in_sidebar
        ),
    )
