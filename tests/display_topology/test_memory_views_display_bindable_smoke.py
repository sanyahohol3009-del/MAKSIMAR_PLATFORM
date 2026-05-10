from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_display_topology_summary


def test_memory_views_display_bindable_smoke() -> None:
    summary = build_display_topology_summary()

    assert summary["memory_views_display_bindable"] is True
    assert summary["dashboard_root_entries"] == 10
    assert summary["display_registry_entries"] == 3
    assert summary["direct_switching_allowed"] == 0
