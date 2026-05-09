from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_preview,
)


def test_memory_registry_preview_builder_smoke() -> None:
    preview = build_memory_registry_view_preview()

    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["retrieval_phase_ready"] is True
    assert preview["flow"] == (
        "memory_registry_summary",
        "panel_contract",
        "view_contract",
        "dashboard_read_only_preview",
    )
