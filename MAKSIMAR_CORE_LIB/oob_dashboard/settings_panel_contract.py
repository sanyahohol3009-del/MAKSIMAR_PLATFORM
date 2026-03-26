from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.settings_panel_models import (
    DashboardSettingsPanel,
    SettingsEntry,
)


def build_dashboard_settings_panel() -> DashboardSettingsPanel:
    """Build settings panel contract."""

    entries = (
        SettingsEntry(key="display.layout", category="display", editable=True),
        SettingsEntry(key="input.mode", category="input", editable=True),
        SettingsEntry(key="security.level", category="security", editable=False),
        SettingsEntry(key="system.mode", category="system", editable=True),
    )

    return DashboardSettingsPanel(
        panel_id="panel_settings",
        entries=entries,
    )
