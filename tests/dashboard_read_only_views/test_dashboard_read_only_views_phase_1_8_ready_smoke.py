from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_preview,
    build_dashboard_read_only_views_phase_readiness,
)


def test_dashboard_read_only_views_phase_1_8_ready_smoke() -> None:
    readiness = build_dashboard_read_only_views_phase_readiness()
    preview = build_dashboard_read_only_views_phase_preview()

    assert readiness.phase_ready is True
    assert preview["phase_ready"] is True
    assert readiness.root_total_entries == preview["root_total_entries"]
