from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_preview,
)


def test_dashboard_read_only_views_phase_preview_smoke() -> None:
    preview = build_dashboard_read_only_views_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_ready"] is True
    assert preview["root_contract_ready"] is True
    assert preview["memory_registry_views_bound"] is True
    assert preview["flow"] == (
        "dashboard_root_contract",
        "memory_registry_views",
        "root_binding",
        "read_only_gate",
        "no_action_gate",
        "no_display_orchestration_gate",
        "phase_readiness",
    )
