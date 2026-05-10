from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_display_topology_preview


def test_display_topology_preview_builder_smoke() -> None:
    preview = build_display_topology_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["display_topology_displays"] == 3
    assert preview["display_ids"] == (
        "display_primary_dashboard_001",
        "display_engineering_001",
        "display_mobile_proxy_001",
    )
    assert preview["display_roles"] == (
        "primary_dashboard_display",
        "engineering_display",
        "mobile_display_proxy",
    )
    assert preview["action_execution_allowed"] == 0
    assert preview["backend_execution_allowed"] == 0
