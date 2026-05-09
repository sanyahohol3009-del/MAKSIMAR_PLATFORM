from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)


def test_dashboard_read_only_views_memory_registry_binding_consistency_smoke() -> None:
    readiness = build_dashboard_read_only_views_phase_readiness()

    assert readiness.memory_registry_root_entries == readiness.memory_registry_view_entries
    assert readiness.root_total_entries == (
        readiness.legacy_root_entries + readiness.memory_registry_root_entries
    )
