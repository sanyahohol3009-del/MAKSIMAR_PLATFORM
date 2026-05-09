from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_summary,
)


def test_memory_registry_summary_builder_smoke() -> None:
    summary = build_memory_registry_view_summary()

    assert summary["summary_ready"] is True
    assert summary["read_only"] is True
    assert summary["action_exposure_allowed"] is False
    assert summary["display_orchestration_allowed"] is False
    assert summary["retrieval_phase_ready"] is True
