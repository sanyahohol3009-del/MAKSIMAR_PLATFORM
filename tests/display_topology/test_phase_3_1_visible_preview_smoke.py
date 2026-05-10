from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_phase_preview,
    build_display_topology_preview,
)


def test_phase_3_1_visible_preview_smoke() -> None:
    preview = build_display_topology_preview()
    phase_preview = build_display_topology_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["display_topology_displays"] == 3
    assert preview["display_registry_entries"] == 3
    assert preview["zone_layout_entries"] == 8
    assert preview["display_capability_entries"] == 11
    assert preview["display_assignment_bindings"] == 3
    assert preview["direct_switching_allowed"] == 0
    assert preview["memory_views_display_bindable"] is True

    assert phase_preview["preview_ready"] is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["no_new_display_roots"] is True
