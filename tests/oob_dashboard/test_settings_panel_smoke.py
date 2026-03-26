from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_settings_panel,
)


def test_settings_panel_builds() -> None:
    panel = build_dashboard_settings_panel()

    assert panel.panel_id == "panel_settings"
    assert len(panel.entries) >= 1
